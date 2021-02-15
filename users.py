from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash


def login(username,password):
    sql ="SELECT pass, id, admin FROM users WHERE name=:username AND visible=1"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["username"] = user[1]
            return True
        else:
            return False

def logout():
    del session["username"]

def register(username,password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (name, pass) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return True
    except:
        return False

def get_userlist():
    sql = "SELECT id, name, date FROM users WHERE visible=1 ORDER BY id DESC"
    result = db.session.execute(sql)
    users = result.fetchall()
    return users

def get_user_query(query):
    sql = "SELECT id, name FROM users WHERE visible=1 AND name LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    users = result.fetchall()
    return users

def get_username(id):
    sql = "SELECT name FROM users WHERE visible=1 AND id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]