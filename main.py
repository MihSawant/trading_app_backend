from fastapi import FastAPI
import db.db_conn as db_setup

app = FastAPI()

# first connect to db
db_setup.connect_db()

@app.get("/")
def hello():
    return {"message" : "Welcome !"}

