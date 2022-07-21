from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField, \
    DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class NewPersonaleForm(FlaskForm):
    nome = StringField('Nome',
                       validators=[DataRequired()])
    cognome = StringField('Cognome',
                          validators=[DataRequired()])

    cf = StringField('Codice Fiscale',
                     validators=[DataRequired()])
    data_di_nascita = DateField('Data di Nascita')

    qualifica = TextAreaField('Qualifica')

    struttura = StringField('Struttura')

    competenza_specifica = TextAreaField('Competenza Specifica')

    tipologia_contratto = StringField('Tipologia Contratto',
                                      validators=[DataRequired()])

    altro = TextAreaField('Altro')

    data_inizio_rapporto = DateField('Data inizio rapporto')

    descrizione = TextAreaField('Descrizione')

    documento = FileField('Documento')

    descrizione_documento = TextAreaField('Descrizione Documento')

    tipo = SelectField('Tipologia', choices=[ ('False', 'Personale di Supporto'), ('True', 'Responsabile')])

    submit_button = SubmitField('Invia')
