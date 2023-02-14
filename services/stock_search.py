import db.db_conn as db_conn

db = db_conn.connect_db()

def find_stock_by_name(name):
    stocks = db.get_collection("stock_list")
    return stocks.find({"name" : {"$regex" : name}}, {"_id" : 0})

