from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo, Regexp

from app.models import Users


class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(message="This field is required"), Email()], render_kw={'placeholder': 'Enter your email: '})
    password = PasswordField("Password",validators=[DataRequired("The length of password must be more than 6 symbols"), Length(min=6)], render_kw={'placeholder': 'Enter your password: '})
    remember = BooleanField("Keep me logged in:", default='unchecked', render_kw={'placeholder': 'Keep me logged in: '})
    submit = SubmitField("Sign In")

class ChangePasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired("The length of password must be from 4 to 10 symbols"), Length(min=4, max=10)], render_kw={'placeholder': 'Enter your password: '})
    confirm_password = PasswordField("Password", validators=[DataRequired("The length of password must be from 4 to 10 symbols"), Length(min=4, max=10)], render_kw={'placeholder': 'Confirm your password: '})
    submit = SubmitField("Submit")

class ToDoForm(FlaskForm):
    title = StringField('Todo Title', validators=[DataRequired("This field is required"), Length(min=1, max=100)])
    description = StringField('', validators=[DataRequired("This field is required"), Length(min=1 , max=200)])
    submit = SubmitField("Add new task")

class FeedbackForm(FlaskForm):
    username = StringField('Feedback Username', validators=[DataRequired("This field is required"), Length(min=1, max=100)])
    feedback = StringField('', validators=[DataRequired("This field is required"), Length(min=1 , max=200)])
    submit = SubmitField("Add new task")

class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="This field is required and must have length between 4 and 25 symbols"), Length(min=4, max=25),
    Regexp('^[A-Za-z][A-Za-z0-9_.]*$', message='Username must have only letters, numbers, dots or underscores')], render_kw={'placeholder': 'Enter your username: '})

    email = StringField("Email", validators=[DataRequired(message="This field is required"), Email()],
    render_kw={'placeholder': 'Enter your email: '})

    password = PasswordField("Password", validators=[DataRequired(message="This field is required"), Length(min=6)],
    render_kw={'placeholder': 'Enter your password: '})

    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(message="This field is required"), Length(min=6),
    EqualTo('password', message='The confirmation input is not equal to password input.')], render_kw={'placeholder': 'Enter your password: '})

    image_file = FileField("Choose Image")

    submit = SubmitField('Sign up')

    def validate_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('The user with such email has been already registered.')

    def validate_username(self, field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('This username is already in use.')

