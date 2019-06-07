from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Wizyta
from flaskblog.wizyty.forms import WizytaForm

wizyty = Blueprint('wizyty', __name__)


@wizyty.route("/wizyta/new", methods=['GET', 'POST'])
@login_required
def new_wizyta():
    form = WizytaForm()
    if form.validate_on_submit():
        wizyta = Wizyta(kategoria=form.kategoria.data, nazwa_wizyty=form.nazwa_wizyty.data, dane_pacjenta=current_user)
        db.session.add(wizyta)
        db.session.commit()
        flash('Twoja wizyta została dodana', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_wizyta.html', title='Nowa Wizyta', form=form, legend="Nowa wizyta")


@wizyty.route("/wizyty/<int:wizyta_id>")
def wizyta(wizyta_id):
    wizyta = Wizyta.query.get_or_404(wizyta_id)
    if wizyta.dane_pacjenta != current_user:
        abort(403)
    return render_template('wizyta.html', title=wizyta.nazwa_wizyty, wizyta=wizyta)


@wizyty.route("/wizyty/<int:wizyta_id>/update", methods=['GET', 'POST'])
@login_required
def update_wizyta(wizyta_id):
    wizyta = Wizyta.query.get_or_404(wizyta_id)
    if wizyta.dane_pacjenta != current_user:
        abort(403)
    form = WizytaForm()
    if form.validate_on_submit():
        wizyta.nazwa_wizyty = form.nazwa_wizyty.data
        wizyta.kategoria = form.kategoria.data
        db.session.commit()
        flash('Twoja wizyta została zaaktualizowana', 'success')
        return redirect(url_for('wizyty.wizyta', wizyta_id=wizyta.id))
    elif request.method == 'GET':
        form.nazwa_wizyty.data = wizyta.nazwa_wizyty
        form.kategoria.data = wizyta.kategoria
    return render_template('create_wizyta.html', title='Zaaktualizowana wizyta', form=form, legend='Zaaktualizowanie Wizyty')


@wizyty.route("/wizyta/<int:wizyta_id>/delete", methods=['POST'])
@login_required
def delete_wizyta(wizyta_id):
    wizyta = Wizyta.query.get_or_404(wizyta_id)
    if wizyta.dane_pacjenta != current_user:
        abort(403)
    db.session.delete(wizyta)
    db.session.commit()
    flash('Twoja wizyta została usunięta!', 'success')
    return redirect(url_for('main.home'))
