from pydantic import BaseModel
import db.db_conn as db_conn
from bson import json_util
import typing
from bson.objectid import ObjectId
import itertools
from services import stock_search

db = db_conn.connect_db()
stock_users = db.get_collection("stocks_users")

class Stock_User(BaseModel):
    stock_ids : typing.List
    user_id : str

class Favourite_Stock(BaseModel):
    user_id: str


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
       return stock_users.update_one(
        {"user_id" : stock_user_data.user_id},
        { "$set" : {"stock_ids" : stock_user_data.stock_ids}})
    
   


def find_favourite_stocks_by_user_id(user_id):
    return stock_users.find({"user_id" : user_id})

def find_favourite_stocks_by_user_id(user_id):
    return stock_users.find_one({"user_id" : user_id}, {"-user_id":0})

async def find_stocks_details_by_user_id(user_id):
    fav_stocks_list = stock_users.find_one({"user_id" : user_id}, {"_id":0, "user_id":0})
    stock_details = []

    stocks = list(itertools.chain.from_iterable(fav_stocks_list.values()))
    for stock in stocks:
      stock_details.append(await stock_search.find_by_id(ObjectId(stock)))
    
    return json_util._json_convert(stock_details)