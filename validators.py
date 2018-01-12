import re

from wtforms.validators import ValidationError


def company_validator(form, field):
    if len(field.data) < 1:
        raise ValidationError("Company Name must be at least 1 character.")


def item_validator(form, field):
    if bool(re.search(r'\d', field.data)):
        raise ValidationError("Item cannot contain any numbers.")

    if len(field.data) < 1:
        raise ValidationError("Item must be at least 1 character.")


def clay_type_validator(form, field):
    colors = ['red', 'rojo', 'white', 'blanco']
    if field.data.lower().encode('ascii') not in colors:
        raise ValidationError("Clay Type must be from this list: [%s]" % ', '.join(colors))


def glaze_color_validator(form, field):
    colors = ['white', 'black', 'gather blue', 'sky blue', 'super blue', 'green', 'golden brown', 'pink', 'gray',
              'grey']
    if field.data not in colors:
        raise ValidationError("Glaze Color must be from this list: [%s]" % ', '.join(colors))


def amount_validator(form, field):
    if int(field.data) <= 0:
        raise ValidationError("Amount must be an integer greater than 0, you typed: %s" % field.data)


def buffer_validator(form, field):
    if not float(field.data) or float(field.data) < 0 or float(field.data) > 1:
        raise ValidationError("Buffer must be a decimal between 0 and 1")


# TODO
def id_validator(form, field):
    # check against pos in db
    pass


def end_of_day_validator(form, field):
    if not int(field.data):
        raise ValidationError("Value must be an integer")

    if int(field.data) < 0:
        raise ValidationError("Value must be at least 0")
