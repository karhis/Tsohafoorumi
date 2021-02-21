from db import db

def get_message_query(query):
    sql = "SELECT M.id, M.content, M.thread_id, U.name, U.id FROM messages M, users U WHERE M.visible=1 AND M.sent_to IS NULL AND U.id=M.created_by AND content LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    messages = result.fetchall()
    return messages

def delete_message(message_id):
    sql = "UPDATE messages SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":message_id})
    db.session.commit()

def get_sent_dms(id,username):
    sql = "SELECT * FROM messages WHERE created_by=:created_by AND sent_to=:sent_to"
    result = db.session.execute(sql, {"created_by":username, "sent_to":id})
    sent_dms = result.fetchall()
    return sent_dms

def get_gotten_dms(id,username):
    sql = "SELECT * FROM messages WHERE created_by=:created_by AND sent_to=:sent_to"
    result = db.session.execute(sql, {"created_by":id, "sent_to":username})
    gotten_dms = result.fetchall()
    return gotten_dms

def send_dm(message, sent_to, id):
    sql = "INSERT INTO messages (content, created_by, sent_to) VALUES (:message, :created_by, :sent_to)"
    db.session.execute(sql, {"message":message, "created_by":id, "sent_to":sent_to})
    db.session.commit()

def send_reply(message, thread_id, id):
    sql = "INSERT INTO messages (content, thread_id, created_by) VALUES (:message, :thread_id, :by)"
    db.session.execute(sql, {"message":message, "thread_id":thread_id, "by":id})
    db.session.commit()

def get_replys_titles(id):
    sql = "SELECT M.id, M.content, M.thread_id, M.date, T.title FROM messages M, threads T WHERE M.visible=1 AND M.created_by=:id AND T.id=M.thread_id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def get_replys(thread_id):
    sql = "SELECT M.id, M.content, M.created_by, M.date, U.name FROM messages M, users U WHERE thread_id=:id AND M.visible=1 AND M.created_by=U.id"
    result = db.session.execute(sql, {"id":thread_id})
    return result.fetchall()

def get_latest_reply(subforum_id):
    sql = "SELECT M.date, U.name, T.id FROM messages M LEFT OUTER JOIN threads T ON T.subforum_id=11 LEFT OUTER JOIN users U ON U.id=M.created_by WHERE M.visible=1 GROUP BY M.date, U.name, T.id"
    result = db.session.execute(sql, {"subforum_id":subforum_id})
    return result.fetchall()