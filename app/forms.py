from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, BooleanField, PasswordField, validators, TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    #remember_me = BooleanField('remember_me', default=False)

