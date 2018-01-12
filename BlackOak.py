# TODO: when i work API
# 0 -> -

import flask
import psycopg2
import forms  # mine (forms.py)
import utils  # mine (utils.py)
import queries  # mine (queries.py)
import SortableTable

app = flask.Flask(__name__)
average_daily_need = 0


@app.route('/')
def home_page():
    data = {}
    for rule in [x for x in app.url_map._rules if not x.rule.startswith('/static/') and not x.rule == '/']:
        data[rule.endpoint] = rule.endpoint.replace('_', ' ').replace('0', '-')
    return flask.render_template('main.html', data=data)


@app.route('/po/viewall')
def View_all_POs():
    pos = utils.fetch_all_pos(connection)
    for po in pos:
        utils.calculate_percent_complete(po, connection)

    sort = flask.request.args.get('sort', 'id')
    reverse = (flask.request.args.get('direction', 'asc') == 'desc')
    table = SortableTable.SortableTable(sorted(pos, sort, reverse=reverse),
                                        sort_by=sort,
                                        sort_reverse=reverse)

    return table.__html__()  # flask.render_template('all.html', pos=pos)


@app.route('/po/add', methods=['GET', 'POST'])
def Add_a_new_PO():
    form = forms.PurchaseOrderForm(flask.request.form)
    if flask.request.method == 'POST':
        if form.validate():
            data = flask.request.form
            cursor = connection.cursor()
            cursor.execute(queries.add(data))
            connection.commit()
            utils.populate_progress_table(connection)
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
        cursor = connection.cursor()
        cursor.execute(queries.delete_from("Progress", po_id))
        if cursor.rowcount > 0:
            cursor.execute(queries.delete_from("PurchaseOrders", po_id))
            connection.commit()
            utils.flash_message("PO deleted!", category='success')
        else:
            utils.flash_message("That id does not exist! Try another.", category='error')
    return flask.render_template('delete.html', form=form)


@app.route('/end-of-day', methods=['GET', 'POST'])
def Enter_end0of0day_numbers():
    global average_daily_need
    form = forms.EndOfDayForm(flask.request.form)
    if flask.request.method == 'POST':
        cursor = connection.cursor()
        cursor.execute(queries.update_progress(flask.request.form))
        cursor.execute(queries.update_leftover(flask.request.form, average_daily_need))
        cursor.execute(queries.update_debat_number(flask.request.form['throw']))
        connection.commit()
        utils.flash_message("Numbers entered!", category='success')
    return flask.render_template('end-of-day.html', form=form)


@app.route('/todo')
def To0Do():  # Focus your efforts here
    cursor = connection.cursor()

    # # get what we have
    # cursor.execute(queries.get_all_from("Have"))
    # have = cursor.fetchall()[0]
    # #        0   , 1    , 2    , 3   , 4     , 5      , 6
    # # white (prep, throw, debat, trim, polish, handles, stamps)
    #
    # #        7   , 8    , 9    , 10  , 11    , 12     , 13
    # # red   (prep, throw, debat, trim, polish, handles, stamps)
    #
    # # get all POs for this week
    # cursor.execute(queries.get_pos_this_week())
    # items = cursor.fetchall()
    #
    # white = red = 0
    # for item in items:
    #     if item[1] == 'white' or item[1] == 'blanco':
    #         white += item[0]
    #     if item[1] == 'red' or item[1] == 'rojo':
    #         red += item[0]
    #
    # rADN = red / 5
    # wADN = white / 5
    #
    # data = {
    #     "prep": {
    #         "white": utils.need(wADN, have[0]),
    #         "red": utils.need(rADN, have[7])
    #     },
    #     "throw": {  # TODO
    #         "white": 0,
    #         "red": 0
    #     },
    #     "debat": {  # TODO: throw number from yesterday
    #         "white": 0,
    #         "red": 0
    #     },
    #     "trim": {
    #         "white": utils.need(wADN, have[3]),
    #         "red": utils.need(rADN, have[10])
    #     },
    #     "assemble": {
    #         "white": wADN,
    #         "red": rADN
    #     },
    #     "polish": {
    #         "white": utils.need(wADN, have[4]),
    #         "red": utils.need(rADN, have[11])
    #     },
    #     "handles": {
    #         "white": utils.need(wADN, have[5]),
    #         "red": utils.need(rADN, have[12])
    #     },
    #     "stamps": {
    #         "white": utils.need(wADN, have[6]),
    #         "red": utils.need(rADN, have[13])
    #     }
    # }

    pos = utils.fetch_all_pos(connection)

    todos = utils.calc_todo(pos)

    return flask.render_template('todo.html', pos=pos, todos=todos)


if __name__ == '__main__':
    connection = psycopg2.connect(host='localhost', user='postgres', password='12', database='postgres')
    app.secret_key = 'black_oak'
    app.run(host=utils.get_ip_address(), debug=True)
