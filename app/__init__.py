import flask
from flask import Flask, render_template, redirect, request
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


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    film_name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    genre = db.Column(db.String)
    country = db.Column(db.Integer, db.ForeignKey("country.id"))
    year = db.Column(db.Integer)


movies = Film.query.all()

movies_by_year = Film.query.all()


@app.route('/')
def home():
    movies = Film.query.all()
    films = Film.query.all()
    form = FilterForm()
    return render_template("home.html", form=form, filter=False, title="Home", films=films, movies=movies)


@app.route('/admin')
def admin():
    return render_template("admin.html")


@login.user_loader
def user_loader(id):
    return User.query.get(int(id))


@app.route('/film/<int:id>')
def film(id):
    film = Film.query.get(id)
    return render_template("film.html", film_name=film.film_name, description=film.description, year=film.year,
                           image=film.image, country=Country.query.get(film.country).name, genre=film.genre)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        db.session.add(User(username=name, password=password, email=email))
        db.session.commit()
        login_user(User.query.filter_by(username=name).first(), remember=form.remember.data)
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


@app.route('/add_film', methods=["GET", "POST"])
@login_required
def add_film():
    form = AddFilmForm()
    file = 0

    if request.method == 'POST':
        file = request.files['image']
        file.save(f'app/static/image/{file.filename}')

    if form.validate_on_submit():
        name_country = form.country.data

        if not Country.query.filter_by(name=name_country).first():
            db.session.add(Country(name=name_country))
            db.session.commit()

        db.session.add(Film(film_name=form.name.data, description=form.description.data,
                            image=f'/static/image/{file.filename}', year=form.year.data,
                            genre=form.genre.data,
                            country=Country.query.filter_by(name=name_country).first().id))
        db.session.commit()
        return redirect('/')

    return render_template("add_film.html", form=form, title="Post new film")


@app.route('/filter', methods=['GET', 'POST'])
def filter_by_genre():
    if request.method == 'POST':
        genre = request.form['genre']
        year = request.form['year']
        filtered_movies = []
        for movie in movies:
            if movie['genre'] == genre and movie['year'] == year:
                filtered_movies.append(movie)
            else:
               return render_template('filter.html', movies=filtered_movies)
        return render_template('filter.html', movies=filtered_movies)
    else:
        return render_template('filter.html', movies=movies)

def filter_movies_by_genre(genre):
    filtered_movies = Film.query.filter_by(genre=genre).all()
    return filtered_movies







