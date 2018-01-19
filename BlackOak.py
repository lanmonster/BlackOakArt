# TODO: when i work API
# 0 -> -

import flask
import psycopg2
import json
import forms  # mine (forms.py)
import utils  # mine (utils.py)
import queries  # mine (queries.py)


app = flask.Flask(__name__)


@app.route('/')
def home_page():
    data = {}
    rules = [x for x in app.url_map._rules if not x.rule.startswith('/static/') and not x.rule == '/' and not x.rule == '/temp']
    for rule in rules:
        data[rule.endpoint] = rule.endpoint.replace('_', ' ').replace('0', '-')
    return flask.render_template('main.html', data=data)


@app.route('/po/viewall')
def View_all_POs():  # TODO sortable? fix percent complete
    pos = utils.fetch_all_pos(connection)
    for po in pos:
        utils.calculate_percent_complete(po, connection)

    return flask.render_template('all.html', pos=pos)


@app.route('/po/<int:po_id>')
def View_PO_by_ID(po_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM public.purchaseorders WHERE id = %d" % po_id)
    return flask.render_template('po.html', po=cursor.fetchone())


@app.route('/po/add', methods=['GET', 'POST'])
def Add_a_new_PO():
    form = forms.PurchaseOrderForm(flask.request.form)
    if flask.request.method == 'POST':
        if form.validate():
            data = flask.request.form
            utils.add_po(data, connection)
            connection.commit()
            utils.flash_message("PO added!", category='success')
        else:
            utils.flash_errors(form)

    return flask.render_template('add.html', form=form)


@app.route('/po/update', methods=['GET', 'POST'])
def Update_a_PO():
    form = forms.UpdatePurchaseOrderForm(flask.request.form)
    if flask.request.method == 'POST':
        if form.validate():
            data = flask.request.form
            cursor = connection.cursor()
            cursor.execute(queries.update_po(data))
            connection.commit()
            utils.flash_message("PO updated!", category='success')
        else:
            utils.flash_errors(form)

    return flask.render_template('update.html', form=form)


@app.route('/po/delete', methods=['GET', 'POST'])
def Delete_a_PO():
    form = forms.DeletePurchaseOrderForm(flask.request.form)
    if flask.request.method == 'POST':
        po_id = flask.request.form['po_id']
        utils.delete_po(po_id, connection)

    return flask.render_template('delete.html', form=form)


@app.route('/end-of-day')
def Enter_end0of0day_numbers(data=None):
    cursor = connection.cursor()
    cursor.execute(queries.get_pos_this_week())
    pos = cursor.fetchall()
    if data:
        for po in data:
            # update progress
            cursor.execute(queries.update_progress(po))
            connection.commit()

            # update have
            utils.update_haves(po, connection)

            # update debat numbers
            utils.update_debat_numbers(po, connection)

            # update leftovers
            utils.update_leftovers(po, connection)

        utils.flash_message("Numbers entered!", category='success')

    return flask.render_template('end-of-day.html', pos=pos, form=forms.NewForm(), length=len(pos))


@app.route('/temp', methods=['POST'])
def temp():
    Enter_end0of0day_numbers(json.loads(flask.request.get_data()))
    return ''


@app.route('/todo')
def To0Do():
    cursor = connection.cursor()
    cursor.execute(queries.get_pos_this_week())
    pos = cursor.fetchall()
    return flask.render_template('todo.html', pos=pos, todos=utils.calc_todo(pos, connection))


if __name__ == '__main__':
    connection = psycopg2.connect(host='localhost', user='jonathanmartin', password='12', database='jonathanmartin')
    app.secret_key = 'black_oak'
    app.run(host=utils.get_ip_address(), debug=True)
