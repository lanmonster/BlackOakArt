from flask_table import Table, Col
from flask import url_for


class SortableTable(Table):
    id = Col('ID')
    company = Col('Company')
    item = Col('Item')
    clay_type = Col('Clay Type')
    glaze_color = Col('Glaze Color')
    amount = Col('Amount')
    buffer = Col('Buffer')
    adjusted_amount = Col('Adjusted Amount')
    description = Col('Description')
    miscellaneous = Col('Miscellaneous')
    percent_complete = Col('Percent Complete')
    delivery_date = Col('Delivery Date')
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('index', sort=col_key, direction=direction)


