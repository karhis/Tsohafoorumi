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
    sql = "SELECT id, title, created_by, thanks, date FROM threads ORDER BY id DESC"
    result = db.session.execute(sql)
    titles = result.fetchall()
    sql = "SELECT COUNT(*) FROM threads"
    result = db.session.execute(sql)
    amount = result.fetchone()[0]
    return render_template("index.html", titles=titles, amount=amount)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/reply", methods=["POST"])
def reply():
    thread_id = request.form["id"]
    message = request.form["message"]
    sql = "INSERT INTO messages (content, thread_id, created_by, thanks, date) VALUES (:message, :thread_id, 69, 0, NOW())"
    db.session.execute(sql, {"message":message, "thread_id":thread_id})
    db.session.commit()
    return redirect("/thread/"+str(thread_id))


@app.route("/create", methods=["POST"])
def send():
    title = request.form["title"]
    sql = "INSERT INTO threads (title, created_by, thanks, date) VALUES (:title, 69, 0, NOW()) RETURNING id"
    result = db.session.execute(sql, {"title":title})
    thread_id = result.fetchone()[0]
    message = request.form["message"]
    sql = "INSERT INTO messages (content, thread_id, created_by, thanks, date) VALUES (:message, :thread_id, 69, 0, NOW())"
    db.session.execute(sql, {"message":message, "thread_id":thread_id})
    db.session.commit()
    return redirect("/")

@app.route("/thread/<int:id>")
def thread(id):
    sql = "SELECT title FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    title = result.fetchone()[0]
    sql = "SELECT content, created_by, thanks, date FROM messages WHERE thread_id=:id"
    result = db.session.execute(sql, {"id":id})
    messages = result.fetchall()
    return render_template("thread.html", title=title, messages=messages, id=id)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")