import db.db_conn as db_conn

db = db_conn.connect_db()
stocks = db.get_collection("stock_list")

def find_stock_by_name(name):
    return stocks.find({"name" : {"$regex" : name}}, {"_id" : 0})

def find_all_stocks():
    return stocks.find({})

async def find_by_id(stock_id):
    return stocks.find_one({"_id" : stock_id}, 
    {"_id":0, "expiry":0, "lotsize":0, "instrumenttype":0, "tick_size" :0, "strike":0})

async def find_by_name(stock_name):
    return stocks.find_one({"token" : stock_name}, 
    {"_id":0, "expiry":0, "lotsize":0, "instrumenttype":0, "tick_size" :0, "strike":0})

def find_by_name(stock_name):
    return stocks.find_one({"token" : stock_name}, 
    {"_id":0, "expiry":0, "lotsize":0, "instrumenttype":0, "tick_size" :0, "strike":0})