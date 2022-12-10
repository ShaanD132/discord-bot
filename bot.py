import discord
from discord.ext import tasks
import pymongo

mongo = pymongo.MongoClient("mongodb+srv://shaand:Sana132@lebbk.urxltwo.mongodb.net/?retryWrites=true&w=majority")
db = mongo.lebbk
collection = db["time"]

channels = [824351465018490931, 964896100223950858]

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
        collection = db["time"]
        exists = False
        for item in collection.find():
            if (item["user"] == author):
                exists = True
        if (exists == True):
            embed = discord.Embed(title = "Invalid Command ❌", description = "You have already been added to the Database.", color = 0xb896ff)
            await message.channel.send(embed = embed)
        else:
            collection = db["time"]
            collection.insert_one({"user": author, "time": 0})
            embed = discord.Embed(title = "Added ✅", description = "Added to Database.", color = 0xb896ff)
            await message.channel.send(embed = embed)

    if message.content.startswith("$time"):
        author = message.author.name
        collection = db["time"]
        post = collection.find_one({"user": author})
        embed = discord.Embed(title = "Time with Le Bobok ⏳", description = "You have spent " + str(post["time"]) + " minutes on Le Bobok", color = 0xb896ff)
        await message.channel.send(embed = embed)

@tasks.loop(seconds = 60)
async def time():
    active_users = []
    for channel in channels:
        channel1 = client.get_channel(channel)
        members1 = channel1.members
        for member in members1:
            active_users.append(member.name)

    print(active_users)
    for user in active_users:
        collection = db["time"]
        post = collection.find_one({"user":user})
        time1 = post["time"]
        time1 += 1
        collection.update_one({"user": user}, { "$set": { "time": time1 } })


client.run("ODI0NTI0NDUxODczMjkyMzE5.GR84x_.POHPNd_uBnIeoBtp0sRWYLHqO5aUq1bDiArB0A")