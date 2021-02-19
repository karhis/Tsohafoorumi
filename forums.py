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

def get_subforum_name(subforum_id):
    sql = "SELECT name FROM subforums WHERE visible=1 AND id=:subforum_id"
    result = db.session.execute(sql, {"subforum_id":subforum_id})
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

def delete_forum(forum_id):
    sql = "UPDATE forums SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":forum_id})
    sql = "UPDATE subforums SET visible=0 WHERE forum_id=:forum_id RETURNING id"
    result = db.session.execute(sql, {"forum_id":forum_id})
    subforumlist = result.fetchall()
    threadlist = []
    for subforum in subforumlist:
        sql = "UPDATE threads SET visible=0 WHERE subforum_id=:subforum_id RETURNING id"
        result = db.session.execute(sql, {"subforum_id":subforum[0]})
        queryids = result.fetchall()
        for query in queryids:
            threadlist.append(query[0])
    for thread in threadlist:
        sql = "UPDATE messages SET visible=0 WHERE thread_id=:thread_id"
        db.session.execute(sql, {"thread_id":thread})
    db.session.commit()

def delete_subforum(subforum_id):
    sql = "UPDATE subforums SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":subforum_id})
    sql = "UPDATE threads SET visible=0 WHERE subforum_id=:subforum_id RETURNING id"
    result = db.session.execute(sql, {"subforum_id":subforum_id})
    threadlist = result.fetchall()
    for thread in threadlist:
        sql = "UPDATE messages SET visible=0 WHERE thread_id=:thread_id"
        db.session.execute(sql, {"thread_id":thread[0]})
    db.session.commit()