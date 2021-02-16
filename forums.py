from db import db

def get_all_forums():
    sql = "SELECT id, name FROM forums WHERE visible=1"
    result = db.session.execute(sql)
    forumlist = result.fetchall()
    return forumlist

def get_all_subforums():
    sql = "SELECT id, name, descri, forum_id FROM subforums WHERE visible=1"
    result = db.session.execute(sql)
    subforumlist = result.fetchall()
    return subforumlist

def get_subforums(forum_id):
    sql = "SELECT id, name, descri, forum_id FROM subforums WHERE visible=1 AND forum_id=:forum_id"
    result = db.session.execute(sql, {"forum_id":forum_id})
    subforumlist = result.fetchall()
    return subforumlist

def get_forum_name(forum_id):
    sql = "SELECT name FROM forums WHERE visible=1 AND id=:forum_id"
    result = db.session.execute(sql, {"forum_id":forum_id})
    name = result.fetchone()[0]
    return name

def new_forum(name):
    sql = "INSERT INTO forums (name) VALUES (:name)"
    result = db.session.execute(sql, {"name":name})
    db.session.commit()

def new_subforum(name,descri,forum_id):
    sql = "INSERT INTO subforums (name, descri, forum_id) VALUES (:name, :descri, :forum_id)"
    db.session.execute(sql, {"name":name, "descri":descri, "forum_id":forum_id})
    db.session.commit()