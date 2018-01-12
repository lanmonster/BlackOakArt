import math


def get_all_from(table_name):
    return "SELECT * FROM public.\"%s\"" % table_name


def get_progress(po_id):
    return '''SELECT prep, throw, debat, \"trim\", assemble, polish
              FROM public.\"Progress\"
              WHERE public.\"Progress\".id = %s''' % po_id


def add_to_progress():
    return '''INSERT INTO public."Progress"(id)
              SELECT id FROM public."PurchaseOrders"
              WHERE id NOT IN (SELECT id FROM public."Progress")'''


def get_pos_this_week():
    return '''SELECT adjusted_amount, clay_type
              FROM public.\"PurchaseOrders\"
              WHERE delivery_date - CURRENT_DATE <= 15
              AND delivery_date - CURRENT_DATE >= 11'''


def update_leftover(data, adn):
    update_query = "UPDATE public.\"Leftover\" SET "
    for key, val in [(x, y) for x, y in data.items() if x != 'po_id']:
        update_query += "\"%s\" = %s, " % (key, (adn - int(val)))
    update_query = update_query[:-2]
    return update_query


def update_progress(data):
    update_query = 'UPDATE public."Progress" SET '
    for (key, val) in [(x, y) for x, y in data.items() if x != 'po_id' and x != 'stamps' and x != 'handles']:
        update_query += '%s = %s + %s, ' % (key, key, data[key])
    update_query = update_query[:-2] + ' WHERE public."Progress".id = %s;' % data['po_id']
    return update_query


def update_debat_number(number):
    return 'UPDATE public."Debat" SET debat = %s' % number


def delete_from(table_name, po_id):
    return "DELETE FROM public.\"%s\" WHERE id=%s" % (table_name, po_id)


def add(data):
    query = 'INSERT INTO public.\"PurchaseOrders\" ('
    for key in data.keys():
        query += "\"%s\", " % key
    query += "adjusted_amount) VALUES ("
    for val in data.values():
        query += "'%s', " % val
    adjusted_amt = math.ceil(int(data['amount']) + (int(data['amount']) * float(data['buffer'])))
    query += "%d);" % adjusted_amt
    return query


def update_po(data):
    query = 'UPDATE public.\"PurchaseOrders\" SET '
    for (key, val) in data.items():
        if key != 'po_id' and val != '':
            query += "%s = '%s', " % (key, val.lower())
    query = query[:-2] + " WHERE public.\"PurchaseOrders\".id = %s;" % data['po_id']
    return query


def join():
    return '''SELECT *
              FROM public.\"Progress\" JOIN public.\"PurchaseOrders\"
              ON public.\"Progress\".id = public.\"PurchaseOrders\".id'''