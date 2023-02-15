import models.users as user_model
import db.db_conn as db_conn

db = db_conn.connect_db()
users = db.get_collection("users")

def find_user_by_pno(data: user_model.User_Check_Pno):
    user = users.find({"phone_no" : data.phone_no})
    c = 0
    try:
        user.next()
        c += 1
    except StopIteration:
        pass
    
    if user.retrieved > 0:
        return 1
    else:
        return -1