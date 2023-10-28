from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired(message="This field is required")], render_kw={'placeholder': 'Enter your username: '})
    password = PasswordField("Password",validators=[DataRequired("The length of password must be from 4 to 10 symbols"), Length(min=4, max=10)], render_kw={'placeholder': 'Enter your password: '})
    remember = BooleanField("Keep me logged in:",default='unchecked', render_kw={'placeholder': 'Keep me logged in: '})
    submit = SubmitField("Sign In")

class ChangePasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired("The length of password must be from 4 to 10 symbols"), Length(min=4, max=10)], render_kw={'placeholder': 'Enter your password: '})
    confirm_password = PasswordField("Password", validators=[DataRequired("The length of password must be from 4 to 10 symbols"), Length(min=4, max=10)], render_kw={'placeholder': 'Confirm your password: '})
    submit = SubmitField("Submit")

