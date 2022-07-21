import os
import secrets

from flask import Blueprint, send_file

from flask import render_template, url_for, flash, redirect, request, abort

from flaskblog.corsi.forms import CorsoForm

from flaskblog.models import Corso, PersonaleQualificato
from flaskblog import db, app
from flask_login import current_user, login_required

corsi = Blueprint('corsi', __name__)


@corsi.route('/corso/new', methods=['GET', 'POST'])
@login_required
def new_corso():
    form = CorsoForm()
    form.responsabile.choices = [(r.id, r.nome+' '+r.cognome ) for r in PersonaleQualificato.query.filter_by(tipo=1)]

    if form.validate_on_submit():
        if form.documentazione.data:
            file = form.documentazione.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            filename = random_hex + f_ext
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'] + '/corsi', filename))

        corso = Corso(titolo_corso=form.titolo_corso.data, data_inizio_corso=form.data_inizio_corso.data, data_fine_corso=form.data_fine_corso.data, n_partecipanti=form.n_partecipanti.data, descrizione=form.descrizione.data,responsabile=form.responsabile.data, documentazione=app.root_path + '/' + app.config['UPLOAD_FOLDER'] + '/corsi/' + filename, descrizione_documentazione=form.descrizione_documentazione.data, ente=1)
        db.session.add(corso)
        db.session.commit()
        flash('Corso inserito con successo', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_corso.html', title='Nuovo Corso', form=form, legend='Inserisci nuovo Corso')


@corsi.route('/corso/<int:corso_id>')
def corso(corso_id):
    corso = Corso.query.get_or_404(corso_id)
    return render_template('corso.html', title='Corso', corso=corso)


@corsi.route('/corso/<int:corso_id>/update', methods=['GET', 'POST'])
@login_required
def update_corso(corso_id):
    corso = Corso.query.get_or_404(corso_id)
    ##if post.author != current_user:
    ##  abort(403)
    form = CorsoForm()
    form.responsabile.choices = [(r.id, r.nome+' '+r.cognome ) for r in PersonaleQualificato.query.filter_by(tipo=1)]

    if form.validate_on_submit():
        if form.documentazione.data:
            file = form.documentazione.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            filename = random_hex + f_ext
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'] + '/corsi', filename))
            os.remove(corso.documentazione)
        corso.titolo_corso = form.titolo_corso.data
        corso.data_inizio_corso = form.data_inizio_corso.data
        corso.data_fine_corso = form.data_fine_corso.data
        corso.n_partecipanti = form.n_partecipanti.data
        corso.descrizione = form.descrizione.data
        corso.responsabile = form.responsabile.data
        corso.documentazione = app.root_path + '/' + app.config['UPLOAD_FOLDER'] + '/corsi/' + filename
        corso.descrizione_documentazione = form.descrizione_documentazione.data

        db.session.commit()
        flash('Corso modificato con successo', 'success')
        return redirect(url_for('corsi.corso', corso_id=corso.id))

    elif request.method == 'GET':
        form.titolo_corso.data = corso.titolo_corso

        form.data_inizio_corso.data = corso.data_inizio_corso

        form.data_fine_corso.data = corso.data_fine_corso

        form.n_partecipanti.data = corso.n_partecipanti

        form.descrizione.data = corso.descrizione

        form.responsabile = corso.responsabile

        form.descrizione_documentazione.data = corso.descrizione_documentazione

    return render_template('create_corso.html', title='Update Corso', form=form, legend='Modifica Corso')


@corsi.route('/corso/<int:corso_id>/delete', methods=['POST'])
@login_required
def delete_corso(corso_id):
    corso = Corso.query.get_or_404(corso_id)
    # if post.author != current_user:
    #   abort(403)
    db.session.delete(corso)
    os.remove(corso.documentazione)
    db.session.commit()
    flash('Corso eliminato con successo', 'success')
    return redirect(url_for('main.home'))


@corsi.route('/corso/<int:corso_id>/download')
@login_required
def download_file(corso_id):
    corso = Corso.query.get_or_404(corso_id)
    path = corso.documentazione
    return send_file(path, as_attachment=True)
