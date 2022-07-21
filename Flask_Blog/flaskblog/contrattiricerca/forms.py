from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField, \
    DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class ContrattoRicercaForm(FlaskForm):
    denominazione_industria = StringField('Denominazione Industria',
                       validators=[DataRequired()])
    contratto = FileField('Contratto')

    descrizione_contratto = TextAreaField('Descrizione Contratto',
                     validators=[DataRequired()])
    anno_sottoscrizione_collaborazione = IntegerField('Anno Sottoscrizione Collaborazione')

    durata_collaborazione = IntegerField('Durata Collaborazione')

    oggetto_collaborazione = TextAreaField('Oggetto della Collaborazione')

    valore_economico_contratto = IntegerField('Valore economico del contratto')

    responsabile = SelectField('Responsabile', choices=[])

    submit_button = SubmitField('Invia')
