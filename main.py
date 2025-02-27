#!/usr/bin/env python3
# A simple script to print some messages.
import time
import re
import json
import random
import os
from pprint import pprint

from telethon import TelegramClient, events, utils
from dotenv import load_dotenv

load_dotenv() # get .env variable

session = os.environ.get('TG_SESSION', 'printer')
api_id = os.getenv("2474270")
api_hash = os.getenv("d6c0a53a212d5cd76afd69a48a9d80f8")
debug_mode = os.getenv("DEBUG_MODE").upper() == "FALSE"

proxy = None  # https://github.com/Anorov/PySocks

# Create and start the client so we can make requests (we don't here)
client = TelegramClient(session, api_id, api_hash, proxy=proxy).start()

# create a sender list to check if user already send private message or mention
senderList = [] 

#read json file and prepare quiz to send later
with open('quizzes.json') as json_file:
    quizzes = json.load(json_file)

@client.on(events.NewMessage)
async def handle_new_message(event):
    
    me = await client.get_me().username
    from_ = await event.client.get_entity(event.from_id)  # this lookup will be cached by telethon
    to_ = await event.client.get_entity(event.message.to_id)

    needToProceed = from_.is_self if debug_mode else not from_.is_self and (event.is_private or re.search("@"+me.username,event.raw_text))
    if needToProceed:  # only auto-reply to private chats:  # only auto-reply to private chats   
        if not from_.bot and event:  # don't auto-reply to bots
            print(time.asctime(), '-', event.message)  # optionally log time and message
            time.sleep(1)  # pause for 1 second to rate-limit automatic replies   
            message = ""
            senderList.append(to_.id)
            if senderList.count(to_.id) < 2:
                message =   f"""**AUTO REPLY**
                \nHi @{from_.username},
                \n\nMohon maaf boss saya sedang offline, mohon tunggu sebentar.
                \nSilahkan lihat-lihat [imacakes](https://www.instagram.com/ima_cake_cirebon) dulu untuk cuci mata.
                \n\n**AUTO REPLY**"""
            elif senderList.count(to_.id) < 3:
                message =   f"""**AUTO REPLY**
                \nMohon bersabar @{from_.username}, boss saya masih offline 😒"""
            elif senderList.count(to_.id) < 4:
                message = f"""**AUTO REPLY** 
                \n@{from_.username} Tolong bersabar yaa 😅"""
            else:
                random_number = random.randint(0,len(quizzes) - 1)
                question = quizzes[random_number]['question']
                answer = quizzes[random_number]['answer']
                message = f"""**AUTO REPLY**
                \n @{from_.username}, Main tebak-tebakan aja yuk 😁
                \n {question}
                \n {answer}
                \n """
            
            if message != "":
                await event.reply(message)

client.start()
client.run_until_disconnected()
