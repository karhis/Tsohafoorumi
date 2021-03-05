from flask import Blueprint, render_template

create = Blueprint('create',__name__,url_prefix='/create')

@create.route("/thread/<subforum_id>")
def newthread(subforum_id):
    return render_template("newthread.html", subforum_id=subforum_id)

@create.route("/subforum/<forum_id>")
def newsubforum(forum_id):
    return render_template("newforum.html", forum_id=forum_id)

@create.route("/forum")
def newforum():
    return render_template("newforum.html")

