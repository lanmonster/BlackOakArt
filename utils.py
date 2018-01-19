import flask
import socket
import datetime

from PurchaseOrder import PurchaseOrder  # mine (PurchaseOrder.py)
from Progress import Progress
import queries


tasks = ["prep", "throw", "debat", "trim", "assemble", "polish", "stamp", "handle", 'ADN']


def task_to_end_of_day_format(task):
    if task == "prep":
        return "prepped"
    elif task == "throw":
        return "thrown"
    elif task == "debat":
        return "debatted"
    elif task == "trim":
        return "trimmed"
    elif task == "assemble":
        return "assembled"
    elif task == "polish":
        return "polished"
    elif task == "stamp":
        return "stamps"
    elif task == "handle":
        return "handles"
    elif task == "ADN":
        return "ADN"


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def add_po(data, connection):
    cursor = connection.cursor()
    cursor.execute(queries.add(data))
    cursor.execute("SELECT id FROM public.purchaseorders")
    ids = [x[0] for x in cursor.fetchall()]
    po_id = max(ids)
    for task in [x for x in tasks if x != "ADN"]:
        cursor.execute(queries.insert_into_have(task, po_id, str(data['item']), str(data['clay_type']), 0))
        cursor.execute(queries.insert_into_leftover(task, po_id, str(data['item']), str(data['clay_type']), 0))


def delete_po(po_id, connection):
    cursor = connection.cursor()
    cursor.execute(queries.delete_from("purchaseorders", po_id))
    if cursor.rowcount > 0:
        for task in [x for x in tasks if x != "ADN"]:
            cursor.execute("DELETE FROM have.%s WHERE id = %s" % (task, str(po_id)))
            cursor.execute("DELETE FROM leftover.%s WHERE id = %s" % (task, str(po_id)))
        connection.commit()
        flash_message("PO deleted!", category='success')
    else:
        flash_message("That id does not exist! Try another.", category='error')


def update_leftovers(po, connection):
    cursor = connection.cursor()
    for task in [x for x in tasks if x != "ADN"]:
        cursor.execute(queries.update_leftover(task, po['id'], task, po['nums'][8]))
    connection.commit()


def update_haves(po, connection):
    cursor = connection.cursor()
    for task in [x for x in tasks if x != "ADN"]:
        cursor.execute(queries.update_have(task, po['id'], task, po['nums'][8]))
    connection.commit()


