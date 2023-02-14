import db.db_conn as db_conn
import configs.conf as c
from pydantic import BaseModel

db = db_conn.connect_db()

users = db.get_collection("users")

class User(BaseModel):
    first_name : str
    last_name: str
    email_id: str
    pin: str


def insert_new_user(user_details: User): 
   
    user_data_enc = {
        "first_name" : user_details.first_name,
        "last_name" : user_details.last_name,
        "email_id" : user_details.email_id,
        "pin" : user_details.pin
    }
    val = users.insert_one(user_data_enc)
    return val.inserted_id

