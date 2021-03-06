from data.db import db

def get_all_forums():
    sql = """SELECT id, name 
               FROM forums 
              WHERE visible"""
    result = db.session.execute(sql)
    return result.fetchall()

def get_all_subforums():
    sql = """SELECT S.id, S.name, S.descri, S.forum_id, COUNT(DISTINCT T.id), COUNT(DISTINCT M.id), MAX(M.date) 
               FROM subforums S 
                    LEFT OUTER JOIN threads T 
                    ON S.id = T.subforum_id 
                       AND T.visible 
                       
                    LEFT OUTER JOIN messages M 
                    ON T.id = M.thread_id 
                       AND M.visible 
              WHERE S.visible GROUP BY S.id"""
    result = db.session.execute(sql)
    return result.fetchall()

def get_subforums(forum_id):
    sql = """SELECT S.id, S.name, S.descri, COUNT(DISTINCT T.id), COUNT(DISTINCT M.id), MAX(M.date) 
               FROM subforums S 
                    LEFT OUTER JOIN threads T 
                    ON S.id = T.subforum_id 
                       AND T.visible 
                       
                    LEFT OUTER JOIN messages M 
                    ON T.id = M.thread_id 
                       AND M.visible 
              WHERE S.visible 
                    AND S.forum_id=:forum_id 
              GROUP BY S.id"""
    result = db.session.execute(sql, {"forum_id":forum_id})
    return result.fetchall()

def get_forum_name(forum_id):
    sql = """SELECT name 
               FROM forums 
              WHERE visible 
                    AND id=:forum_id"""
    result = db.session.execute(sql, {"forum_id":forum_id})
    return result.fetchone()[0]

def get_subforum_info(subforum_id):
    sql = """SELECT name, forum_id 
               FROM subforums 
              WHERE visible 
                    AND id=:subforum_id"""
    result = db.session.execute(sql, {"subforum_id":subforum_id})
    return result.fetchone()

def new_forum(name):
    try:
        sql = """INSERT INTO forums (name) 
                VALUES (:name)"""
        db.session.execute(sql, {"name":name})
        db.session.commit()
        return True
    except:
        return False

def new_subforum(name,descri,forum_id):
    try:
        sql = """INSERT INTO subforums (name, descri, forum_id) 
                VALUES (:name, :descri, :forum_id)"""
        db.session.execute(sql, {"name":name, "descri":descri, "forum_id":forum_id})
        db.session.commit()
        return True
    except:
        return False

def delete_forum(forum_id):
    sql = """UPDATE forums 
                SET visible=False 
              WHERE id=:id"""
    db.session.execute(sql, {"id":forum_id})
    sql = """UPDATE subforums 
                SET visible=False 
              WHERE forum_id=:forum_id 
          RETURNING id"""
    result = db.session.execute(sql, {"forum_id":forum_id})
    subforumlist = result.fetchall()
    threadlist = []
    for subforum in subforumlist:
        sql = """UPDATE threads 
                    SET visible=False 
                  WHERE subforum_id=:subforum_id 
              RETURNING id"""
        result = db.session.execute(sql, {"subforum_id":subforum[0]})
        queryids = result.fetchall()
        for query in queryids:
            threadlist.append(query[0])
    for thread in threadlist:
        sql = """UPDATE messages 
                    SET visible=False 
                  WHERE thread_id=:thread_id"""
        db.session.execute(sql, {"thread_id":thread})
    db.session.commit()

def delete_subforum(subforum_id):
    sql = """UPDATE subforums 
                SET visible=False 
              WHERE id=:id"""
    db.session.execute(sql, {"id":subforum_id})
    sql = """UPDATE threads 
                SET visible=False 
              WHERE subforum_id=:subforum_id 
          RETURNING id"""
    result = db.session.execute(sql, {"subforum_id":subforum_id})
    threadlist = result.fetchall()
    for thread in threadlist:
        sql = """UPDATE messages 
                    SET visible=False 
                  WHERE thread_id=:thread_id"""
        db.session.execute(sql, {"thread_id":thread[0]})
    db.session.commit()