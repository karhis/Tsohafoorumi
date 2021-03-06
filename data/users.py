from data.db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username,password):
    sql = """SELECT pass, id, admin, banned 
               FROM users 
              WHERE name=:username 
                    AND visible"""
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            if user[2]:
                session["username"] = user[1]
                session["mod"] = True
                return True
            if user[3]:
                session["username"] = user[1]
                session["banned"] = True
                return True
            else:
                session["username"] = user[1]
                return True
        else:
            return False

def logout():
    session["mod"] = False
    session["banned"] = False
    del session["username"]

def register(username,password):
    hash_value = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (name, pass) 
                 VALUES (:username, :password)"""
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return True
    except:
        return False

def get_userlist():
    sql = """SELECT id, name, date 
               FROM users 
              WHERE visible 
           ORDER BY id DESC"""
    result = db.session.execute(sql)
    return result.fetchall()

def get_user_query(query):
    sql = """SELECT id, name 
               FROM users 
              WHERE visible 
                    AND name 
                    LIKE :query"""
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()

def ban_user(ban_id):
    sql = """UPDATE users 
                SET banned=True 
              WHERE id=:id"""
    db.session.execute(sql, {"id":ban_id})
    db.session.commit()

def unban_user(ban_id):
    sql = """UPDATE users 
                SET banned=False
              WHERE id=:id"""
    db.session.execute(sql, {"id":ban_id})
    db.session.commit()

def get_profile(id):
    sql = """SELECT name, banned, id, signature 
               FROM users 
              WHERE visible 
                    AND id=:id"""
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def add_signature(id,signature):
    sql = """UPDATE users
                SET signature=:signature
              WHERE id=:id"""
    db.session.execute(sql, {"id":id, "signature":signature})
    db.session.commit()