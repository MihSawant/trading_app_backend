
import requests
import db.db_conn as db_conn
import datetime
import json

db = db_conn.connect_db()

auths = db.get_collection("angel_auth")
doc = auths.find_one({"name" : "angel"})
if doc is not None:
  # already exist the keys so use them for the today
  payload = {
  "refreshToken" : doc['refreshToken']
  }
  headers = {
    'Authorization': 'Bearer '+doc['jwtToken'],
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-UserType': 'USER',
    'X-SourceID': 'WEB',
    'X-ClientLocalIP': '192.168.1.9',
    'X-ClientPublicIP': '192.168.1.9',
    'X-MACAddress': '1c:57:dc:81:35:b8',
    'X-PrivateKey': doc['feedToken']
  }
  resp = requests.post("https://apiconnect.angelbroking.com/rest/auth/angelbroking/jwt/v1/generateTokens", 
  headers=headers, json=payload)
  a_resp = resp.json()['data']
  if a_resp is None:
    print("Response Is None")
  else:
    if a_resp['status'] == True:
      auths.update_one({"name" : "angel"}, 
      {"$set" : 
        {
        "refreshToken" : a_resp['refreshToken'],
        "jwtToken" : a_resp['jwtToken'],
        "feedToken" : a_resp['feedToken'],
        "last_updated": str(datetime.datetime.now()) 
        }
      }
      )
      print("TOKEN IS SET..")
    else:
      print(json.dumps({
        "status" : a_resp['errcode'],
        "message" : a_resp['message']
      }))
