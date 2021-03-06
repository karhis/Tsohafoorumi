from flask.signals import message_flashed
from wtforms import Form, StringField, PasswordField, validators

class RegistartionForm(Form):
    username = StringField('Käyttäjätunnus', [validators.InputRequired(message='Käyttäjätunnus ei voi olla tyhjä'), validators.Length(min=1, max=32, message='Käyttäjätunnuksen on oltava 1-32 merkkiä'), validators.Regexp('^\S+$', message="Käyttäjätunnuksessa ei voi olla välilyöntejä")])
    password = PasswordField('Salasana', [validators.InputRequired(message='Salasana ei voi olla tyhjä'), validators.Length(min=6, max=32), validators.EqualTo('confirm', message='Salasanat eivät täsmää')])
    confirm = PasswordField('Vahvista salasana')

class LoginForm(Form):
    username = StringField('Käyttäjätunnus', [validators.InputRequired(message='Käyttäjätunnus ei voi olla tyhjä')])
    password = PasswordField('Salasana', [validators.InputRequired(message='Salasana ei voi olla tyhjä')])

class SignatureForm(Form):
    signature = StringField('Muokkaa, tai lisää allekirjoitus:', [validators.InputRequired(message='Allekirjoitus ei voi olla tyhjä'), validators.Length(min=1, max=120, message='Allekirjoitus on oltava 1-120 merkkiä')])