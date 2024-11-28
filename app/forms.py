from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ChargeForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired(), Length(max=128)])
    amount = DecimalField('Montant', validators=[DataRequired(), NumberRange(min=0)])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Ajouter Charge')

class RevenueForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired(), Length(max=128)])
    amount = DecimalField('Montant', validators=[DataRequired(), NumberRange(min=0)])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Ajouter Revenu')

class DeleteForm(FlaskForm):
    submit = SubmitField('Supprimer')
