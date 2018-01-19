import math
import utils  # mine


def get_all_pos():
    return "SELECT id, company, item, clay_type, glaze_color, amount, buffer, adjusted_amount, description, miscellaneous, delivery_date " \
           "FROM public.purchaseorders"


def get_pos_this_week():
    return '''SELECT company, id, item
              FROM public.PurchaseOrders
              WHERE delivery_date - CURRENT_DATE <= 28
              AND delivery_date - CURRENT_DATE >= 14'''


def get_pos_for_prepping_this_week():
    return '''SELECT * FROM public.PurchaseOrders
                  WHERE delivery_date - CURRENT_DATE <= 28
                  AND delivery_date - CURRENT_DATE >= 22'''


def get_pos_for_throwing_this_week():
    return '''SELECT * FROM public.PurchaseOrders
                  WHERE delivery_date - CURRENT_DATE <= 27
                  AND delivery_date - CURRENT_DATE >= 21'''


def get_pos_for_debatting_this_week():
    return '''SELECT * FROM public.PurchaseOrders
                  WHERE delivery_date - CURRENT_DATE <= 26
                  AND delivery_date - CURRENT_DATE >= 20'''


def get_pos_for_trimming_this_week():
    return '''SELECT * FROM public.PurchaseOrders
                  WHERE delivery_date - CURRENT_DATE <= 25
                  AND delivery_date - CURRENT_DATE >= 19'''


def get_pos_for_assembling_this_week():
    return '''SELECT * FROM public.PurchaseOrders
                  WHERE delivery_date - CURRENT_DATE <= 22
                  AND delivery_date - CURRENT_DATE >= 18'''


def get_pos_for_polishing_this_week():
    return '''SELECT * FROM public.PurchaseOrders
                  WHERE delivery_date - CURRENT_DATE <= 20
                  AND delivery_date - CURRENT_DATE >= 14'''


def get_have_for_pos(pos, task):
    query = "SELECT amount FROM have.%s WHERE id = " % task
    for po in pos:
        query += str(po) + " OR id = "
    return query[:-9]


def get_leftover_for_pos(pos, task):
    query = "SELECT amount FROM leftover.%s WHERE id = " % task
    for po in pos:
        query += str(po) + " OR id = "
    return query[:-9]


def delete_from(table_name, po_id):
    return "DELETE FROM public.\"%s\" WHERE id=%s" % (table_name, po_id)


def add(data):
    query = 'INSERT INTO public.PurchaseOrders ('
    for key in data.keys():
        query += "\"%s\", " % key
    query += "adjusted_amount) VALUES ("
    for val in data.values():
        query += "'%s', " % val
    adjusted_amt = math.ceil(int(data['amount']) + (int(data['amount']) * float(data['buffer'])))
    query += "%d);" % adjusted_amt
    return query


def update_po(data):
    query = 'UPDATE public.PurchaseOrders SET '
    for (key, val) in data.items():
        if key != 'po_id' and val != '':
            query += "%s = '%s', " % (key, val.lower())
    query = query[:-2] + " WHERE public.PurchaseOrders.id = %s;" % data['po_id']
    return query


def insert_into_have(task, po_id, item, clay_type, amount):
    query = "INSERT INTO have.%s (id, item, clay_type, amount)" % task
    query += "VALUES (%d, \'%s', \'%s\', %d)" % (po_id, item, clay_type, amount)
    return query


def insert_into_leftover(task, po_id, item, clay_type, amount):
    query = "INSERT INTO leftover.%s (id, item, clay_type, amount)" % task
    query += "VALUES (%d, \'%s', \'%s\', %d)" % (po_id, item, clay_type, amount)
    return query


def update_progress(po):
    query = "UPDATE public.purchaseorders SET "
    nums = [x for x in po['nums']]
    nums.pop()
    for i, num in enumerate(nums):
        query += "%s = %s, " % (utils.task_to_end_of_day_format(utils.tasks[i]), num)
    return query[:-2] + " WHERE id = %s" % po['id']


def update_leftover(task, amount, po_id, adn):
    return "UPDATE leftover.%s SET amount = %d WHERE id = %s" % (task, adn - int(amount), po_id)


def update_have(task, amount, po_id, adn):
    return "UPDATE have.%s SET amount = %d WHERE id = %s" % (task, adn - int(amount), po_id)


def update_debat_number(po_id, amount):
    return "UPDATE public.debat SET id = %s, amount = %s" % (po_id, str(amount))

