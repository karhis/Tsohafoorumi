from db import db

def get_thread_info(subforum_id):
    sql = "SELECT T.id, T.title, T.created_by, T.date, T.locked, U.name, COUNT(DISTINCT M.id), COUNT(DISTINCT L.id) AS THANKCOUNT, MAX(M.date) FROM threads T LEFT OUTER JOIN messages M ON T.id = M.thread_id AND M.visible LEFT OUTER JOIN users U ON U.id=T.created_by LEFT OUTER JOIN thanks L ON T.id=L.thread_id AND L.visible WHERE T.visible AND T.subforum_id=:subforum_id GROUP BY T.id, U.name"
    result = db.session.execute(sql, {"subforum_id":subforum_id})
    titles = result.fetchall()
    return titles

def get_thread_count():
    sql = "SELECT COUNT(*) FROM threads WHERE visible"
    result = db.session.execute(sql)
    amount = result.fetchone()[0]
    return amount

def get_thread_query(query):
    sql = "SELECT T.id, T.title, T.created_by, T.date, U.name, T.locked FROM threads T, users U WHERE T.visible AND U.id=T.created_by AND T.title LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    threads = result.fetchall()
    return threads

def delete_thread(thread_id):
    sql = "UPDATE threads SET visible=False WHERE id=:id"
    db.session.execute(sql, {"id":thread_id})
    sql = "UPDATE messages SET visible=False WHERE thread_id=:id"
    db.session.execute(sql, {"id":thread_id})
    db.session.commit()

def new(title, username, subforum_id):
    sql = "INSERT INTO threads (title, created_by, subforum_id) VALUES (:title, :by, :subforum_id) RETURNING id"
    result = db.session.execute(sql, {"title":title, "by":username, "subforum_id":subforum_id})
    return result.fetchone()[0]

def get_title(thread_id):
    sql = "SELECT T.title FROM threads T WHERE T.id=:id AND T.visible GROUP BY T.title"
    result = db.session.execute(sql, {"id":thread_id})
    title = result.fetchone()[0]
    return title

def get_locked(thread_id):
    sql = "SELECT locked FROM threads WHERE id=:id AND visible"
    result = db.session.execute(sql, {"id":thread_id})
    locked = result.fetchone()[0]
    return locked

def lock_thread(thread_id):
    sql = "UPDATE threads SET locked=True WHERE id=:id"
    db.session.execute(sql, {"id":thread_id})
    db.session.commit()

def unlock_thread(thread_id):
    sql = "UPDATE threads SET locked=False WHERE id=:id"
    db.session.execute(sql, {"id":thread_id})
    db.session.commit()

