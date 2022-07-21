import os
import secrets

from flask import Blueprint, send_file

from flask import render_template, url_for, flash, redirect, request, abort

from flaskblog.supportolicensing.forms import SupportoLicensingForm

from flaskblog.models import SupportoLicensing, PersonaleQualificato
from flaskblog import db, app
from flask_login import current_user, login_required

supportolicensings = Blueprint('supportolicensings', __name__)


@supportolicensings.route('/supportolicensing/new', methods=['GET', 'POST'])
@login_required
def new_supportolicensing():
    form = SupportoLicensingForm()
    form.responsabile.choices = [(r.id, r.nome+' '+r.cognome ) for r in PersonaleQualificato.query.filter_by(tipo=1)]

    if form.validate_on_submit():
        if form.documentazione.data:
            file = form.documentazione.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            filename = random_hex + f_ext
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'] + '/supporti', filename))

        supportolicensing = SupportoLicensing(oggetto_licensing=form.oggetto_licensing.data, responsabile=form.responsabile.data, ente_controparte=form.ente_controparte.data, nazione_controparte=form.nazione_controparte.data, descrizione_controparte=form.descrizione_controparte.data,eventuali_entrate_correlate=form.eventuali_entrate_correlate.data, documentazione=app.root_path + '/' + app.config['UPLOAD_FOLDER'] + '/supporti/' + filename, descrizione_documentazione=form.descrizione_documentazione.data, ente=1)
        db.session.add(supportolicensing)
        db.session.commit()
        flash('Supporto Licensing inserito con successo', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_supportolicensing.html', title='Nuovo Supporto Licensing', form=form, legend='Inserisci nuovo Supporto Licensing')


@supportolicensings.route('/supportolicensing/<int:supportolicensing_id>')
def supportolicensing(supportolicensing_id):
    supportolicensing = SupportoLicensing.query.get_or_404(supportolicensing_id)
    return render_template('supportolicensing.html', title='Supporto Licensing', supportolicensing=supportolicensing)


@supportolicensings.route('/supportolicensing/<int:supportolicensing_id>/update', methods=['GET', 'POST'])
@login_required
def update_supportolicensing(supportolicensing_id):
    supportolicensing = SupportoLicensing.query.get_or_404(supportolicensing_id)
    ##if post.author != current_user:
    ##  abort(403)
    form = SupportoLicensingForm()
    form.responsabile.choices = [(r.id, r.nome+' '+r.cognome ) for r in PersonaleQualificato.query.filter_by(tipo=1)]

    if form.validate_on_submit():
        if form.documentazione.data:
            file = form.documentazione.data
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(file.filename)
            filename = random_hex + f_ext
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'] + '/supporti', filename))
            os.remove(supportolicensing.documentazione)
        supportolicensing.oggetto_licensing = form.oggetto_licensing.data
        supportolicensing.responsabile = form.responsabile.data
        supportolicensing.ente_controparte = form.ente_controparte.data
        supportolicensing.nazione_controparte = form.nazione_controparte.data
        supportolicensing.descrizione_controparte = form.descrizione_controparte.data
        supportolicensing.eventuali_entrate_correlate = form.eventuali_entrate_correlate.data
        supportolicensing.documentazione = app.root_path + '/' + app.config['UPLOAD_FOLDER'] + '/supporti/' + filename
        supportolicensing.descrizione_documentazione = form.descrizione_documentazione.data

        db.session.commit()
        flash('Supporto e Licensing modificato con successo', 'success')
        return redirect(url_for('supportolicensings.supportolicensing', supportolicensing_id=supportolicensing.id))

    elif request.method == 'GET':
        form.oggetto_licensing.data = supportolicensing.oggetto_licensing

        form.ente_controparte.data = supportolicensing.ente_controparte

        form.nazione_controparte.data = supportolicensing.nazione_controparte

        form.descrizione_controparte.data = supportolicensing.descrizione_controparte

        form.eventuali_entrate_correlate.data = supportolicensing.eventuali_entrate_correlate

        form.descrizione_documentazione.data = supportolicensing.descrizione_documentazione

    return render_template('create_supportolicensing.html', title='Update Supporto e Licensing ', form=form, legend='Modifica Supporto e Licensing')


@supportolicensings.route('/supportolicensing/<int:supportolicensing_id>/delete', methods=['POST'])
@login_required
def delete_supportolicensing(supportolicensing_id):
    supportolicensing = SupportoLicensing.query.get_or_404(supportolicensing_id)
    # if post.author != current_user:
    #   abort(403)
    db.session.delete(supportolicensing)
    os.remove(supportolicensing.documentazione)
    db.session.commit()
    flash('Supporto e Licensing eliminato con successo', 'success')
    return redirect(url_for('main.home'))


@supportolicensings.route('/supportolicensing/<int:supportolicensing_id>/download')
@login_required
def download_file(supportolicensing_id):
    supporto = SupportoLicensing.query.get_or_404(supportolicensing_id)
    path = supporto.documentazione
    return send_file(path, as_attachment=True)
