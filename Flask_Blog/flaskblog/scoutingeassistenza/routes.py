import os
import secrets

from flask import Blueprint, send_file

from flask import render_template, url_for, flash, redirect, request, abort

from flaskblog.scoutingeassistenza.forms import ScoutingeAssistenzaForm

from flaskblog.models import ScoutingeAssistenza, PersonaleQualificato
from flaskblog import db, app
from flask_login import current_user, login_required

scoutingassistenza = Blueprint('scoutingassistenza', __name__)


@scoutingassistenza.route('/scoutingeassistenza/new', methods=['GET', 'POST'])
@login_required
def new_scoutingeassistenza():
    form = ScoutingeAssistenzaForm()
    form.responsabile.choices = [(r.id, r.nome+' '+r.cognome ) for r in PersonaleQualificato.query.filter_by(tipo=1)]

    if form.validate_on_submit():
        if form.documentazione.data:
            file = form.documentazione.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            filename = random_hex + f_ext
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'] + '/scouting', filename))

        scoutingeassistenza = ScoutingeAssistenza(tipologia=form.tipologia.data,responsabile=form.responsabile.data, documentazione=app.root_path + '/' + app.config['UPLOAD_FOLDER'] + '/scouting/' + filename, descrizione_documentazione=form.descrizione_documentazione.data, ente=1)
        db.session.add(scoutingeassistenza)
        db.session.commit()
        flash('Scouting e Assistenza inserito con successo', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_scoutingeassistenza.html', title='Nuovo Scouting e Assistenza', form=form, legend='Inserisci nuovo scouting e assistenza')


@scoutingassistenza.route('/scoutingeassistenza/<int:scoutingeassistenza_id>')
def scoutingeassistenza(scoutingeassistenza_id):
    scoutingeassistenza = ScoutingeAssistenza.query.get_or_404(scoutingeassistenza_id)
    return render_template('scoutingeassistenza.html', title='Scouting e Assistenza', scoutingeassistenza=scoutingeassistenza)


@scoutingassistenza.route('/scoutingeassistenza/<int:scoutingeassistenza_id>/update', methods=['GET', 'POST'])
@login_required
def update_scoutingeassistenza(scoutingeassistenza_id):
    scoutingeassistenza = ScoutingeAssistenza.query.get_or_404(scoutingeassistenza_id)
    ##if post.author != current_user:
    ##  abort(403)
    form = ScoutingeAssistenzaForm()
    form.responsabile.choices = [(r.id, r.nome+' '+r.cognome ) for r in PersonaleQualificato.query.filter_by(tipo=1)]

    if form.validate_on_submit():
        if form.documentazione.data:
            file = form.documentazione.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            filename = random_hex + f_ext
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'] + '/scouting', filename))
            os.remove(scoutingeassistenza.documentazione)
        scoutingeassistenza.tipologia = form.tipologia.data
        scoutingeassistenza.documentazione = app.root_path + '/' + app.config['UPLOAD_FOLDER'] + '/scouting/' + filename
        scoutingeassistenza.descrizione_documentazione = form.descrizione_documentazione.data
        scoutingeassistenza.responsabile = form.responsabile.data
        db.session.commit()
        flash('Scouting e Assistenza modificato con successo', 'success')
        return redirect(url_for('scoutingassistenza.scoutingeassistenza', scoutingeassistenza_id=scoutingeassistenza.id))

    elif request.method == 'GET':
        form.tipologia.data = scoutingeassistenza.tipologia
        form.descrizione_documentazione.data = scoutingeassistenza.descrizione_documentazione

    return render_template('create_scoutingeassistenza.html', title='Update Scouting e Assistenza ', form=form, legend='Modifica Scouting e Assistenza')


@scoutingassistenza.route('/scoutingeassistenza/<int:scoutingeassistenza_id>/delete', methods=['POST'])
@login_required
def delete_scoutingeassistenza(scoutingeassistenza_id):
    scoutingeassistenza = ScoutingeAssistenza.query.get_or_404(scoutingeassistenza_id)
    # if post.author != current_user:
    #   abort(403)
    db.session.delete(scoutingeassistenza)
    os.remove(scoutingeassistenza.documentazione)
    db.session.commit()
    flash('Scouting e Assitenza eliminato con successo', 'success')
    return redirect(url_for('main.home'))


@scoutingassistenza.route('/scoutingeassistenza/<int:scoutingeassistenza_id>/download')
@login_required
def download_file(scoutingeassistenza_id):
    scouting = ScoutingeAssistenza.query.get_or_404(scoutingeassistenza_id)
    path = scouting.documentazione
    return send_file(path, as_attachment=True)
