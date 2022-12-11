import discord
from discord.ext import tasks
import pymongo
import os
import asyncio
import random

token = os.getenv("DISCORD_TOKEN")

mongo = pymongo.MongoClient("mongodb+srv://shaand:Sana132@lebbk.urxltwo.mongodb.net/?retryWrites=true&w=majority")

channels = [824351465018490931, 964896100223950858]

hottie_arr = [0] * 10
count = [0]

def get_url():
    valid = False
    f = open('hottie.txt')
    urls = f.readlines()
    y = len(urls)
    while valid == False:
        line_no = random.randint(0, y)
        url = urls[line_no]
        repeat = False
        if url in hottie_arr:
            repeat = True
        if (repeat == False):
            valid = True
            hottie_arr[count[0]] = url
            if (count[0] != 9):
                count[0] = count[0] + 1
            else:
                count[0] = 0
    f.close()
    return url

#new_item = {"user": "Shaan", "time":0}
#collection.insert_one(new_item)
"""
collection = db["time"]
time1 = 1
await message.channel.send("hi")
collection.update_one({"user":"Shaan"}, { "$set": { "time": 2 } })
"""


intents = discord.Intents.default()
intents.messages = True
#intents.message_content = True
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Logged in.")
    time.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$setup"):
        author = message.author.name
        db = mongo.lebbk
        collection = db["time"]
        exists = False
        for item in collection.find():
            if (item["user"] == author):
                exists = True
        if (exists == True):
            embed = discord.Embed(title = "Invalid Command ❌", description = "You have already been added to the Database.", color = 0xb896ff)
            await message.channel.send(embed = embed)
        else:
            db = mongo.lebbk
            collection = db["time"]
            collection.insert_one({"user": author, "time": 0})
            embed = discord.Embed(title = "Added ✅", description = "Added to Database.", color = 0xb896ff)
            await message.channel.send(embed = embed)

    if message.content.startswith("$time"):
        message1 = message.content
        message1 = message1.rstrip()
        db = mongo.lebbk
        collection = db["time"]
        message1 = message1[5:]
        if (message1 != ""):
            message1 = message1.lstrip()
            print(message1)
            target = collection.find_one({"user": message1})
            if target != None:
                author = target["user"]
        else:
            author = message.author.name
        post = collection.find_one({"user": author})
        if (post == None):
            embed = discord.Embed(title = "Taey To Fou?", description = "Use $setup first to be added to the database", color = 0xb896ff)
            await message.channel.send(embed = embed)
        else:
            time1 = post["time"]
            time_h = str(time1 // 60)
            time_m = str(time1 % 60)
            if (time_h == "1"):
                h_str = "hour"
            else:
                h_str = "hours"

            if (time_m == "1"):
                m_str = "minute"
            else:
                m_str = "minutes"

            time1 = time_h + " " + h_str + " and " + time_m + " " + m_str
            embed = discord.Embed(title = "Time with Le Bobok ⏳", description = "You have spent " + str(time1) + " with Le Bobok", color = 0xb896ff)
            await message.channel.send(embed = embed)

    if message.content.startswith("$hottie"):
        url = get_url()
        await asyncio.sleep(0.5)
        embed = discord.Embed(title = "Hottie 💯", color = 0x5dc299)
        embed.set_image(url = url)
        await message.channel.send(embed = embed)

@tasks.loop(seconds = 60)
async def time():
    active_users = []
    db = mongo.lebbk

    for channel in channels:
        channel1 = client.get_channel(channel)
        members1 = channel1.members
        for member in members1:
            active_users.append(member.name)

    print(active_users)
    for user in active_users:
        collection = db["time"]
        post = collection.find_one({"user":user})
        if (post != None):
            time1 = post["time"]
            time1 += 1
            collection.update_one({"user": user}, { "$set": { "time": time1 } })

client.run(token)