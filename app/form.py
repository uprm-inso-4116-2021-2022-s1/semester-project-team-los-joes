from re import RegexFlag
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FileField, IntegerField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Book, User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    show_password = BooleanField('Show Password')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class SignUpForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class NewPostingForm(FlaskForm):
    isbn_choices = []
    for book in Book.query.all():
        isbn_choices.append(book.title)
    title = SelectField('Title', choices=isbn_choices, validators=[DataRequired()])
    description = TextAreaField('Add Description', validators=[DataRequired()])
    condition = SelectField('Condition', choices=['Like New','Used', 'Very Used', 'Barely Holding On'], validators=[DataRequired()])
    price = IntegerField('Enter Price',validators=[DataRequired()])
    image = FileField(u'Image File', validators=[DataRequired()])
    submit = SubmitField('Submit')