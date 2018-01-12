import flask
import socket

from PurchaseOrder import PurchaseOrder  # mine (PurchaseOrder.py)
from Progress import Progress  # mine (Progress.py)
import queries


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def calculate_percent_complete(po, connection):
    # sum of all (amt through step / total) * (1/steps) for steps
    prog = fetch_progress(po.id, connection)
    percentage = 0
    for x in prog.data:
        percentage += (x / (po.amount * 1.0)) * (1.0 / 6.0)
    po.progress = percentage * 100


def fetch_all_pos(connection):
    cursor = connection.cursor()
    cursor.execute(queries.get_all_from("PurchaseOrders"))
    pos = []
    for row in cursor.fetchall():
        pos.append(PurchaseOrder(row))

    return pos


def fetch_progress(po_id, connection):
    cursor = connection.cursor()
    cursor.execute(queries.get_progress(po_id))
    return Progress(cursor.fetchone())


def populate_progress_table(connection):
    cursor = connection.cursor()
    cursor.execute(queries.add_to_progress())
    connection.commit()


def need(adn, have):
    return adn - have + adn


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flask.flash(u"Error in %s field - %s" % (field, error), 'error')


def flash_message(msg, category='info'):
    flask.flash(msg, category)
