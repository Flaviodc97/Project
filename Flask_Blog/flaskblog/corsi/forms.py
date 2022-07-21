from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField, \
    DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class CorsoForm(FlaskForm):
    titolo_corso = StringField('Titolo corso',
                               validators=[DataRequired()])
    data_inizio_corso = DateField('Data inizio corso',
                                  validators=[DataRequired()])
    data_fine_corso = DateField('Data fine corso',
                                validators=[DataRequired()])

    n_partecipanti = IntegerField('Numero Partecipanti')

    descrizione = TextAreaField('Descrizione')

    documentazione = FileField('Documentazione')

    descrizione_documentazione = StringField('Descrizione Documentazione')

    responsabile = SelectField('Responsabile', choices=[])

    submit_button = SubmitField('Invia')
