import flask
from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from app.forms import RegisterForm, LoginForm, AddFilmForm, FilterForm
import datetime
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required, current_user
from flask_migrate import Migrate


app = Flask(__name__)
app.config["SECRET_KEY"] = '1234'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'


db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
app.app_context().push()

all_genres = ('Action film', 'Adventure film', 'Animated film', 'Comedy film',
              'Drama', 'Fantasy film', 'Historical film', 'Horror film', 'Musical film',
              'Noir film', 'Romance film', 'Science fiction film', 'Thriller film', 'Western')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String, nullable=False, unique=True)


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    film_name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    url = db.Column(db.String)
    id_user = db.Column(db.Integer)
    id_genre = db.Column(db.Integer)
    id_country = db.Column(db.Integer)
    year = db.Column(db.Integer)



@app.route('/')
def home():
    form = FilterForm()
    return render_template("base.html", form=form, filter=False, title="Home", films=Film.query.all())

@login.user_loader
def user_loader(id):
    return User.query.get(int(id))

@app.route('/film/<int:id>')
def film(id):
    film = Film.query.get(id)
    return render_template("film.html", name=film.film_name, description=film.description, year=film.year,
                           image=film.image, url=film.url, poster=User.query.get(film.id_poster).username,
                           country=Country.query.get(film.id_country).country_name, genre=all_genres[film.id_genre])

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        db.session.add(User(name=name, password=password, email=email))
        db.session.commit()
        login_user(User.query.filter_by(name=name).first(), remember=form.remember.data)
        return redirect('/')
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        login_user(user, remember=form.remember.data)
        flask.flash('Logged in successfully')
        if user is None or user.password != password:
            return redirect('/login')
        return redirect('/')
    return render_template("login.html", form=form)
