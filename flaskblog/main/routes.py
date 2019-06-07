from flask import render_template, request, Blueprint
from flaskblog.models import Wizyta

main = Blueprint('main', __name__)


@main.route("/")
def poczatek():
    return render_template('blank.html', title='Zaloguj sie')


@main.route("/wizyty")
def home():
    page = request.args.get('page', 1, type=int)
    wizyty = Wizyta.query.order_by(Wizyta.data_wizyty.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', wizyty=wizyty)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/home")
def blank():
    return render_template('blank.html', title='Zaloguj sie')
