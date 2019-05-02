import asyncio
import sys
import configparser
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.users import GetFullUserRequest

async def main():
    #set the variables
    config = configparser.ConfigParser()
    config.read('./python/settings.ini')
    api_id = int(config['Telegram_Credentials']['api_id'])
    api_hash = config['Telegram_Credentials']['api_hash']
    phone_number = config['Telegram_Credentials']['phone_number']
    client = await TelegramClient('./python/session_name', api_id, api_hash).start()

    # assign variables from arguments
    userName = sys.argv[1:][0]

    # pull user info
    full = await client(GetFullUserRequest(userName))
    userid = full.user.id

    #set the output message and output
    outputMessage = '{ "userID" : "' + str(userid) + '" }'
    print(outputMessage)

asyncio.get_event_loop().run_until_complete(main())
