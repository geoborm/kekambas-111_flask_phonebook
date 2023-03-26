from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, EqualTo


class PhoneForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    address = StringField('Address')
    phone_number = StringField('Phone Number', validators=[InputRequired()])
    submit = SubmitField()

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()]) 
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log In ')


class SignupForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')