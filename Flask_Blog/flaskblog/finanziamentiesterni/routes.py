import os
import secrets

from flask import Blueprint, send_file

from flask import render_template, url_for, flash, redirect, request, abort

from flaskblog.finanziamentiesterni.forms import FinanziamentoEsternoForm

from flaskblog.models import FinanziamentoEsterni, PersonaleQualificato
from flaskblog import db, app
from flask_login import current_user, login_required

finanziamentiesterni = Blueprint('finanziamentiesterni', __name__)


@finanziamentiesterni.route('/finanziamentoesterno/new', methods=['GET', 'POST'])
@login_required
def new_finanziamentoesterno():
    form = FinanziamentoEsternoForm()
    form.responsabile.choices = [(r.id, r.nome+' '+r.cognome ) for r in PersonaleQualificato.query.filter_by(tipo=1)]


    if form.validate_on_submit():
        if form.documentazione.data:
            file = form.documentazione.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            filename = random_hex + f_ext
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'] + '/finanziamentiesterni', filename))

        finanziamentoesterno = FinanziamentoEsterni(tipologia=form.tipologia.data, ente_cotroparte=form.ente_controparte.data, nazione_ente_controparte=form.nazione_ente_controparte.data, eventuali_entrate_correlate=form.eventuali_entrate_correlate.data,
                            documentazione=app.root_path + '/' + app.config['UPLOAD_FOLDER'] + '/finanziamentiesterni/' + filename, descrizione_documentazione=form.descrizione_documentazione.data,
                            responsabile=form.responsabile.data, ente=1)
        db.session.add(finanziamentoesterno)
        db.session.commit()
        flash('Finanziamento Esterno inserito con successo', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_finanziamentoesterno.html', title='Nuovo Finanziamento Esterno', form=form, legend='Inserisci Nuovo Finanziamento Esterno')


@finanziamentiesterni.route('/finanziamentoesterno/<int:finanziamentoesterno_id>')
def finanziamentoesterno(finanziamentoesterno_id):
    finanziamentoesterno = FinanziamentoEsterni.query.get_or_404(finanziamentoesterno_id)
    return render_template('finanziamentoesterno.html', title='Finanziamento Esterno', finanziamentoesterno=finanziamentoesterno)


@finanziamentiesterni.route('/finanziamentoesterno/<int:finanziamentoesterno_id>/update', methods=['GET', 'POST'])
@login_required
def update_finanziamentoesterno(finanziamentoesterno_id):
    finanziamentoesterno = FinanziamentoEsterni.query.get_or_404(finanziamentoesterno_id)
    ##if post.author != current_user:
    ##  abort(403)
    form = FinanziamentoEsternoForm()
    form.responsabile.choices = [(r.id, r.nome+' '+r.cognome ) for r in PersonaleQualificato.query.filter_by(tipo=1)]

    if form.validate_on_submit():
        if form.documentazione.data:
            file = form.documentazione.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            filename = random_hex + f_ext
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'] + '/finanziamentiesterni', filename))
            os.remove(finanziamentoesterno.documentazione)
        finanziamentoesterno.tipologia = form.tipologia.data
        finanziamentoesterno.responsabile = form.responsabile.data
        finanziamentoesterno.ente_cotroparte = form.ente_controparte.data
        finanziamentoesterno.nazione_ente_controparte = form.nazione_ente_controparte.data
        finanziamentoesterno.eventuali_entrate_correlate = form.eventuali_entrate_correlate.data
        finanziamentoesterno.documentazione = app.root_path + '/' + app.config['UPLOAD_FOLDER'] + '/finanziamentiesterni/' + filename
        finanziamentoesterno.descrizione_documentazione = form.descrizione_documentazione.data
        db.session.commit()
        flash('Finanziamento esterno modificato con successo', 'success')
        return redirect(url_for('finanziamentiesterni.finanziamentoesterno', finanziamentoesterno_id=finanziamentoesterno.id))
    elif request.method == 'GET':
        form.tipologia.data = finanziamentoesterno.tipologia
        form.ente_controparte.data = finanziamentoesterno.ente_cotroparte
        form.nazione_ente_controparte.data = finanziamentoesterno.nazione_ente_controparte
        form.eventuali_entrate_correlate.data = finanziamentoesterno.eventuali_entrate_correlate
        form.descrizione_documentazione.data = finanziamentoesterno.descrizione_documentazione


    return render_template('create_finanziamentoesterno.html', title='Update finanziamentoesterno', form=form, legend='Modifica finanziamentoesterno')


@finanziamentiesterni.route('/finanziamentoesterno/<int:finanziamentoesterno_id>/delete', methods=['POST'])
@login_required
def delete_finanziamentoesterno(finanziamentoesterno_id):
    finanziamentoesterno = FinanziamentoEsterni.query.get_or_404(finanziamentoesterno_id)
    # if post.author != current_user:
    #   abort(403)
    db.session.delete(finanziamentoesterno)
    os.remove(finanziamentoesterno.documentazione)
    db.session.commit()
    flash('Finanziamento Esterno eliminato con successo', 'success')
    return redirect(url_for('main.home'))

@finanziamentiesterni.route('/finanziamentoesterno/<int:finanziamentoesterno_id>/download')
@login_required
def download_file(finanziamentoesterno_id):
    finanziamentoesterno = FinanziamentoEsterni.query.get_or_404(finanziamentoesterno_id)
    path = finanziamentoesterno.documentazione
    return send_file(path, as_attachment=True)

