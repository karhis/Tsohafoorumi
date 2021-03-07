from data import messages
from data import users
from data import threads
from flask import Blueprint, render_template, request

result = Blueprint('result',__name__)

@result.route("/result", methods=["GET"])
def resultpage():
    query = request.args["query"]
    replys = messages.get_message_query(query)
    usernames = users.get_user_query(query)
    threadlist = threads.get_thread_query(query)
    return render_template("result.html", messages=replys, users=usernames, threadlist=threadlist)
