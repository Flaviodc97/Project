from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField, \
    DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import Corso


class IncubatoreAccelleratoreImpresaForm(FlaskForm):

    tipologia = StringField('Tipologia',
                       validators=[DataRequired()])
    descrizione = TextAreaField('Descrizione',
                          validators=[DataRequired()])

    documentazione = FileField('Documentazione')

    descrizione_documentazione= StringField('Descrizione Documentazione')

    responsabile = SelectField('Responsabile', choices=[])

    submit_button = SubmitField('Invia')
