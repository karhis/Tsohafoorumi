from data import forums
from data import threads
from flask import Blueprint, render_template

home = Blueprint('home',__name__)

@home.route("/")
def index():
    forumlist = forums.get_all_forums()
    subforumlist = forums.get_all_subforums()
    total_thread_amount = threads.get_thread_count()
    return render_template("index.html", total_thread_amount=total_thread_amount, forumlist=forumlist, subforumlist=subforumlist)
