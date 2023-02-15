from pydantic import BaseModel
import db.db_conn as db_conn
import json
import typing
db = db_conn.connect_db()
stock_users = db.get_collection("stock_users")

class Stock_User(BaseModel):
    stock_ids : typing.List
    user_id : str


def insert_favourite_stock(stock_user_data : Stock_User):
   
    user_id = stock_user_data.user_id
    if find_favourite_stocks_by_user_id(user_id) is None:
        data =  stock_users.insert_one({
            "stock_ids" : stock_user_data.stock_ids,
            "user_id" : stock_user_data.user_id
        })
        print(data.inserted_id)
    else:
       fav_stocks = find_favourite_stocks_by_user_id(user_id)
       print(fav_stocks)
       return stock_users.update_one({
        "stock_ids" : stock_user_data.stock_ids,
        }, {"user_id" : stock_user_data.user_id})
    
   


def find_favourite_stocks_by_user_id(user_id):
    return stock_users.find({"user_id" : user_id})

def find_favourite_stocks_by_user_id(user_id):
    return stock_users.find_one({"user_id" : user_id}, {"-user_id":0})