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
    uid : str

class Favourite_Stock(BaseModel):
    uid: str


def insert_favourite_stock(stock_user_data : Stock_User):
   
    uid = stock_user_data.uid
    if find_favourite_stocks_by_user_id(uid) is None:
        data =  stock_users.insert_one({
            "stock_ids" : stock_user_data.stock_ids,
            "uid" : stock_user_data.uid
        })
        print(data.inserted_id)
    else:
       fav_stocks = find_favourite_stocks_by_user_id(uid)
       print(fav_stocks)
       return stock_users.update_one(
        {"uid" : stock_user_data.user_id},
        { "$set" : {"stock_ids" : stock_user_data.stock_ids}})
    
   


def find_favourite_stocks_by_user_id(uid):
    return stock_users.find({"uid" : uid})

def find_favourite_stocks_by_user_id(uid):
    return stock_users.find_one({"uid" : uid}, {"-user_id":0})

async def find_stocks_details_by_user_id(uid):
    fav_stocks_list = stock_users.find_one({"uid" : uid}, {"_id":0, "uid":0})
    stock_details = []

    stocks = list(itertools.chain.from_iterable(fav_stocks_list.values()))
    for stock in stocks:
      stock_details.append(await stock_search.find_by_id(ObjectId(stock)))
    
    return json_util._json_convert(stock_details)