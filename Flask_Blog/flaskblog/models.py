from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='dafault.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}' )"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Ente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cf_ente = db.Column(db.String(20), nullable=False)
    nome_ente = db.Column(db.String(1000), nullable=False)
    descrizione_ente = db.Column(db.Text, nullable=False)
    legale = db.Column(db.String(1000), nullable=False)
    n_personale = db.Column(db.Integer, nullable=False)
    tipologie_expertise_personale = db.Column(db.Text, nullable=False)
    personale = db.relationship('PersonaleQualificato', backref='author', lazy=True)
    brevetti = db.relationship('Brevetto', backref='author', lazy=True)
    contratti_ricerca = db.relationship('ContrattoRicerca', backref='author', lazy=True)
    negoziazioni_trasferimento_tecnologico = db.relationship('NegoziazioneTrasferimentoTecnologico', backref='author',
                                                             lazy=True)
    scouting_e_assistenza = db.relationship('ScoutingeAssistenza', backref='author', lazy=True)
    finanziamenti_esterni = db.relationship('FinanziamentoEsterni', backref='author', lazy=True)
    supporto_licensing = db.relationship('SupportoLicensing', backref='author', lazy=True)
    corsi = db.relationship('Corso', backref='author', lazy=True)
    incubatori = db.relationship('IncubatoriAccelleratoriImpresa', backref='author', lazy=True)

    def __repr__(self):
        return f"Ente('{self.nome_ente}', '{self.descrizione_ente}')"


class PersonaleQualificato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(1000), nullable=False)
    cognome = db.Column(db.String(1000), nullable=False)
    cf = db.Column(db.String(16), nullable=False)
    data_di_nascita = db.Column(db.Date, nullable=True)
    qualifica = db.Column(db.Text, nullable=False, default='Nessuna Qualifica')
    struttura = db.Column(db.String(1000), nullable=False, default='Nessuna Struttura')
    competenza_specifica = db.Column(db.Text, nullable=False, default='Nessuna Competenza')
    tipologia_contratto = db.Column(db.String(1000), nullable=False)
    altro = db.Column(db.Text, nullable=True)
    data_inizio_rapporto = db.Column(db.Date, nullable=True)
    descrizione = db.Column(db.Text, nullable=False, default='Nessuna Descrizione')
    documento = db.Column(db.String(1000), nullable=False)
    descrizione_documento = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.Boolean, nullable=False)
    ente = db.Column(db.Integer, db.ForeignKey('ente.id'), nullable=False)
    brevetti = db.relationship('Brevetto', backref='res', lazy=True)
    contratti_ricerca = db.relationship('ContrattoRicerca', backref='resp', lazy=True)
    negoziazioni_trasferimento_tecnologico = db.relationship('NegoziazioneTrasferimentoTecnologico', backref='resp',
                                                             lazy=True)
    scouting_e_assistenza = db.relationship('ScoutingeAssistenza', backref='resp', lazy=True)
    finanziamenti_esterni = db.relationship('FinanziamentoEsterni', backref='resp', lazy=True)
    supporto_licensing = db.relationship('SupportoLicensing', backref='resp', lazy=True)
    corsi = db.relationship('Corso', backref='resp', lazy=True)
    incubatori_accelleratori_impresa = db.relationship('IncubatoriAccelleratoriImpresa', backref='resp', lazy=True)

    def __repr__(self):
        return f"Personale_Qualificato('{self.nome}', '{self.cognome}')"

    def personale_query(self):
        return PersonaleQualificato.query


class Brevetto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(1000), nullable=False)
    codice = db.Column(db.Integer, nullable=False)
    nazione_validita = db.Column(db.String(1000), nullable=False)
    descrizione = db.Column(db.Text, nullable=False, default='Nessuna Descrizione')
    anno_presentazione = db.Column(db.Integer, nullable=False)
    anno_assegnazione = db.Column(db.Integer, nullable=False)
    certificato = db.Column(db.String(1000), nullable=False)
    ente = db.Column(db.Integer, db.ForeignKey('ente.id'), nullable=False)
    responsabile = db.Column(db.Integer, db.ForeignKey('personale_qualificato.id'), nullable=False)

    # personale_supporto = db.Column(db.Integer, db.ForeignKey('personalequalificato.id'), nullable=False)

    def __repr__(self):
        return f"Brevetto('{self.nome}', '{self.descrizione}')"


class ContrattoRicerca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    denominazione_industria = db.Column(db.String(1000), nullable=False)
    contratto = db.Column(db.String(1000), nullable=False)
    descrizione_contratto = db.Column(db.Text, nullable=False, default='Nessuna Descrizione')
    anno_sottoscrizione_collaborazione = db.Column(db.Integer, nullable=False)
    durata_collaborazione = db.Column(db.Integer, nullable=False)
    oggetto_collaborazione = db.Column(db.Text, nullable=False)
    valore_economico_contratto = db.Column(db.Integer, nullable=False)
    ente = db.Column(db.Integer, db.ForeignKey('ente.id'), nullable=False)
    responsabile = db.Column(db.Integer, db.ForeignKey('personale_qualificato.id'), nullable=False)

    # personale_supporto = db.Column(db.Integer, db.ForeignKey('personalequalificato.id'), nullable=False)

    def __repr__(self):
        return f"Contratto_Ricerca('{self.descrizione_contratto}', '{self.valore_economico_contratto}')"


