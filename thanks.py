from db import db

def get_all_thanks():
    sql = "SELECT thread_id, message_id, COUNT(*) FROM thanks WHERE visible GROUP BY thread_id, message_id"
    result = db.session.execute(sql)
    thanks = result.fetchall()
    return thanks

def thank_message(message_id,username):
    try:
        sql = "INSERT INTO thanks (message_id, created_by) VALUES (:message_id, :created_by)"
        db.session.execute(sql, {"message_id":message_id, "created_by":username})
        db.session.commit()
        return True
    except:
        return False

def thank_thread(thread_id,username):
    try:
        sql = "INSERT INTO thanks (thread_id, created_by) VALUES (:thread_id, :created_by)"
        db.session.execute(sql, {"thread_id":thread_id, "created_by":username})
        db.session.commit()
        return True
    except:
        return False
