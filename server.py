import asyncio
import sys
import configparser
import json
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.users import GetFullUserRequest
from quart import Quart, jsonify, request
from quart_cors import cors, route_cors

# set app
app = Quart(__name__)
app = cors(app)

# set route
@app.route("/getUserID", methods=["POST"])
@route_cors()
async def index():
    test_client = app.test_client()
    app.config["QUART_CORS_EXPOSE_HEADERS"] = ["X-Special", "X-Other"]
    response = await test_client.get("/", headers={"Origin": "http://localhost"})
    assert response.access_control.allow_origin == {"*"}
    assert response.access_control.expose_headers == {"X-Special", "X-Other"}

    # get the json variables from the request
    jsonObjectIn = await request.get_json()

    #map variables from request
    tipToUserName = jsonObjectIn['tipToUserName']
    tipFromID = jsonObjectIn['tipFromID']
    telegramGroupID = jsonObjectIn['telegramGroupID']
    tipFromUserName = jsonObjectIn['tipFromUserName']
    tipAmount = jsonObjectIn['tipAmount']
    tipToken = jsonObjectIn['tipToken']
    memo = jsonObjectIn['memo']
    tokenID = jsonObjectIn['tokenID']

    # load in the config for Telegram API
    config = configparser.ConfigParser()
    config.read('settings.ini')
    api_id = int(config['Telegram_Credentials']['api_id'])
    api_hash = config['Telegram_Credentials']['api_hash']
    phone_number = config['Telegram_Credentials']['phone_number']

    ## set client as global var
    global client

    ## if the client is already defined don't reload
    try:
        client
    except NameError:
       client = await TelegramClient('session_name', api_id, api_hash).start()
    else:
        print("client is defined")

    jsonOut = {
        "tipToUserName": str(tipToUserName),
        "tipFromID": str(tipFromID),
        "telegramGroupID": str(telegramGroupID),
        "tipFromUserName": str(tipFromUserName),
        "tipAmount": str(tipAmount),
        "tipToken": str(tipToken),
        "memo": str(memo),
        "tokenID": str(tokenID)
    }

    try:
        full = await client(GetFullUserRequest(str(tipToUserName)))
        userID = full.user.id
        jsonOut.update("userID": str(userID))
    except:
        userID = None
    
    return json.dumps(jsonOut)

app.run(port=5000, host='0.0.0.0')