class NegoziazioneTrasferimentoTecnologico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipologia = db.Column(db.Text, nullable=False)
    controparte = db.Column(db.String(1000), nullable=False)
    nazione_controparte = db.Column(db.String(1000), nullable=False)
    documentazione = db.Column(db.String(1000), nullable=False)
    descrizione_documentazione = db.Column(db.Text)
    ente = db.Column(db.Integer, db.ForeignKey('ente.id'), nullable=False)
    responsabile = db.Column(db.Integer, db.ForeignKey('personale_qualificato.id'), nullable=False)

    # personale_supporto = db.Column(db.Integer, db.ForeignKey('personalequalificato.id'), nullable=False)

    def __repr__(self):
        return f"('Negoziazione_Trasferimento_Tecnologico{self.descrizione_contratto}', '{self.valore_economico_contratto}')"


class ScoutingeAssistenza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipologia = db.Column(db.String(1000), nullable=False)
    documentazione = db.Column(db.String(1000), nullable=False)
    descrizione_documentazione = db.Column(db.Text, nullable=False, default='Nessuna Descrizione')
    ente = db.Column(db.Integer, db.ForeignKey('ente.id'), nullable=False)
    responsabile = db.Column(db.Integer, db.ForeignKey('personale_qualificato.id'), nullable=False)

    # personale_supporto = db.Column(db.Integer, db.ForeignKey('personalequalificato.id'), nullable=False)

    def __repr__(self):
        return f"Scouting_e_Assistenza('{self.descrizione_contratto}', '{self.valore_economico_contratto}')"


class FinanziamentoEsterni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipologia = db.Column(db.String(1000), nullable=False)
    ente_cotroparte = db.Column(db.String(1000), nullable=False)
    nazione_ente_controparte = db.Column(db.String(1000), nullable=False)
    eventuali_entrate_correlate = db.Column(db.Integer, nullable=True)
    documentazione = db.Column(db.String(1000), nullable=False)
    descrizione_documentazione = db.Column(db.Text, nullable=False, default='Nessuna Descrizione')
    ente = db.Column(db.Integer, db.ForeignKey('ente.id'), nullable=False)
    responsabile = db.Column(db.Integer, db.ForeignKey('personale_qualificato.id'), nullable=False)

    # personale_supporto = db.Column(db.Integer, db.ForeignKey('personalequalificato.id'), nullable=False)

    def __repr__(self):
        return f"Finanziamento_Esterni('{self.tipologia}', '{self.ente_cotroparte}')"


class SupportoLicensing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oggetto_licensing = db.Column(db.Text, nullable=False)
    ente_controparte = db.Column(db.String(1000), nullable=False)
    nazione_controparte = db.Column(db.String(1000), nullable=False)
    descrizione_controparte = db.Column(db.Text, nullable=False)
    eventuali_entrate_correlate = db.Column(db.Integer, nullable=True)
    documentazione = db.Column(db.String(1000), nullable=False)
    descrizione_documentazione = db.Column(db.Text, nullable=False)
    ente = db.Column(db.Integer, db.ForeignKey('ente.id'), nullable=False)
    responsabile = db.Column(db.Integer, db.ForeignKey('personale_qualificato.id'), nullable=False)

    # personale_supporto = db.Column(db.Integer, db.ForeignKey('personalequalificato.id'), nullable=False)

    def __repr__(self):
        return f"Supporto_Licensing('{self.oggetto_licensing}', '{self.ente_cotroparte}')"


class Corso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titolo_corso = db.Column(db.String(1000), nullable=False)
    data_inizio_corso = db.Column(db.Date, nullable=False)
    data_fine_corso = db.Column(db.Date, nullable=False)
    n_partecipanti = db.Column(db.Integer, nullable=False)
    descrizione = db.Column(db.Text, nullable=False, default='Nessuna Descrizione')
    documentazione = db.Column(db.String(1000), nullable=False)
    descrizione_documentazione = db.Column(db.Text, nullable=False)
    ente = db.Column(db.Integer, db.ForeignKey('ente.id'), nullable=False)
    responsabile = db.Column(db.Integer, db.ForeignKey('personale_qualificato.id'), nullable=False)

    # personale_supporto = db.Column(db.Integer, db.ForeignKey('personalequalificato.id'), nullable=False)

    def __repr__(self):
        return f"Corso('{self.titolo_corso}', '{self.descrizione}')"


class IncubatoriAccelleratoriImpresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipologia = db.Column(db.String(1000), nullable=False)
    descrizione = db.Column(db.Text, nullable=False, default='Nessuna Descrizione')
    documentazione = db.Column(db.String(1000), nullable=False)
    descrizione_documentazione = db.Column(db.Text, nullable=False)
    ente = db.Column(db.Integer, db.ForeignKey('ente.id'), nullable=False)
    responsabile = db.Column(db.Integer, db.ForeignKey('personale_qualificato.id'), nullable=False)

    # personale_supporto = db.Column(db.Integer, db.ForeignKey('personalequalificato.id'), nullable=False)

    def __repr__(self):
        return f"Incubatori_Accelleratori_Impresa(('{self.tipologia}', '{self.descrizione}')"
