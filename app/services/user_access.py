import models.users as user
import db.db_conn as db_conn

db = db_conn.connect_db()

def check_access(uid):
    auth_details = db.get_collection("angel_auth")
    u = user.find_by_uid(uid)
    if u is not None:
        return auth_details.find_one({"name" : "angel"}, {"name" : 0, "_id" : 0}) 
    else:
        return "User Not Found !"

