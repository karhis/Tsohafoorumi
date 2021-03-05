from data import forums
from flask import Blueprint, render_template

forum = Blueprint('forum',__name__,url_prefix='/forum')

@forum.route("/<forum_id>")
def forumpage(forum_id):
    subforumlist = forums.get_subforums(forum_id)
    forumname = forums.get_forum_name(forum_id)
    return render_template("forum.html", subforumlist=subforumlist, forum_id=forum_id, forumname=forumname)
