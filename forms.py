from wtforms import Form, StringField, PasswordField, validators

class RegistartionForm(Form):
    username = StringField('Käyttäjätunnus', [validators.InputRequired(), validators.Length(min=1, max=32)])
    password = PasswordField('Salasana', [validators.InputRequired(), validators.EqualTo('confirm', message='Salasanat eivät täsmää')])
    confirm = PasswordField('Vahvista salasana')

class LoginForm(Form):
    username = StringField('Käyttäjätunnus', [validators.InputRequired(), validators.Length(min=1, max=32)])
    password = PasswordField('Salasana', [validators.InputRequired()])