from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from wtforms import ValidationError
from ..models import User


class SignUpForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(1, 56), Regexp('^[A-Za-z][A-Za-z]',0,'Name must only contain letters')])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(1, 56), Regexp('^[A-Za-z][A-Za-z]',0,'Name must only contain letters')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 56), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=32), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already in use')


class LogInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 56), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class ChangePasswordForm(FlaskForm):
    oldpassword = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, max=32), EqualTo('password2', message='Passwords Must Match')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Update Password')