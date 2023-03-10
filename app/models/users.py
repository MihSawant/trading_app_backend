import db.db_conn as db_conn
import configs.conf as c
from pydantic import BaseModel, validator, ValidationError
import bcrypt
from bson.objectid import ObjectId
import services.check_pno as check_pno
import bson.json_util as json_util
import uuid

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

class User_Check_Pno(BaseModel):
    phone_no: str

    @validator("phone_no")
    def phone_no_check(cls, pno):
        if len(pno) != 10:
            raise ValueError("phone no. must be of 10 digits")
        return pno

class User_Login(BaseModel):
    phone_no: str
    pin: str

class User_Access(BaseModel):
    uid: str
    
def insert_new_user(user_details: User): 
    user_count = check_pno.find_user_by_pno(user_details)
    if user_count > 0:
        return json_util._json_convert({
            "error" : True,
            "message" : "User Already Exists with this No. !"
        })
    else:
        enc_pin = bcrypt.hashpw(user_details.pin.encode(), c.Config.salt)
        user_data_enc = {
            "first_name" : user_details.first_name,
            "last_name" : user_details.last_name,
            "phone_no" : user_details.phone_no,
            "pin" : enc_pin,
            "uid" : str(uuid.uuid4())
        }
        
        val = users.insert_one(user_data_enc)
    dmat_user = db.get_collection("dmat_user")
    user_data_to_return = users.find_one({"_id" : val.inserted_id})
    dmat_user.insert_one({
        "dmat_id" : str(uuid.uuid4()),
        "balance" : 1000000,
        "uid" : user_data_to_return["uid"]
    })

    return json_util._json_convert({
        "error" : False,
        "uid" : user_data_to_return["uid"],
        "first_name" : user_data_to_return["first_name"],
        "last_name" : user_data_to_return["last_name"]
    })

def find_by_id(user_id):
    return users.find_one({"_id" : ObjectId(user_id)})

def find_by_uid(uid):
    return users.find_one({"uid" : uid})