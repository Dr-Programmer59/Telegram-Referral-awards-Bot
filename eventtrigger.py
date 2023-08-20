from telethon import connection, events
from telethon import TelegramClient, sync

from telethon.tl import functions, types
import mysql.connector
import json

# Read configuration from the file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)


mydb=mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        passwd=config["passwd"],
        database=config["database"]
    )
print("connected")
mycursor = mydb.cursor()
API_ID = config["API_ID_Telegram"],
API_HASH = config["API_HASH_Telegram"],

client_ = TelegramClient("bot",int(API_ID),API_HASH)
client_.start(bot_token=config["BOT_TOKEN_Telegram"])


@client_.on(events.Raw(types.UpdateChannelParticipant))
async def f(event):
    invite_link=event.invite.link
    user_id=event.user_id
    mycursor.execute(f"SELECT name,peoples FROM `inviteReward` WHERE link='{invite_link}'")
    result = mycursor.fetchall()
    if(not(result==[])):
        mycursor.execute(f"UPDATE `inviteReward` SET peoples = '{str(result[0][1])+str(user_id)},' WHERE name ='{result[0][0]}'")
        mydb.commit()

    # print(vars(event))

    # event is the object which contains all the returned values including invite_link if there is any
    # You can check all the attributes of the object using vars(event)

client_.run_until_disconnected()


