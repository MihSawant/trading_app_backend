import db.db_conn as db_conn
from pydantic import BaseModel
import uuid
import datetime
import bson.json_util as json_util

db = db_conn.connect_db()

orders = db.get_collection("users_orders")
transaction = db.get_collection("transaction")
user_dmat = db.get_collection("dmat_user")
portfolio = db.get_collection("users_portfolio")

class User_Order(BaseModel):
    uid : str
    type: str
    token: str
    qty: int
    transaction_id: str
    buy_rate: float
    sell_rate: float
    
class Portfolio(BaseModel):
    uid : str
class Balance(BaseModel):
    uid: str


def insert_new_order(order: User_Order):
   
    order_id = str(uuid.uuid4())
    orders.insert_one({
        "order_id" : order_id,
        "type" : order.type,
        "token" : order.token,
        "qty" : order.qty,
        "buy_rate" : order.buy_rate,
        "sell_rate" : order.sell_rate,
        "time" : str(datetime.datetime.now()),
        "qty" : order.qty,
        "transaction_id" : "",
        "uid" : order.uid
    })
    user_order = orders.find_one({"order_id" : order_id}, {"_id" : 0})
    if user_order is not None:
        order_type = ""
      
        
        tid = str(uuid.uuid4())

        dmat_account = user_dmat.find_one({"uid" : str(user_order['uid'])})
        if dmat_account is not None:
            balance_amount = dmat_account['balance']
            # means stock is sold
            if user_order['buy_rate'] !=  0.0:
                order_type = "Buy"
                price = user_order['buy_rate'] * user_order['qty']
            
            # means stock is buy
            else:
                order_type = "Sell"
                price = user_order['sell_rate'] * user_order['qty']
            
            transaction.insert_one({
                "type" : order_type,
                "amount" : price,
                "from" : "DMAT",
                "to" : order.uid,
                "transaction_id" : tid
            })
            
            user_transaction = transaction.find_one({"transaction_id" : tid})
            orders.update_one(
            {
            "order_id" : order_id
            }, {
                "$set":{
                    "transaction_id" : user_transaction['transaction_id']
                }
            })
            if user_transaction['type'] == "Buy":
                amt = balance_amount - user_transaction['amount']
                if price > balance_amount:
                    json_util._json_convert({
                        "error" : True,
                        "message" : "Not Have Enough Funds !"
                    })
            else:
                amt = balance_amount + user_transaction['amount']
            user_dmat.update_one(
                {
                    "uid" : str(user_order['uid']),
                
                }, 

                {
                    "$set" :{
                        "balance" : amt
                    }
                }
                
                )
            if user_transaction['type'] == "Buy":
                pos = True
            else:
                pos = False
            portfolio.insert_one({
                "uid" : user_order['uid'],
                "token": user_order['token'],
                "buy_rate" : user_order['buy_rate'],
                "position" : pos,
                "sell_rate" : user_order['sell_rate'],
                "qty" : user_order['qty'],
                "order_id" : user_order['order_id']
            })
            return json_util._json_convert({
                "error" : False,
                "message" : "Stock Successfully added to portfolio"
            })
        return json_util._json_convert({
            "error" : True,
            "message" : "DMAT Not Found !"
        })    
    return json_util._json_convert({
        "error" : True,
        "message" : "User Not Found !"
    })

def get_info(uid):
    return portfolio.find({"uid" : uid}, {"_id":0})

def find_balance_of_user(uid):
    return user_dmat.find({"uid" : uid}, {"_id":0, "uid":0, "dmat_id":0})        

def find_order_by_uid(uid):
    return orders.find({"uid": uid}, {"_id":0})     
