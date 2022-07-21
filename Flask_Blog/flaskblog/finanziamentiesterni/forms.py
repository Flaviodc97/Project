from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField, \
    DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class FinanziamentoEsternoForm(FlaskForm):
    tipologia = TextAreaField('Tipologia',
                       validators=[DataRequired()])
    ente_controparte = StringField('Controparte',
                          validators=[DataRequired()])
    nazione_ente_controparte = StringField('Nazione Controparte',
                     validators=[DataRequired()])

    eventuali_entrate_correlate = IntegerField('Eventuali entrate correlate')

    documentazione = FileField('Documentazione')

    descrizione_documentazione= StringField('Descrizione Documentazione')

    responsabile = SelectField('Responsabile', choices=[])


    submit_button = SubmitField('Invia')
