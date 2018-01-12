import wtforms
from wtforms.validators import InputRequired, Optional
import validators  # mine (validators.py)


class DeletePurchaseOrderForm(wtforms.Form):
    po_id = wtforms.IntegerField("PO #: ", [InputRequired(), validators.id_validator])


class UpdatePurchaseOrderForm(wtforms.Form):
    po_id = wtforms.IntegerField('PO #: ', [InputRequired(), validators.id_validator])
    company = wtforms.StringField('Company: ', [Optional(), validators.company_validator])
    item = wtforms.StringField('Item: ', [Optional(), validators.item_validator])
    clay_type = wtforms.StringField('Clay Type: ', [InputRequired(), validators.clay_type_validator])
    glaze_color = wtforms.StringField('Glaze Color: ', [Optional(), validators.glaze_color_validator])
    amount = wtforms.IntegerField('Amount: ', [Optional(), validators.amount_validator])
    buffer = wtforms.DecimalField('Buffer: ', [Optional(), validators.buffer_validator])
    description = wtforms.TextAreaField('Description: ', [Optional()])
    miscellaneous = wtforms.TextAreaField('Miscellaneous Info: ')
    delivery_date = wtforms.DateField('Delivery Date (YYYY/MM/DD): ', format='%Y/%m/%d', validators=([Optional()]))


class PurchaseOrderForm(wtforms.Form):
    company = wtforms.StringField('Company: ', [InputRequired(), validators.company_validator])
    item = wtforms.StringField('Item: ', [InputRequired(), validators.item_validator])
    clay_type = wtforms.StringField('Clay Type: ', [InputRequired(), validators.clay_type_validator])
    glaze_color = wtforms.StringField('Glaze Color: ', [InputRequired(), validators.glaze_color_validator])
    amount = wtforms.IntegerField('Amount: ', [InputRequired(), validators.amount_validator])
    buffer = wtforms.DecimalField('Buffer: ', [InputRequired(), validators.buffer_validator])
    description = wtforms.TextAreaField('Description: ', [InputRequired()])
    miscellaneous = wtforms.TextAreaField('Miscellaneous Info: ')
    delivery_date = wtforms.DateField('Delivery Date (YYYY/MM/DD): ', format='%Y/%m/%d')


class EndOfDayForm(wtforms.Form):
    po_id = wtforms.IntegerField('PO #: ', [InputRequired(), validators.id_validator])
    prep = wtforms.IntegerField('prepped: ', [InputRequired(), validators.end_of_day_validator])
    throw = wtforms.IntegerField('thrown: ', [InputRequired(), validators.end_of_day_validator])
    debat = wtforms.IntegerField('debatted: ', [InputRequired(), validators.end_of_day_validator])
    trim = wtforms.IntegerField('trimmed: ', [InputRequired(), validators.end_of_day_validator])
    assemble = wtforms.IntegerField('assembled: ', [InputRequired(), validators.end_of_day_validator])
    polish = wtforms.IntegerField('polished: ', [InputRequired(), validators.end_of_day_validator])
    stamps = wtforms.IntegerField('stamps made: ', [InputRequired(), validators.end_of_day_validator])
    handles = wtforms.IntegerField('handles made: ', [InputRequired(), validators.end_of_day_validator])
