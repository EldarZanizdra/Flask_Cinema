from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Password Repeat', validators=[EqualTo('password'), DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField('Enter')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField('Enter')


class AddFilmForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    image = StringField('Image', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Enter')


class FilterForm(FlaskForm):
    name = StringField('Name')
    genre = StringField('Genre')
    country = StringField('Country')
    year = IntegerField('Year', validators=[DataRequired()])
    submit = SubmitField('Search')
