# save this as app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '463d73851bf4ad01b51b88782f63acde'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/attivita'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main
from flaskblog.PersonaleQualificato.routes import personalequalificato
from flaskblog.brevetti.routes import brevetti
from flaskblog.contrattiricerca.routes import contrattiricerca
from flaskblog.negoziazionitrasferimentotecnologico.routes import negoziazionitrasferimentotecnologico
from flaskblog.scoutingeassistenza.routes import scoutingassistenza
from flaskblog.finanziamentiesterni.routes import finanziamentiesterni
from flaskblog.supportolicensing.routes import supportolicensings
from flaskblog.corsi.routes import corsi
from flaskblog.incubatoriaccelleratoriimpresa.routes import incubatoriaccelleratoriimpresa
from flaskblog.errors.handlers import errors

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(personalequalificato)
app.register_blueprint(brevetti)
app.register_blueprint(contrattiricerca)
app.register_blueprint(negoziazionitrasferimentotecnologico)
app.register_blueprint(scoutingassistenza)
app.register_blueprint(finanziamentiesterni)
app.register_blueprint(supportolicensings)
app.register_blueprint(corsi)
app.register_blueprint(incubatoriaccelleratoriimpresa)
app.register_blueprint(errors)
