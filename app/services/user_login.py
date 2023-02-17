import db.db_conn as db_conn
import models.users as user_models
import bcrypt
import configs.conf as c
import bson.json_util as json_util

db = db_conn.connect_db()


users = db.get_collection("users")


def verify_pin(user_details: user_models.User_Login):
    try:
        user = users.find_one({"phone_no" : user_details.phone_no})
        dec_pass = bcrypt.checkpw(user_details.pin.encode() ,user['pin'])
        if dec_pass:
            return json_util._json_convert(
            {
                "error" : False,
                "uid" : user["uid"],
                "first_name" : user["first_name"],
                "last_name" : user["last_name"]
            })
        else:
            return json_util._json_convert(
                {
                    "error" : True,
                    "message" : "Pin is invalid"
                }
            )

    except StopIteration:
        pass
    