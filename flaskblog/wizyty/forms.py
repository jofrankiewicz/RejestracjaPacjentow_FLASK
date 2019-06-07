from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class WizytaForm(FlaskForm):
    kategoria = StringField('Dziedzina medycyny', validators=[DataRequired()])
    nazwa_wizyty = TextAreaField('Szczegóły wizyty', validators=[DataRequired()])
    submit = SubmitField('Dodaj wizytę')
