import db.db_conn as db_conn
import configs.conf as c
from pydantic import BaseModel, validator, ValidationError
import bcrypt

db = db_conn.connect_db()

users = db.get_collection("users")

class User(BaseModel):
    first_name : str
    last_name: str
    phone_no: str
    pin: str

    @validator("phone_no")
    def phone_no_check(cls, pno):
        if len(pno) != 10:
            raise ValueError("phone no. must be of 10 digits")
        return pno

def insert_new_user(user_details: User): 
    enc_pin = bcrypt.hashpw(user_details.pin.encode(), c.Config.salt)
    user_data_enc = {
        "first_name" : user_details.first_name,
        "last_name" : user_details.last_name,
        "phone_no" : user_details.phone_no,
        "pin" : enc_pin
    }
    val = users.insert_one(user_data_enc)
    return val.inserted_id

