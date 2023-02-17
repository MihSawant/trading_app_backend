from pymongo import MongoClient
from pymongo import errors
import requests

try:
    CONNECTION_STRING = "mongodb://unigo_db:oB7YYc5P7ozwzqAJzUWLBhI3EsQUfS8daHteGmw8@165.232.188.167:27017/?authMechanism=DEFAULT"
    client = MongoClient(CONNECTION_STRING)

    db = client.get_database("unigo")

    r = requests.get('https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json')
    print("loadind..")
   
    for i in r.json() : 
        db.stock_list.insert_one(i)


except errors.PyMongoError:
    print("Connection ERROR")