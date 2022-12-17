import discord
from discord.ext import tasks
import pymongo
import os
import asyncio
import random

token = os.getenv("DISCORD_TOKEN")

mongo = pymongo.MongoClient("mongodb+srv://shaand:Sana132@lebbk.urxltwo.mongodb.net/?retryWrites=true&w=majority")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)

lebbk_channels = [824351465018490931, 964896100223950858, 824524626361188403, 824565516920160286, 824339628659965983, 824354320120152106, 824354228847509504, 951085083085930496, 951085037040861214, 968134067344265276]
juno_channels = [636804198918258698, 458678727916912640, 797415731494780978, 458678879351996439, 484236105814769667, 404993149522542634, 414807748274814996]

hottie_arr = [0] * 10
count = [0]

def get_url():
    valid = False
    f = open('hottie.txt')
    urls = f.readlines()
    y = len(urls)
    while valid == False:
        line_no = random.randint(0, y-1)
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


@client.event
async def on_ready():
    print("Logged in.")
    time.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$time"):
        message1 = message.content
        message1 = message1.rstrip()
        id1 = message.guild.id
        prefix = "You have"
        if (id1 == 824339628424167464):
            db = mongo.lebbk
        elif (id1 == 365086888496726018):
            db = mongo.juno
        collection = db["time"]
        message1 = message1[5:]
        if (message1 != ""):
            message1 = message1.lstrip()
            print(message1)
            target = collection.find_one({"user": message1})
            if target != None:
                author = target["user"]
                prefix = author + " has"
        else:
            author = message.author.name
        post = collection.find_one({"user": author})
        if (post == None):
            if (id1 == 824339628424167464):
                embed = discord.Embed(title = "Taey To Fou?", description = "Use $setup first to be added to the database", color = 0xb896ff)
            else:
                embed = discord.Embed(title = "You Crazy?", description = "Use $setup first to be added to the database", color = 0xb896ff)
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
            if (id1 == 824339628424167464):
                embed = discord.Embed(title = "Time with Le Bobok ⏳", description = prefix + " spent " + str(time1) + " with Le Bobok", color = 0xb896ff)
            else:
                embed = discord.Embed(title = "Time on Server", description = prefix + " spent " + str(time1) + " on this server", color = 0xb896ff)
            await message.channel.send(embed = embed)

    if message.content.startswith("$lb"):
        id1 = message.guild.id
        if (id1 == 824339628424167464):
            db = mongo.lebbk
        elif (id1 == 365086888496726018):
            db = mongo.juno
        collection = db["time"]
        users = []
        times = []
        for user in collection.find():
            times.append(user["time"])
            users.append(user["user"])
        for _ in range (0, len(times)):
            for j in range(0, len(times) -1):
                if (times[j] < times[j+1]):
                    temp = times[j]
                    times[j] = times[j+1]
                    times[j+1] = temp
                    temp1 = users[j]
                    users[j] = users[j+1]
                    users[j+1] = temp1
        embed = discord.Embed(title = "Leaderboard", description = "", color = 0x42559e)
        for i in range(10):
            time_h = times[i] // 60
            time_m = times[i] % 60
            if (time_h > 1):
                time_str = str(time_h) + " hours and " + str(time_m) + " minutes"
            else:
                time_str = str(time_h) + " hour and " + str(time_m) + " minutes"
            name_str = str(i+1) + ". " + users[i]
            value_str = "Has spent " + time_str
            embed.add_field(name = name_str, value = value_str, inline = False)

        author = users.index(message.author.name)
        time_u = times[author] // 60
        time_um = times[author] % 60
        if (time_u > 1):
            time_str1 = "You have spent " + str(time_u) + " hours and " + str(time_um) + " minutes"
        else:
            time_str1 = "You have spent " + str(time_u) + " hour and " + str(time_m) + " minutes"
        name_str1 = "Your Position: " + str(author + 1)

        embed.add_field(name = name_str1, value = time_str1, inline = False)
        await message.channel.send(embed = embed)

    if message.content.startswith("$jisakam"):
        embed = discord.Embed(title = "Zakam", description = "He's just a friend", color = 0xb896ff)
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

    for channel in lebbk_channels:
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

    active_users = []
    db = mongo.juno
    for channel in juno_channels:
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