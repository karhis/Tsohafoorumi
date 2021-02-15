from app import app
import thanks
import threads
import messages
import users
from flask import request, redirect, render_template, session


@app.route("/")
def index():
    titles = threads.get_thread_info()
    all_thanks = thanks.get_all_thanks()
    amount = threads.get_thread_count()
    return render_template("index.html", titles=titles, amount=amount, thanks=all_thanks)

@app.route("/new")
def new():
    return render_template("new.html")

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
    if delete_type == "1":          #1 for messages, 0 for threads
        messages.delete_message(delete_id)
        return redirect("/")
    else: 
        threads.delete_thread(delete_id)
        return redirect("/")

@app.route("/profile/<id>/chat", methods=["GET"])
def chat(id):
    session_username = session["username"]
    sent_dms = messages.get_sent_dms(id,session_username)
    gotten_dms = messages.get_gotten_dms(id,session_username)
    username = users.get_username(id)
    dms = sent_dms + gotten_dms
    dms.sort()
    return render_template("chat.html", dms=dms, id=id, username=username)

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
    username = users.get_username(id)
    return render_template("profile.html", messages=replys, id=id, username=username)

@app.route("/create", methods=["POST"])
def send():
    title = request.form["title"]
    username = session["username"]
    thread_id = threads.new(title, username)
    message = request.form["message"]
    messages.send_reply(message, thread_id, username)
    return redirect("/")

@app.route("/thread/<int:id>")
def thread(id):
    title = threads.get_title(id)
    replys = messages.get_replys(id)
    likes = thanks.get_all_thanks()
    return render_template("thread.html", title=title, messages=replys, id=id, thanks=likes)


