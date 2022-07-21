from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField, \
    DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class SupportoLicensingForm(FlaskForm):
    oggetto_licensing = TextAreaField('Oggetto Licensing',
                       validators=[DataRequired()])
    ente_controparte = StringField('Ente Controparte')

    nazione_controparte = StringField('Nazione Controparte')

    descrizione_controparte = TextAreaField('Descrizione Controparte')

    eventuali_entrate_correlate = IntegerField('Eventuali Entrate Correlate')

    documentazione = FileField('Documentazione')

    descrizione_documentazione= TextAreaField('Descrizione Documentazione')

    responsabile = SelectField('Responsabile', choices=[])


    submit_button = SubmitField('Invia')
