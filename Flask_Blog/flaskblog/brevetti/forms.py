from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField, \
    DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from flaskblog.models import PersonaleQualificato



class BrevettoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    codice = IntegerField('Codice',
                          validators=[DataRequired()])
    nazione_validita = StringField('Nazione validita',
                     validators=[DataRequired()])
    descrizione = TextAreaField('Descrizione')

    anno_presentazione = IntegerField('Anno Presentazione')

    anno_assegnazione = IntegerField('Anno di Assegnazione')

    certificato = FileField('Certificato')

    responsabile = SelectField('Responsabile', choices=[])

    submit_button = SubmitField('Invia')
