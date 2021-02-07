from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash



app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)



@app.route("/")
def index():
    sql = "SELECT T.id, T.title, T.created_by, T.date, U.name FROM threads T, users U WHERE T.visible=1 AND T.created_by=U.id ORDER BY date DESC"
    result = db.session.execute(sql)
    titles = result.fetchall()
    sql = "SELECT thread_id, COUNT(*) FROM thanks WHERE visible=1 GROUP BY thread_id"
    result = db.session.execute(sql)
    thanks = result.fetchall()
    sql = "SELECT COUNT(*) FROM threads WHERE visible=1"
    result = db.session.execute(sql)
    amount = result.fetchone()[0]
    return render_template("index.html", titles=titles, amount=amount, thanks=thanks)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/reply", methods=["POST"])
def reply():
    thread_id = request.form["id"]
    message = request.form["message"]
    sql = "INSERT INTO messages (content, thread_id, created_by) VALUES (:message, :thread_id, :by)"
    db.session.execute(sql, {"message":message, "thread_id":thread_id, "by":session["username"]})
    db.session.commit()
    return redirect("/thread/"+str(thread_id))

@app.route("/thank_message", methods=["POST"])
def thank_message():
        message_id = request.form["message_id"]
        sql = "INSERT INTO thanks (message_id, created_by) VALUES (:message_id, :created_by)"
        db.session.execute(sql, {"message_id":message_id, "created_by":session["username"]})
        db.session.commit()
        return redirect("/")

@app.route("/thank_thread", methods=["POST"])
def thank_thread():
        thread_id = request.form["thread_id"]
        sql = "INSERT INTO thanks (thread_id, created_by) VALUES (:thread_id, :created_by)"
        db.session.execute(sql, {"thread_id":thread_id, "created_by":session["username"]})
        db.session.commit()
        return redirect("/")

@app.route("/create", methods=["POST"])
def send():
    title = request.form["title"]
    sql = "INSERT INTO threads (title, created_by) VALUES (:title, :by) RETURNING id"
    result = db.session.execute(sql, {"title":title, "by":session["username"]})
    thread_id = result.fetchone()[0]
    message = request.form["message"]
    sql = "INSERT INTO messages (content, thread_id, created_by) VALUES (:message, :thread_id, :by)"
    db.session.execute(sql, {"message":message, "thread_id":thread_id, "by":session["username"]})
    db.session.commit()
    return redirect("/")

@app.route("/thread/<int:id>")
def thread(id):
    sql = "SELECT title FROM threads WHERE id=:id AND visible=1"
    result = db.session.execute(sql, {"id":id})
    title = result.fetchone()[0]
    sql = "SELECT M.id, M.content, M.created_by, M.date, U.name FROM messages M, users U WHERE thread_id=:id AND M.visible=1 AND M.created_by=U.id"
    result = db.session.execute(sql, {"id":id})
    messages = result.fetchall()
    sql = "SELECT message_id, COUNT(*) FROM thanks WHERE visible=1 GROUP BY message_id"
    result = db.session.execute(sql)
    thanks = result.fetchall()
    return render_template("thread.html", title=title, messages=messages, id=id, thanks=thanks)


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql ="SELECT pass, id, admin FROM users WHERE name=:username AND visible=1"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return redirect("/loginerror")
    else:
        hash_value = user[0]
        if user[2] == True:
            session["admin"] = True
        else:
            session["admin"] = False
        if check_password_hash(hash_value,password):
            session["username"] = user[1]
            return redirect("/")
        else:
            return redirect("/loginerror")
    

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["POST"])
def register():
    password = request.form["pass"]
    name = request.form["name"]
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (name, pass) VALUES (:name, :password)"
        db.session.execute(sql, {"name":name, "password":hash_value})
        db.session.commit()
        return redirect("/")
    except:
        return redirect("/registererror")

@app.route("/registererror")
def registererror():
    return render_template("registererror.html")

@app.route("/loginerror")
def loginerror():
    return render_template("loginerror.html")

@app.route("/userlist")
def userlist():
    sql = "SELECT id, name, date FROM users WHERE visible=1 ORDER BY id DESC"
    result = db.session.execute(sql)
    users = result.fetchall()
    return render_template("/userlist.html", users=users)

@app.route("/result", methods=["GET"])
def result():
    query = request.args["query"]
    sql = "SELECT id, content, thread_id FROM messages WHERE visible=1 AND content LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    messages = result.fetchall()
    sql = "SELECT id, name FROM users WHERE visible=1 AND name LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    users = result.fetchall()
    sql = "SELECT T.id, T.title, T.created_by, T.date, U.name FROM threads T, users U WHERE T.visible=1 AND U.id=T.created_by AND T.title LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    threads = result.fetchall()
    return render_template("result.html", messages=messages, users=users, threads=threads)

@app.route("/profile/<id>")
def profile(id):
    sql = "SELECT M.id, M.content, M.thread_id, M.date, T.title FROM messages M, threads T WHERE M.visible=1 AND M.created_by=:id AND T.id=M.thread_id"
    result = db.session.execute(sql, {"id":id})
    messages = result.fetchall()
    sql = "SELECT name FROM users WHERE visible=1 AND id=:id"
    result = db.session.execute(sql, {"id":id})
    username = result.fetchone()[0]
    return render_template("profile.html", messages=messages, id=id, username=username)

@app.route("/delete_thread", methods=["POST"])
def delete_thread():
    thread_id = request.form["thread_id"]
    sql = "UPDATE threads SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":thread_id})
    sql = "UPDATE messages SET visible=0 WHERE thread_id=:id"
    db.session.execute(sql, {"id":thread_id})
    db.session.commit()
    return redirect("/")

@app.route("/delete_message", methods=["POST"])
def delete_message():
    message_id = request.form["message_id"]
    sql = "UPDATE messages SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":message_id})
    sql = "UPDATE messages SET visible=0 WHERE thread_id=:id"
    db.session.execute(sql, {"id":message_id})
    db.session.commit()
    return redirect("/")    

@app.route("/profile/<id>/chat", methods=["GET"])
def chat(id):
    sql = "SELECT * FROM messages WHERE created_by=:created_by AND sent_to=:sent_to"
    result = db.session.execute(sql, {"created_by":session["username"], "sent_to":id})
    sent_dms = result.fetchall()
    sql = "SELECT * FROM messages WHERE created_by=:created_by AND sent_to=:sent_to"
    result = db.session.execute(sql, {"created_by":id, "sent_to":session["username"]})
    got_dms = result.fetchall()
    sql = "SELECT name FROM users WHERE visible=1 AND id=:id"
    result = db.session.execute(sql, {"id":id})
    username = result.fetchone()[0]
    dms = sent_dms + got_dms
    dms.sort()
    return render_template("chat.html", dms=dms, id=id, username=username)

@app.route("/send_dm", methods=["POST"])
def send_dm():
    message = request.form["message"]
    sent_to = request.form["sent_to"]
    sql = "INSERT INTO messages (content, created_by, sent_to) VALUES (:content, :created_by, :sent_to)"
    db.session.execute(sql, {"content":message, "created_by":session["username"], "sent_to":sent_to})
    db.session.commit()
    return redirect("/")