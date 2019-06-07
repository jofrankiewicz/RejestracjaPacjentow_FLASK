from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import Pacjent


class RegistrationForm(FlaskForm):
    imie = StringField('Imie', validators=[DataRequired(), Length(min=2, max=20)])
    nazwisko = StringField('Nazwisko', validators=[DataRequired(), Length(min=2, max=20)])
    pesel = StringField('Pesel', validators=[DataRequired(), Length(11)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj się')

    def validate_pesel(self, pesel):
        pacjent = Pacjent.query.filter_by(pesel=pesel.data).first()
        if pacjent:
            raise ValidationError('Ten PESEL już istnieje w bazie')

    def validate_email(self, email):
        pacjent = Pacjent.query.filter_by(email=email.data).first()
        if pacjent:
            raise ValidationError('Ten EMAIL już istnieje w bazie')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj się')


class UpdateAccountForm(FlaskForm):
    pesel = StringField('Pesel', validators=[DataRequired(), Length(11)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Aktualizuj')

    def validate_email(self, email):
        if email.data != current_user.email:
            pacjent = Pacjent.query.filter_by(email=email.data).first()
            if pacjent:
                raise ValidationError('Ten EMAIL już istnieje w bazie')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Zresetowanie hasła')

    def validate_email(self, email):
        pacjent = Pacjent.query.filter_by(email=email.data).first()
        if pacjent is None:
            raise ValidationError('Nie istnieje konto o podanym adresie e-mail.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zmień hasło')
