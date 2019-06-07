from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import Pacjent, Wizyta
from flaskblog.pacjenci.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from flaskblog.pacjenci.utils import send_reset_email

pacjenci = Blueprint('pacjenci', __name__)


@pacjenci.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        pacjent = Pacjent(pesel=form.pesel.data, email=form.email.data, password=hashed_password)
        db.session.add(pacjent)
        db.session.commit()
        flash('Twoje konto zostało stworzone, możesz się zalogować.', 'success')
        return redirect(url_for('pacjenci.login'))
    return render_template('register.html', title='Register', form=form)


@pacjenci.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        pacjent = Pacjent.query.filter_by(email=form.email.data).first()
        if pacjent and bcrypt.check_password_hash(pacjent.password, form.password.data):
            login_user(pacjent, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Logowanie nie powiodło się, Proszę sprawdzić e-mail oraz hasło.', 'danger')
    return render_template('login.html', title='Login', form=form)


@pacjenci.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.blank'))


@pacjenci.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.commit()
        flash('Twoje konto zostało zaaktualizowane!', 'success')
        return redirect(url_for('pacjenci.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@pacjenci.route("/pacjent/<string:pesel>")
def wizyty_pacjenta(pesel):
    page = request.args.get('page', 1, type=int)
    pacjent = Pacjent.query.filter_by(pesel=pesel).first_or_404()
    wizyty = Wizyta.query.filter_by(dane_pacjenta=pacjent)\
        .order_by(Wizyta.data_wizyty.desc())\
        .paginate(page=page, per_page=5)
    return render_template('wizyty_pacjenta.html', wizyty=wizyty, pacjent=pacjent)


@pacjenci.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        pacjent = Pacjent.query.filter_by(email=form.email.data).first()
        send_reset_email(pacjent)
        flash('Wysłano email z instrukcją do zresetowania hasła', 'info')
        return redirect(url_for('pacjenci.login'))
    return render_template('reset_request.html', title='Zresetuj hasło', form=form)


@pacjenci.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    pacjent = Pacjent.verify_reset_token(token)
    if pacjent is None:
        flash('Nieprawidłowy token', 'warning')
        return redirect(url_for('pacjenci.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        pacjent.password = hashed_password
        db.session.commit()
        flash('Twoje hasło zostało zaaktualizowane', 'success')
        return redirect(url_for('pacjenci.login'))
    return render_template('reset_token.html', title='Zresetuj hasło', form=form)
