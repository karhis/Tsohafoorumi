from app import app
import thanks
import threads
import messages
import users
import forums
from flask import request, redirect, render_template, session


@app.route("/")
def index():
    forumlist = forums.get_all_forums()
    subforumlist = forums.get_all_subforums()
    total_thread_amount = threads.get_thread_count()
    return render_template("index.html", total_thread_amount=total_thread_amount, forumlist=forumlist, subforumlist=subforumlist)


@app.route("/forum/<forum_id>")
def forum(forum_id):
    subforumlist = forums.get_subforums(forum_id)
    forumname = forums.get_forum_name(forum_id)
    forum_id = forum_id
    return render_template("forum.html", subforumlist=subforumlist, forum_id=forum_id, forumname=forumname)

@app.route("/forum/<forum_id>/sub/<subforum_id>")
def subforum(forum_id,subforum_id):
    titles = threads.get_thread_info(subforum_id)
    subforum_id = subforum_id
    latest_reply = messages.get_latest_reply(subforum_id)
    subforum_name = forums.get_subforum_name(subforum_id)
    forum_id = forum_id
    return render_template("subforum.html", titles=titles, subforum_id=subforum_id, forum_id=forum_id, subforum_name=subforum_name, latest_reply=latest_reply)

@app.route("/createforum", methods=["POST"])
def createforum():
    forumname = request.form["forumname"]
    forum_type = request.form["forum_type"]
    if forum_type == "1":
        forum_id = request.form["forum_id"]
        descri = request.form["descri"]
        forums.new_subforum(forumname,descri,forum_id)
        return redirect("/")
    else:
        forums.new_forum(forumname)
        return redirect("/")

@app.route("/newforum")
def newforum():
    return render_template("newforum.html")


@app.route("/forum/<forum_id>/newforum")
def newsubforum(forum_id):
    forum_id = forum_id
    return render_template("newforum.html", forum_id=forum_id)


@app.route("/forum/<forum_id>/sub/<subforum_id>/new")
def new(forum_id,subforum_id):
    subforum_id = subforum_id
    return render_template("new.html", subforum_id=subforum_id)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username,password):
        return redirect("/")
    else:
        return render_template("error.html",error_message="Sisäänkirjautuminen epäonnistui, väärä käyttäjätunnus tai salasana.")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["POST"])
def register():
    password = request.form["pass"]
    username = request.form["name"]
    if users.register(username,password):
        return redirect("/")
    else:
        return render_template("error.html",error_message="Rekisteröityminen epäonnistui.")

@app.route("/userlist")
def userlist():
    userslist = users.get_userlist()
    return render_template("/userlist.html", users=userslist)        

@app.route("/result", methods=["GET"])
def result():
    query = request.args["query"]
    replys = messages.get_message_query(query)
    usernames = users.get_user_query(query)
    thread_titles = threads.get_thread_query(query)
    return render_template("result.html", messages=replys, users=usernames, threads=thread_titles)

@app.route("/thank", methods=["POST"])
def thank():
    username = session["username"]
    message_id = request.form["message_id"]
    thread_id = request.form["thread_id"]
    thanks.thank(thread_id,message_id,username)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():   
    delete_id = request.form["delete_id"]
    delete_type = request.form["delete_type"]
    if delete_type == "1":          #1 for messages, 0 for threads, 2 for forums, 3 for subforums
        messages.delete_message(delete_id)
        return redirect("/")
    if delete_type == "2":
        forums.delete_forum(delete_id)
        return redirect("/")
    if delete_type == "3":
        forums.delete_subforum(delete_id)
        return redirect("/")
    else: 
        threads.delete_thread(delete_id)
        return redirect("/")

@app.route("/profile/<id>/chat", methods=["GET"])
def chat(id):
    session_username = session["username"]
    sent_dms = messages.get_sent_dms(id,session_username)
    gotten_dms = messages.get_gotten_dms(id,session_username)
    profile= users.get_profile(id)
    dms = sent_dms + gotten_dms
    dms.sort()
    return render_template("chat.html", dms=dms, id=id, profile=profile)

@app.route("/reply", methods=["POST"])
def reply():
    username = session["username"]
    message = request.form["message"]
    reply_type = request.form["reply_type"]
    if reply_type == "1":
        sent_to = request.form["sent_to"]
        messages.send_dm(message, sent_to, username)
        return redirect("/profile/"+str(sent_to)+"/chat")
    else:
        thread_id = request.form["thread_id"]
        messages.send_reply(message, thread_id, username)
        return redirect("/thread/"+str(thread_id))

@app.route("/profile/<id>")
def profile(id):
    replys = messages.get_replys_titles(id)
    profile = users.get_profile(id)
    return render_template("profile.html", messages=replys, id=id, profile=profile)

@app.route("/create", methods=["POST"])
def send():
    title = request.form["title"]
    username = session["username"]
    subforum_id = request.form["subforum_id"]
    thread_id = threads.new(title, username, subforum_id)
    message = request.form["message"]
    messages.send_reply(message, thread_id, username)
    return redirect("/")


@app.route("/thread/<id>")
def thread(id):
    title = threads.get_title(id)
    locked = threads.get_locked(id)
    replys = messages.get_replys(id)
    likes = thanks.get_all_thanks()
    return render_template("thread.html", title=title, locked=locked, messages=replys, id=id, thanks=likes)

@app.route("/lock", methods=["POST"])
def lock():   
    lock_id = request.form["lock_id"]
    lock_type = request.form["lock_type"]
    if lock_type == "1":
        threads.lock_thread(lock_id)
        return redirect("/")
    else:
        threads.unlock_thread(lock_id)
        return redirect("/")

@app.route("/ban", methods=["POST"])
def ban():
    ban_id = request.form["ban_id"]
    ban_type = request.form["ban_type"]
    if ban_type == "1":
        users.ban_user(ban_id)
        return redirect("/")
    else:
        users.unban_user(ban_id)
        return redirect("/")
    
    


