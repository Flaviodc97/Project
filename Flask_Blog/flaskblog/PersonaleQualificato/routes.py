import os
import secrets

from flask import Blueprint, send_file

from flask import render_template, url_for, flash, redirect, request, abort

from flaskblog.PersonaleQualificato.forms import NewPersonaleForm

from flaskblog.models import Ente, PersonaleQualificato
from flaskblog import db, app
from flask_login import current_user, login_required

personalequalificato = Blueprint('personalequalificato', __name__)


@personalequalificato.route('/personalequalificato/new', methods=['GET', 'POST'])
@login_required
def new_personale():
    form = NewPersonaleForm()
    if form.validate_on_submit():
        tipo = form.tipo.data
        if tipo == 'False':
            tipo = False
        else:
            tipo = True
        if form.documento.data:
            file = form.documento.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            filename = random_hex + f_ext
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'] + '/personale', filename))

        personale = PersonaleQualificato(nome=form.nome.data, cognome=form.cognome.data, cf=form.cf.data,
                                         data_di_nascita=form.data_di_nascita.data, qualifica=form.qualifica.data,
                                         struttura=form.struttura.data,
                                         competenza_specifica=form.competenza_specifica.data,
                                         tipologia_contratto=form.tipologia_contratto.data, altro=form.altro.data,
                                         data_inizio_rapporto=form.data_inizio_rapporto.data,
                                         documento=app.root_path + '/' + app.config['UPLOAD_FOLDER'] + '/personale/' + filename,
                                         descrizione_documento=form.descrizione_documento.data,
                                         descrizione=form.descrizione.data, tipo=tipo, ente=1)
        db.session.add(personale)
        db.session.commit()
        flash('Personale Qualificato inserito con successo', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_personale.html', title='Nuovo Personale Qualificato', form=form,
                           legend='Inserisci nuovo personale')


@personalequalificato.route('/personalequalificato/<int:personale_id>')
def personale(personale_id):
    personale = PersonaleQualificato.query.get_or_404(personale_id)
    return render_template('personale.html', title='personale.nome' + 'personale.cognome', personale=personale)


@personalequalificato.route('/personalequalificato/<int:personale_id>/update', methods=['GET', 'POST'])
@login_required
def update_personale(personale_id):
    personale = PersonaleQualificato.query.get_or_404(personale_id)
    ##if post.author != current_user:
    ##  abort(403)
    form = NewPersonaleForm()
    if form.validate_on_submit():
        tipo = form.tipo.data
        if tipo == 'False':
            tipo = False
        else:
            tipo = True
        if form.documento.data:
            file = form.documento.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            filename = random_hex + f_ext
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'] + '/personale', filename))
            os.remove(personale.documento)
        personale.nome = form.nome.data
        personale.cognome = form.cognome.data
        personale.cf = form.cf.data
        personale.data_di_nascita = form.data_di_nascita.data
        personale.qualifica = form.qualifica.data
        personale.struttura = form.struttura.data
        personale.competenza_specifica = form.competenza_specifica.data
        personale.tipologia_contratto = form.tipologia_contratto.data
        personale.altro = form.altro.data
        personale.data_inizio_rapporto = form.data_inizio_rapporto.data
        personale.documento = app.root_path + '/' + app.config['UPLOAD_FOLDER'] + '/personale/' + filename
        personale.descrizione = form.descrizione.data
        personale.descrizione_documento = form.descrizione_documento.data
        personale.tipo = tipo
        db.session.commit()
        flash('Personale modificato con successo', 'success')
        return redirect(url_for('personalequalificato.personale', personale_id=personale.id))
    elif request.method == 'GET':
        form.nome.data = personale.nome
        form.cognome.data = personale.cognome
        form.cf.data = personale.cf
        form.data_di_nascita.data = personale.data_di_nascita
        form.qualifica.data = personale.qualifica
        form.struttura.data = personale.struttura
        form.competenza_specifica.data = personale.competenza_specifica
        form.tipologia_contratto.data = personale.tipologia_contratto
        form.altro.data = personale.altro
        form.data_inizio_rapporto.data = personale.data_inizio_rapporto

        form.descrizione.data = personale.descrizione
        form.descrizione_documento.data = personale.descrizione_documento
        form.tipo.data = personale.tipo
    return render_template('create_personale.html', title='Update Personale', form=form, legend='Modifica Personale')


@personalequalificato.route('/personalequalificato/<int:personale_id>/delete', methods=['POST'])
@login_required
def delete_personale(personale_id):
    personale = PersonaleQualificato.query.get_or_404(personale_id)
    # if post.author != current_user:
    #   abort(403)
    db.session.delete(personale)
    os.remove(personale.documento)
    db.session.commit()
    flash('Personale eliminato con successo', 'success')
    return redirect(url_for('main.home'))
@personalequalificato.route('/personalequalificato/<int:personale_id>/download')
@login_required
def download_file(personale_id):
    personale = PersonaleQualificato.query.get_or_404(personale_id)
    path = personale.documento
    return send_file(path, as_attachment=True)
