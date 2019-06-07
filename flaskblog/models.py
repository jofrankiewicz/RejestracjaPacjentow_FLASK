from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_pacjent(pacjent_id):
    return Pacjent.query.get(int(pacjent_id))


class Pacjent(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    pesel = db.Column(db.String(11), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    wizyty = db.relationship('Wizyta', backref='dane_pacjenta', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'pacjent_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            pacjent_id = s.loads(token)['pacjent_id']
        except:
            return None
        return Pacjent.query.get(pacjent_id)

    def __repr__(self):
        return f"Pacjent('{self.pesel}', '{self.email}', '{self.password}')"


class Wizyta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_wizyty = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    nazwa_wizyty = db.Column(db.String(50), nullable=False)
    kategoria = db.Column(db.Text, nullable=False)
    pacjent_id = db.Column(db.Integer, db.ForeignKey('pacjent.id'), nullable=False)

    def __repr__(self):
        return f"Wizyta('{self.nazwa_wizyty}', '{self.data_wizyty}')"
