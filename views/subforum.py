from data import threads
from data import messages
from data import forums
from flask import Blueprint, render_template

subforum = Blueprint('subforum',__name__,url_prefix="/subforum")

@subforum.route("/<subforum_id>")
def subforumpage(subforum_id):
    titles = threads.get_thread_info(subforum_id)
    titles.sort(key=lambda tup: (tup[9], tup[8]), reverse=True)
    subforum_info = forums.get_subforum_info(subforum_id)
    forum_name = forums.get_forum_name(subforum_info[1])
    return render_template("subforum.html", titles=titles, subforum_id=subforum_id, forum_id=subforum_info[1], subforum_name=subforum_info[0], forum_name=forum_name)