def update_debat_numbers(po, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT amount FROM public.debat WHERE id = %s" % po['id'])
    amount = cursor.fetchone()[0]
    if amount:
        amount -= int(po['nums'][2])
        if amount <= 0:
            cursor.execute("DELETE FROM public.debat WHERE id = %s" % po['id'])
        else:
            cursor.execute("UPDATE public.debat SET amount = %d WHERE id = %s" % (amount, po['id']))
        amount += int(po['nums'][1])
        if amount > 0:
            cursor.execute("UPDATE public.debat SET amount = %d WHERE id = %s" % (amount, po['id']))
    connection.commit()


def calculate_percent_complete(po, connection):  # todo
    # sum of all (amt through step / total) * (1/steps) for steps
    prog = fetch_progress(po.id, connection)
    percentage = 0
    for x in prog.data:
        percentage += (x / (po.amount * 1.0)) * (1.0 / 6.0)
    po.progress = percentage * 100


def fetch_all_pos(connection):
    cursor = connection.cursor()
    cursor.execute(queries.get_all_pos())
    pos = []
    for row in cursor.fetchall():
        pos.append(PurchaseOrder(row))
    return pos


def fetch_progress(po_id, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT prepped, thrown, debatted, trimmed, assembled, polished FROM public.purchaseorders WHERE id = %s" % po_id)
    return Progress(cursor.fetchone())


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flask.flash(u"Error in %s field - %s" % (field, error), 'error')


def flash_message(msg, category='info'):
    flask.flash(msg, category)


def calc_days_left_for_task(task):
    day = datetime.datetime.today().weekday()

    tasks = [[1, 5, 4, 3, 2],
             [2, 1, 5, 4, 3],
             [3, 2, 1, 5, 4],
             [4, 3, 2, 1, 5],
             [5, 4, 3, 2, 1],
             [2, 1, 5, 4, 3]]

    return tasks[task][day]


def calc_numbers(pos, have, leftover, task, total_pos):
    results = [0]*len(total_pos)
    for i, po in enumerate(pos):
        total = po[8]
        adn = (total - have[i]) / calc_days_left_for_task(task)
        results[get_index(total_pos, po[10])] = adn + leftover[i]
    return results


def get_index(pos, po_id):
    for i, po in enumerate(pos):
        if po[1] == po_id:
            return i


def get_debat_numbers(connection, total_pos):
    cursor = connection.cursor()
    cursor.execute("SELECT * from public.debat")
    pos = cursor.fetchall()
    results = [0]*len(total_pos)
    for po in pos:
        results[get_index(total_pos, po[10])] = po[1]
        cursor.execute("DELETE FROM public.debat WHERE id = %s" % po[0])
    connection.commit()
    return results


def calc_todo(pos, connection):
    cursor = connection.cursor()

    # PREP
    cursor.execute(queries.get_pos_for_prepping_this_week())
    prep_pos = cursor.fetchall()
    ids = [x[10] for x in prep_pos]
    cursor.execute(queries.get_have_for_pos(ids, "prep"))
    prep_have = [x[0] for x in cursor.fetchall()]
    cursor.execute(queries.get_leftover_for_pos(ids, "prep"))
    prep_leftover = [x[0] for x in cursor.fetchall()]

    # THROW
    cursor.execute(queries.get_pos_for_throwing_this_week())
    throw_pos = cursor.fetchall()
    ids = [x[10] for x in throw_pos]
    cursor.execute(queries.get_have_for_pos(ids, "throw"))
    throw_have = [x[0] for x in cursor.fetchall()]
    cursor.execute(queries.get_leftover_for_pos(ids, "throw"))
    throw_leftover = [x[0] for x in cursor.fetchall()]

    # DEBAT
    debat_numbers = get_debat_numbers(connection, pos)

    # TRIM
    cursor.execute(queries.get_pos_for_trimming_this_week())
    trim_pos = cursor.fetchall()
    ids = [x[10] for x in trim_pos]
    cursor.execute(queries.get_have_for_pos(ids, "trim"))
    trim_have = [x[0] for x in cursor.fetchall()]
    cursor.execute(queries.get_leftover_for_pos(ids, "trim"))
    trim_leftover = [x[0] for x in cursor.fetchall()]

    # ASSEMBLY
    cursor.execute(queries.get_pos_for_assembling_this_week())
    assemble_pos = cursor.fetchall()
    ids = [x[10] for x in assemble_pos]
    cursor.execute(queries.get_have_for_pos(ids, "assemble"))
    assemble_have = [x[0] for x in cursor.fetchall()]
    cursor.execute(queries.get_leftover_for_pos(ids, "assemble"))
    assemble_leftover = [x[0] for x in cursor.fetchall()]

    # POLISH
    cursor.execute(queries.get_pos_for_polishing_this_week())
    polish_pos = cursor.fetchall()
    ids = [x[10] for x in polish_pos]
    cursor.execute(queries.get_have_for_pos(ids, "polish"))
    polish_have = [x[0] for x in cursor.fetchall()]
    cursor.execute(queries.get_leftover_for_pos(ids, "polish"))
    polish_leftover = [x[0] for x in cursor.fetchall()]

    return {
        "prep": calc_numbers(prep_pos, prep_have, prep_leftover, 0, pos),
        "throw": calc_numbers(throw_pos, throw_have, throw_leftover, 1, pos),
        "debat": debat_numbers,  # calc_numbers(debat_pos, debat_have, debat_leftover, 2),
        "trim": calc_numbers(trim_pos, trim_have, trim_leftover, 3, pos),
        "assemble": calc_numbers(assemble_pos, assemble_have, assemble_leftover, 4, pos),
        "polish": calc_numbers(polish_pos, polish_have, polish_leftover, 5, pos),
        "handles": calc_numbers(assemble_pos, assemble_have, assemble_leftover, 4, pos),
        "stamps": calc_numbers(assemble_pos, assemble_have, assemble_leftover, 4, pos)
    }
