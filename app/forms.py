from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

class ChargeForm(FlaskForm):
    description = StringField('Nom', validators=[DataRequired(), Length(max=128)])
    amount = DecimalField('Montant', validators=[DataRequired(), NumberRange(min=0)])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Ajouter Charge')

class RevenueForm(FlaskForm):
    description = StringField('Nom', validators=[DataRequired(), Length(max=128)])
    amount = DecimalField('Montant', validators=[DataRequired(), NumberRange(min=0)])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    person_id = SelectField('Personne', coerce=int)  # Champ pour sélectionner une personne
    submit = SubmitField('Ajouter Revenu')

class DeleteForm(FlaskForm):
    submit = SubmitField('Supprimer')

class LoginForm(FlaskForm):
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class AllocationForm(FlaskForm):
    person_id = SelectField('Personne', coerce=int, validators=[DataRequired()])  # Sélectionner une personne
    allocation_percentage = DecimalField('Pourcentage Alloué', validators=[DataRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField('Mettre à jour l\'allocation')

class PersonForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired(), Length(max=64)])
    allocation_percentage = DecimalField(
        'Pourcentage Alloué', validators=[DataRequired(), NumberRange(min=0, max=100)]
    )
    submit = SubmitField('Ajouter')
