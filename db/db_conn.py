from pymongo import MongoClient
from pymongo import errors

import configs.conf as c



def connect_db():
    try:
        CONNECTION_STRING = "mongodb://" + c.Config.db_username + ":" + c.Config.db_pwd + "@165.232.188.167:27017/?authMechanism=DEFAULT"
        client = MongoClient(CONNECTION_STRING)

        db = client.get_database("unigo")
        c.Config.db_collections.append(db.list_collection_names())
        return db

    except errors.PyMongoError:
        print("Connection ERROR")