import os
import secrets

from flask import Blueprint, send_file

from flask import render_template, url_for, flash, redirect, request, abort

from flaskblog.incubatoriaccelleratoriimpresa.forms import IncubatoreAccelleratoreImpresaForm

from flaskblog.models import Corso, IncubatoriAccelleratoriImpresa, PersonaleQualificato
from flaskblog import db, app
from flask_login import current_user, login_required

incubatoriaccelleratoriimpresa = Blueprint('incubatoriaccelleratoriimpresa', __name__)


@incubatoriaccelleratoriimpresa.route('/incubatoriaccelleratoriimpresa/new', methods=['GET', 'POST'])
@login_required
def new_incubatore():
    form = IncubatoreAccelleratoreImpresaForm()
    form.responsabile.choices = [(r.id, r.nome+' '+r.cognome ) for r in PersonaleQualificato.query.filter_by(tipo=1)]

    if form.validate_on_submit():
        if form.documentazione.data:
            file = form.documentazione.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            filename = random_hex + f_ext
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'] + '/incubatori', filename))

        incubatore = IncubatoriAccelleratoriImpresa(tipologia=form.tipologia.data, descrizione=form.descrizione.data,responsabile=form.responsabile.data, documentazione=app.root_path + '/' + app.config['UPLOAD_FOLDER'] + '/incubatori/' + filename, descrizione_documentazione=form.descrizione_documentazione.data, ente=1)
        db.session.add(incubatore)
        db.session.commit()
        flash('Incubatore/Accelleratore di Impresa aggiunto con successo', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_incubatore.html', title='Nuovo Incubatore/Accelleratore di Impresa', form=form, legend='Inserisci nuovo Incubatore/Accelleratore di Impresa')


@incubatoriaccelleratoriimpresa.route('/incubatoriaccelleratoriimpresa/<int:incubatore_id>')
def incubatore(incubatore_id):
    incubatore = IncubatoriAccelleratoriImpresa.query.get_or_404(incubatore_id)
    return render_template('incubatore.html', title='Incubatore', incubatore=incubatore)


@incubatoriaccelleratoriimpresa.route('/incubatoriaccelleratoriimpresa/<int:incubatore_id>/update', methods=['GET', 'POST'])
@login_required
def update_incubatore(incubatore_id):
    incubatore = IncubatoriAccelleratoriImpresa.query.get_or_404(incubatore_id)
    ##if post.author != current_user:
    ##  abort(403)
    form = IncubatoreAccelleratoreImpresaForm()
    form.responsabile.choices = [(r.id, r.nome+' '+r.cognome ) for r in PersonaleQualificato.query.filter_by(tipo=1)]

    if form.validate_on_submit():
        if form.documentazione.data:
            file = form.documentazione.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            filename = random_hex + f_ext
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'] + '/incubatori', filename))
            os.remove(incubatore.documentazione)
        incubatore.tipologia = form.tipologia.data
        incubatore.responsabile = form.responsabile.data
        incubatore.descrizione = form.descrizione.data
        incubatore.documentazione = app.root_path + '/' + app.config['UPLOAD_FOLDER'] + '/incubatori/' + filename
        incubatore.descrizione_documentazione = form.descrizione_documentazione.data

        db.session.commit()
        flash('Incubatore/Accelleratore di Impresa modificato con successo', 'success')
        return redirect(url_for('incubatoriaccelleratoriimpresa.incubatore', incubatore_id=incubatore.id))

    elif request.method == 'GET':
        form.tipologia.data = incubatore.tipologia

        form.descrizione.data = incubatore.descrizione

        form.descrizione_documentazione.data = incubatore.descrizione_documentazione

    return render_template('create_incubatore.html', title='Update incubatore', form=form, legend='Modifica incubatore')


@incubatoriaccelleratoriimpresa.route('/incubatoriaccelleratoriimpresa/<int:incubatore_id>/delete', methods=['POST'])
@login_required
def delete_incubatore(incubatore_id):
    incubatore = IncubatoriAccelleratoriImpresa.query.get_or_404(incubatore_id)
    # if post.author != current_user:
    #   abort(403)
    db.session.delete(incubatore)
    os.remove(incubatore.documentazione)
    db.session.commit()
    flash('Incubatore/Accelleratore Impresa eliminato con successo', 'success')
    return redirect(url_for('main.home'))


@incubatoriaccelleratoriimpresa.route('/incubatoriaccelleratoriimpresa/<int:incubatore_id>/download')
@login_required
def download_file(incubatore_id):
    incubatore = Corso.query.get_or_404(incubatore_id)
    path = incubatore.documentazione
    return send_file(path, as_attachment=True)
