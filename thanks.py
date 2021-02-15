from db import db


def get_all_thanks():
    sql = "SELECT thread_id, message_id, COUNT(*) FROM thanks WHERE visible=1 GROUP BY thread_id, message_id"
    result = db.session.execute(sql)
    thanks = result.fetchall()
    return thanks




def get_thanks():
    sql = "SELECT message_id, COUNT(*) FROM thanks WHERE visible=1 GROUP BY message_id"
    result = db.session.execute(sql)
    return result.fetchall()

def thank(thread_id,message_id,username):
    sql = "INSERT INTO thanks (thread_id, message_id, created_by) VALUES (:thread_id, :message_id, :created_by)"
    db.session.execute(sql, {"thread_id":thread_id, "message_id":message_id, "created_by":username})
    db.session.commit()

