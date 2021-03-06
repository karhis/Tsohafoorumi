from flask import Blueprint, render_template
from forms import ForumForm, ThreadForm

create = Blueprint('create',__name__,url_prefix='/create')

@create.route("/thread/<subforum_id>")
def newthread(subforum_id):
    form = ThreadForm()
    return render_template("newthread.html", subforum_id=subforum_id, form=form)

@create.route("/subforum/<forum_id>")
def newsubforum(forum_id):
    form = ForumForm()
    return render_template("newforum.html", forum_id=forum_id, form=form)

@create.route("/forum")
def newforum():
    form = ForumForm()
    return render_template("newforum.html", form=form)

