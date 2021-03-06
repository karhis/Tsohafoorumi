from wtforms import Form, StringField, PasswordField, validators

class RegistartionForm(Form):
    username = StringField('Käyttäjätunnus', [validators.InputRequired(message='Käyttäjätunnus ei voi olla tyhjä'), validators.Length(min=1, max=32, message='Käyttäjätunnuksen on oltava 1-32 merkkiä'), validators.Regexp('^\S+$', message="Käyttäjätunnuksessa ei voi olla välilyöntejä")])
    password = PasswordField('Salasana', [validators.InputRequired(message='Salasana ei voi olla tyhjä'), validators.Length(min=6, max=32, message='Salasanan on oltava 6-32 merkkiä'), validators.EqualTo('confirm', message='Salasanat eivät täsmää')])
    confirm = PasswordField('Vahvista salasana')

class LoginForm(Form):
    username = StringField('Käyttäjätunnus', [validators.InputRequired(message='Käyttäjätunnus ei voi olla tyhjä')])
    password = PasswordField('Salasana', [validators.InputRequired(message='Salasana ei voi olla tyhjä')])

class SignatureForm(Form):
    signature = StringField('Muokkaa, tai lisää allekirjoitus:', [validators.InputRequired(message='Allekirjoitus ei voi olla tyhjä'), validators.Length(min=1, max=120, message='Allekirjoitus on oltava 1-120 merkkiä')])

class MessageForm(Form):
    message = StringField('Viesti:', [validators.InputRequired(message='Viesti ei voi olla tyhjä')])

class ForumForm(Form):
    title = StringField('Nimi:', [validators.InputRequired(message='Nimi ei voi olla tyhjä'), validators.Length(min=1, max=120, message='Nimen on oltava 1-120 merkkiä')])
    description = StringField('Vapaaehtoinen kuvaus:', [validators.Length(max=240, message='Kuvauksen on oltava max 240 merkkiä')])

class ThreadForm(Form):
    title = StringField('Otsikko:', [validators.InputRequired(message='Otsikko ei voi olla tyhjä'), validators.Length(min=1, max=120, message='Otsikon on oltava 1-120 merkkiä')])
    message = StringField('Viesti:', [validators.InputRequired(message='Viesti ei voi olla tyhjä')])