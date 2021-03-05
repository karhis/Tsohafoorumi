from flask import Flask

app = Flask(__name__)

from routes import auth
from views.profile import profile
from views.home import home
from views.forum import forum
from views.subforum import subforum
from views.thread import thread
from views.userlist import userlist
from views.result import result
from views.create import create


app.register_blueprint(profile)
app.register_blueprint(home)
app.register_blueprint(forum)
app.register_blueprint(subforum)
app.register_blueprint(thread)
app.register_blueprint(userlist)
app.register_blueprint(result)
app.register_blueprint(create)
app.register_blueprint(auth)