from fastapi import FastAPI, Request, Response
import db.db_conn as db_setup
from services import stock_search, check_pno, user_login, user_access
# only to on when ref token is needed...
# from services import angel_login
import bson.json_util as json_util
from fastapi import websockets, WebSocket ,WebSocketDisconnect
from models import users, stock_users
import uvicorn

app = FastAPI(
    title="Trade App Backend (Elan and nVision)",
    version="1.0"
)
print("application startup was successfull...")
# first connect to db
# db_setup.connect_db()
@app.get("/", tags=["Hello World!"])
def hello():
    return {"message" : "Welcome !"}

@app.websocket("/ws/stock-name")
async def stock_search_by_name_ws(webs: WebSocket):
    try:
        await webs.accept()
        while True:
            name = await webs.receive_text()
            if name is None or len(name) == 0:
                webs.send_json({
                    "error" : True,
                    "message" : "Name of Stock cannot be null"
                })
            else:
                results = stock_search.find_stock_by_name(name)
                await webs.send_json(json_util._json_convert(results))
    except WebSocketDisconnect:
        print("Connection close")


@app.post("/new-user/register", tags=["Register New User"])
def new_user(user_details: users.User,):
    response = users.insert_new_user(user_details)
    return response

@app.post("/user/add-watchlist", tags=["Add Favourite stocks for user"])
def stock_user_insert(stock_data: stock_users.Stock_User):
    stock_users.insert_favourite_stock(stock_data)

@app.post("/user/index", tags=["Check If User Already Exists (contact page -- uis)"])
def check_if_user_exists(phone_no: users.User_Check_Pno):
    return json_util._json_convert({
        "code" : check_pno.find_user_by_pno(phone_no)
    })

@app.post("/user/login", tags=["User Login"])
def login(data : users.User_Login):
    return user_login.verify_pin(data)

@app.post("/user/favourite-stocks", tags=["Fetch All Favourite Stocks of User (by uid)"])
async def get_favourite_stocks_by_user_id(data: stock_users.Favourite_Stock):
    return await stock_users.find_stocks_details_by_user_id(data.uid)

@app.post("/user/check-login-access", tags=["Angel Auth Details for User (by uid)"])
def check_user_access(data: users.User_Access):
    return json_util._json_convert(user_access.check_access(data.uid))
# print(stock_history.get_history())
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8090, log_level="info")
