from fastapi import FastAPI
import db.db_conn as db_setup
import services.stock_search as stock_search
import bson.json_util as json_util
from fastapi import websockets, WebSocket ,WebSocketDisconnect


app = FastAPI()

# first connect to db
# db_setup.connect_db()

@app.get("/")
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


