from data.db import db

def get_thread_info(subforum_id):
    sql = """SELECT T.id, T.title, T.created_by, T.date, T.locked, U.name,  
                    COUNT(DISTINCT M.id), COUNT(DISTINCT L.id) AS THANKCOUNT, 
                    MAX(M.date) 
               FROM threads T 
                    LEFT OUTER JOIN messages M 
                    ON T.id = M.thread_id 
                       AND M.visible 
                       
                    LEFT OUTER JOIN users U 
                    ON U.id=T.created_by 

                    LEFT OUTER JOIN thanks L 
                    ON T.id=L.thread_id 
                       AND L.visible 
              WHERE T.visible 
                    AND T.subforum_id=:subforum_id
              GROUP BY T.id, U.name"""
    result = db.session.execute(sql, {"subforum_id":subforum_id})
    return result.fetchall()

def get_thread_count():
    sql = """SELECT COUNT(*) 
               FROM threads 
              WHERE visible"""
    result = db.session.execute(sql)
    return result.fetchone()[0]

def get_thread_query(query):
    sql = """SELECT T.id, T.title, T.created_by, T.date, U.name, T.subforum_id, S.forum_id 
               FROM threads T
                    LEFT OUTER JOIN users U
                    ON T.created_by=U.id 

                    LEFT OUTER JOIN subforums S
                    ON T.subforum_id=S.id
              WHERE T.visible 
                    AND T.title LIKE :query
              GROUP BY T.id, U.name, S.forum_id"""
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()

def delete_thread(thread_id):
    sql = """UPDATE threads 
                SET visible=False 
              WHERE id=:thread_id"""
    db.session.execute(sql, {"thread_id":thread_id})
    sql = """UPDATE messages 
                SET visible=False 
              WHERE thread_id=:thread_id"""
    db.session.execute(sql, {"thread_id":thread_id})
    db.session.commit()

def new(title,username,subforum_id):
    try:
        sql = """INSERT INTO threads (title, created_by, subforum_id) 
                VALUES (:title, :by, :subforum_id) 
                RETURNING id"""
        result = db.session.execute(sql, {"title":title, "by":username, "subforum_id":subforum_id})
        return True, result.fetchone()[0]
    except:
        return False

def get_title(thread_id):
    sql = """SELECT title, locked, subforum_id 
               FROM threads 
              WHERE id=:id 
                    AND visible """
    result = db.session.execute(sql, {"id":thread_id})
    return result.fetchone()

def lock_thread(thread_id):
    sql = """UPDATE threads 
                SET locked=True 
              WHERE id=:id"""
    db.session.execute(sql, {"id":thread_id})
    db.session.commit()

def unlock_thread(thread_id):
    sql = """UPDATE threads 
                SET locked=False 
              WHERE id=:id"""
    db.session.execute(sql, {"id":thread_id})
    db.session.commit()

