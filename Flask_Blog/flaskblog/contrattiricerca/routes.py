import os
import secrets

from flask import Blueprint

from flask import render_template, url_for, flash, redirect, request, abort, send_file
from werkzeug.utils import secure_filename

from flaskblog.contrattiricerca.forms import ContrattoRicercaForm

from flaskblog.models import ContrattoRicerca, PersonaleQualificato
from flaskblog import db, app
from flask_login import current_user, login_required

contrattiricerca = Blueprint('contrattiricerca', __name__)


@contrattiricerca.route('/contrattoricerca/new', methods=['GET', 'POST'])
@login_required
def new_contrattoricerca():
    form = ContrattoRicercaForm()
    form.responsabile.choices = [(r.id, r.nome+' '+r.cognome ) for r in PersonaleQualificato.query.filter_by(tipo=1)]
    if form.validate_on_submit():
        if form.contratto.data:
            file = form.contratto.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            filename = random_hex + f_ext
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'] + '/contrattiricerca', filename))

        contrattoricerca = ContrattoRicerca(denominazione_industria=form.denominazione_industria.data,
                                            contratto=app.root_path + '/' + app.config['UPLOAD_FOLDER'] + '/contrattiricerca/' + filename,
                                            descrizione_contratto=form.descrizione_contratto.data,
                                            anno_sottoscrizione_collaborazione=form.anno_sottoscrizione_collaborazione.data,
                                            durata_collaborazione=form.durata_collaborazione.data,
                                            oggetto_collaborazione=form.oggetto_collaborazione.data,
                                            valore_economico_contratto=form.valore_economico_contratto.data,
                                            responsabile=form.responsabile.data, ente=1)
        db.session.add(contrattoricerca)
        db.session.commit()
        flash('Contratto di Ricerca inserito con successo', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_contrattoricerca.html', title='Nuovo Contratto di Ricerca', form=form,
                           legend='Inserisci nuovo contratto di ricerca')


@contrattiricerca.route('/contrattoricerca/<int:contrattoricerca_id>')
def contrattoricerca(contrattoricerca_id):
    contrattoricerca = ContrattoRicerca.query.get_or_404(contrattoricerca_id)
    return render_template('contrattoricerca.html', title='Contratto Ricerca', contrattoricerca=contrattoricerca)


@contrattiricerca.route('/contrattoricerca/<int:contrattoricerca_id>/update', methods=['GET', 'POST'])
@login_required
def update_contrattoricerca(contrattoricerca_id):
    contrattoricerca = ContrattoRicerca.query.get_or_404(contrattoricerca_id)
    ##if post.author != current_user:
    ##  abort(403)
    form = ContrattoRicercaForm()
    form.responsabile.choices = [(r.id, r.nome+' '+r.cognome ) for r in PersonaleQualificato.query.filter_by(tipo=1)]
    if form.validate_on_submit():
        if form.contratto.data:
            file = form.contratto.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            filename = random_hex + f_ext
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'] + '/contrattiricerca', filename))
            os.remove(contrattoricerca.contratto)

        contrattoricerca.denominazione_industria = form.denominazione_industria.data
        contrattoricerca.contratto = app.root_path + '/' + app.config['UPLOAD_FOLDER'] + '/contrattiricerca/' + filename
        contrattoricerca.descrizione_contratto = form.descrizione_contratto.data
        contrattoricerca.anno_sottoscrizione_collaborazione = form.anno_sottoscrizione_collaborazione.data
        contrattoricerca.durata_collaborazione = form.durata_collaborazione.data
        contrattoricerca.oggetto_collaborazione = form.oggetto_collaborazione.data
        contrattoricerca.valore_economico_contratto = form.valore_economico_contratto.data
        contrattoricerca.responsabile = form.responsabile.data
        db.session.commit()
        flash('Contratto modificato con successo', 'success')
        return redirect(url_for('contrattiricerca.contrattoricerca', contrattoricerca_id=contrattoricerca.id))

    elif request.method == 'GET':
        form.denominazione_industria.data = contrattoricerca.denominazione_industria
        form.contratto.data = contrattoricerca.contratto
        form.descrizione_contratto.data = contrattoricerca.descrizione_contratto
        form.anno_sottoscrizione_collaborazione.data = contrattoricerca.anno_sottoscrizione_collaborazione
        form.durata_collaborazione.data = contrattoricerca.durata_collaborazione
        form.oggetto_collaborazione.data = contrattoricerca.oggetto_collaborazione
        form.valore_economico_contratto.data = contrattoricerca.valore_economico_contratto

    return render_template('create_contrattoricerca.html', title='Update Contratto di Ricerca', form=form,
                           legend='Modifica Contratto di Ricerca')


@contrattiricerca.route('/contrattoricerca/<int:contrattoricerca_id>/delete', methods=['POST'])
@login_required
def delete_contrattoricerca(contrattoricerca_id):
    contrattoricerca = ContrattoRicerca.query.get_or_404(contrattoricerca_id)
    # if post.author != current_user:
    #   abort(403)
    db.session.delete(contrattoricerca)
    os.remove(contrattoricerca.contratto)
    db.session.commit()
    flash('Contratto di Ricerca eliminato con successo', 'success')
    return redirect(url_for('main.home'))
@contrattiricerca.route('/contrattoricerca/<int:contrattoricerca_id>/download')
@login_required
def download_file(contrattoricerca_id):
    contrattoricerca = ContrattoRicerca.query.get_or_404(contrattoricerca_id)
    path = contrattoricerca.contratto
    return send_file(path, as_attachment=True)
