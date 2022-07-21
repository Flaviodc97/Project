from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField, \
    DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class NegoziazioneTrasferimentoTecnologicoForm(FlaskForm):
    tipologia = TextAreaField('Tipologia',
                       validators=[DataRequired()])
    controparte = StringField('Controparte',
                          validators=[DataRequired()])
    nazione_controparte = StringField('Nazione Controparte',
                     validators=[DataRequired()])
    documentazione = FileField('Documentazione')

    descrizione_documentazione= StringField('Descrizione Documentazione')

    responsabile = SelectField('Responsabile', choices=[])


    submit_button = SubmitField('Invia')
