import os
import secrets

from flask import Blueprint, send_file

from flask import render_template, url_for, flash, redirect, request, abort

from flaskblog.negoziazionitrasferimentotecnologico.forms import NegoziazioneTrasferimentoTecnologicoForm

from flaskblog.models import NegoziazioneTrasferimentoTecnologico, PersonaleQualificato
from flaskblog import db, app
from flask_login import current_user, login_required

negoziazionitrasferimentotecnologico = Blueprint('negoziazionitrasferimentotecnologico', __name__)


@negoziazionitrasferimentotecnologico.route('/negoziazionetrasferimentotecnologico/new', methods=['GET', 'POST'])
@login_required
def new_negoziazione():
    form = NegoziazioneTrasferimentoTecnologicoForm()
    form.responsabile.choices = [(r.id, r.nome+' '+r.cognome ) for r in PersonaleQualificato.query.filter_by(tipo=1)]

    if form.validate_on_submit():
        if form.documentazione.data:
            file = form.documentazione.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            filename = random_hex + f_ext
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'] + '/negoziazioni', filename))

        negoziazione= NegoziazioneTrasferimentoTecnologico(tipologia=form.tipologia.data, controparte=form.controparte.data, nazione_controparte=form.nazione_controparte.data,
                            documentazione=app.root_path + '/' + app.config['UPLOAD_FOLDER'] + '/negoziazioni/' + filename, descrizione_documentazione=form.descrizione_documentazione.data,
                            responsabile=form.responsabile.data,ente=1)
        db.session.add(negoziazione)
        db.session.commit()
        flash('Negoziazione per il trasferimento tecnologico inserito con successo', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_negoziazione.html', title='Nuova Negoziazione', form=form, legend='Inserisci Nuova Negoziazione')


@negoziazionitrasferimentotecnologico.route('/negoziazionetrasferimentotecnologico/<int:negoziazione_id>')
def negoziazione(negoziazione_id):
    negoziazione = NegoziazioneTrasferimentoTecnologico.query.get_or_404(negoziazione_id)
    return render_template('negoziazione.html', title='Negoziazione trasferimento tecnologico', negoziazione=negoziazione)


@negoziazionitrasferimentotecnologico.route('/negoziazionetrasferimentotecnologico/<int:negoziazione_id>/update', methods=['GET', 'POST'])
@login_required
def update_negoziazione(negoziazione_id):
    negoziazione = NegoziazioneTrasferimentoTecnologico.query.get_or_404(negoziazione_id)
    ##if post.author != current_user:
    ##  abort(403)
    form = NegoziazioneTrasferimentoTecnologicoForm()
    form.responsabile.choices = [(r.id, r.nome+' '+r.cognome ) for r in PersonaleQualificato.query.filter_by(tipo=1)]

    if form.validate_on_submit():
        if form.documentazione.data:
            file = form.documentazione.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            filename = random_hex + f_ext
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'] + '/negoziazioni', filename))
            os.remove(negoziazione.documentazione)
        negoziazione.tipologia = form.tipologia.data
        negoziazione.responsabile = form.responsabile.data
        negoziazione.controparte = form.controparte.data
        negoziazione.nazione_controparte = form.nazione_controparte.data
        negoziazione.documentazione = app.root_path + '/' + app.config['UPLOAD_FOLDER'] + '/negoziazioni/' + filename
        negoziazione.descrizione_documentazione = form.descrizione_documentazione.data
        db.session.commit()
        flash('Contratto modificato con successo', 'success')
        return redirect(url_for('negoziazionitrasferimentotecnologico.negoziazione', negoziazione_id=negoziazione.id))
    elif request.method == 'GET':
        form.tipologia.data = negoziazione.tipologia
        form.controparte.data = negoziazione.controparte
        form.nazione_controparte.data = negoziazione.nazione_controparte
        form.descrizione_documentazione.data = negoziazione.descrizione_documentazione


    return render_template('create_negoziazione.html', title='Update Negoziazione', form=form, legend='Modifica Negoziazione')


@negoziazionitrasferimentotecnologico.route('/negoziazionetrasferimentotecnologico/<int:negoziazione_id>/delete', methods=['POST'])
@login_required
def delete_negoziazione(negoziazione_id):
    negoziazione = NegoziazioneTrasferimentoTecnologico.query.get_or_404(negoziazione_id)
    # if post.author != current_user:
    #   abort(403)
    db.session.delete(negoziazione)
    os.remove(negoziazione.documentazione)
    db.session.commit()
    flash('Negoziazione eliminato con successo', 'success')
    return redirect(url_for('main.home'))


@negoziazionitrasferimentotecnologico.route('/negoziazionetrasferimentotecnologico/<int:negoziazione_id>/download')
@login_required
def download_file(negoziazione_id):
    negoziazione = NegoziazioneTrasferimentoTecnologico.query.get_or_404(negoziazione_id)
    path = negoziazione.documentazione
    return send_file(path, as_attachment=True)
