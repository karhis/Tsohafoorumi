from data import threads
from data import forums
from data import messages
from flask import Blueprint, render_template
from forms import MessageForm

thread = Blueprint('thread',__name__,url_prefix='/thread')

@thread.route("/<thread_id>")
def threadpage(thread_id):
    title = threads.get_title(thread_id)
    replys = messages.get_replys(thread_id)
    subforum_info = forums.get_subforum_info(title[2])
    forum_name = forums.get_forum_name(subforum_info[1])
    form = MessageForm()
    return render_template("thread.html", title=title, locked=title[1], sticky=title[3], messages=replys, thread_id=thread_id, subforum_name=subforum_info[0], forum_name=forum_name, forum_id=subforum_info[1], subforum_id=title[2], form=form)
