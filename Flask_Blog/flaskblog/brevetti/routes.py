import os
import secrets

from flask import Blueprint

from flask import render_template, url_for, flash, redirect, request, abort, send_file
from werkzeug.utils import secure_filename

from flaskblog.brevetti.forms import BrevettoForm

from flaskblog.models import Brevetto, PersonaleQualificato
from flaskblog import db, app
from flask_login import current_user, login_required

brevetti = Blueprint('brevetti', __name__)


@brevetti.route('/brevetti/new', methods=['GET', 'POST'])
@login_required
def new_brevetto():
    form = BrevettoForm()
    form.responsabile.choices = [(r.id, r.nome+' '+r.cognome ) for r in PersonaleQualificato.query.filter_by(tipo=1)]
    if form.validate_on_submit():
        if form.certificato.data:
            file = form.certificato.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            filename = random_hex + f_ext
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'] + '/brevetti', filename))

        brevetto = Brevetto(nome=form.nome.data,
                            codice=form.codice.data,
                            nazione_validita=form.nazione_validita.data,
                            descrizione=form.descrizione.data,
                            anno_presentazione=form.anno_presentazione.data,
                            anno_assegnazione=form.anno_assegnazione.data,
                            certificato=app.root_path + '/' + app.config['UPLOAD_FOLDER'] + '/brevetti/' + filename,
                            responsabile=form.responsabile.data,
                            ente=1)
        db.session.add(brevetto)
        db.session.commit()
        flash('Brevetto inserito con successo', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_brevetto.html', title='Nuovo Brevetto', form=form, legend='Inserisci nuovo brevetto')


@brevetti.route('/brevetto/<int:brevetto_id>')
def brevetto(brevetto_id):
    brevetto = Brevetto.query.get_or_404(brevetto_id)
    return render_template('brevetto.html', title='Brevetto', brevetto=brevetto)


@brevetti.route('/brevetto/<int:brevetto_id>/update', methods=['GET', 'POST'])
@login_required
def update_brevetto(brevetto_id):
    brevetto = Brevetto.query.get_or_404(brevetto_id)
    ##if post.author != current_user:
    ##  abort(403)
    form = BrevettoForm()
    form.responsabile.choices = [(r.id, r.nome+' '+r.cognome ) for r in PersonaleQualificato.query.filter_by(tipo=1)]
    if form.validate_on_submit():
        if form.certificato.data:
            file = form.certificato.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            filename = random_hex + f_ext
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'] + '/brevetti', filename))
            os.remove(brevetto.certificato)

        brevetto.nome = form.nome.data
        brevetto.certificato = app.root_path + '/' + app.config['UPLOAD_FOLDER'] + '/brevetti/' + filename
        brevetto.codice = form.codice.data
        brevetto.nazione_validita = form.nazione_validita.data
        brevetto.descrizione = form.descrizione.data
        brevetto.anno_assegnazione = form.anno_assegnazione.data
        brevetto.anno_presentazione = form.anno_presentazione.data
        brevetto.responsabile = form.responsabile.data
        db.session.commit()
        flash('Brevetto caricato con successo', 'success')
        return redirect(url_for('brevetti.brevetto', brevetto_id=brevetto.id))

    elif request.method == 'GET':
        form.nome.data = brevetto.nome
        form.codice.data = brevetto.codice
        form.nazione_validita.data = brevetto.nazione_validita
        form.descrizione.data = brevetto.descrizione
        form.responsabile.data = brevetto.responsabile
        form.anno_presentazione.data = brevetto.anno_presentazione
        form.anno_assegnazione.data = brevetto.anno_assegnazione

    return render_template('create_brevetto.html', title='Update Brevetto', form=form,
                           legend='Modifica Brevetto')


@brevetti.route('/brevetto/<int:brevetto_id>/delete', methods=['POST'])
@login_required
def delete_brevetto(brevetto_id):
    brevetto = Brevetto.query.get_or_404(brevetto_id)
    # if post.author != current_user:
    #   abort(403)
    db.session.delete(brevetto)
    os.remove(brevetto.certificato)
    db.session.commit()
    flash('Brevetto eliminato con successo', 'success')
    return redirect(url_for('main.home'))


@brevetti.route('/brevetto/<int:brevetto_id>/download')
@login_required
def download_file(brevetto_id):
    brevetto = Brevetto.query.get_or_404(brevetto_id)
    path = brevetto.certificato
    return send_file(path, as_attachment=True)
