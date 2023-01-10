import discord
from discord.ext import tasks
import pymongo
import os
import asyncio
import random
from datetime import date, timedelta

token = os.getenv("DISCORD_TOKEN")
mongo = pymongo.MongoClient("mongodb+srv://shaand:Sana132@lebbk.urxltwo.mongodb.net/?retryWrites=true&w=majority")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.presences = True
intents.members = True
intents.reactions = True

client = discord.Client(intents=intents)

lebbk_channels = [824351465018490931, 964896100223950858, 824524626361188403, 824565516920160286, 824339628659965983, 824354320120152106, 824354228847509504, 951085083085930496, 951085037040861214, 968134067344265276]
juno_channels = [636804198918258698, 458678727916912640, 797415731494780978, 458678879351996439, 484236105814769667, 404993149522542634, 414807748274814996]

hottie_arr = [0] * 10
count = [0]
proj50_id = 0
start_proj50 = "2023/1/5"

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
    project_50.start()

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
    
    if message.content.startswith("$alone"):
        message1 = message.content
        message1 = message1.rstrip()
        id1 = message.guild.id
        prefix = "You have"
        if (id1 == 824339628424167464):
            db = mongo.lebbk
        elif (id1 == 365086888496726018):
            db = mongo.juno
        collection = db["time"]
        message1 = message1[6:]
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
            time1 = post["alone_time"]
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
                embed = discord.Embed(title = "Time in Le Bobok Alone 😔", description = prefix + " spent " + str(time1) + " alone", color = 0x630008)
            else:
                embed = discord.Embed(title = "Time on Server", description = prefix + " spent " + str(time1) + " on this server", color = 0x630008)
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

    if message.content.startswith("$alone_lb"):
        id1 = message.guild.id
        if (id1 == 824339628424167464):
            db = mongo.lebbk
        elif (id1 == 365086888496726018):
            db = mongo.juno
        collection = db["time"]
        users = []
        times = []
        for user in collection.find():
            times.append(user["alone_time"])
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
        embed = discord.Embed(title = "Alone Leaderboard", description = "", color = 0x42559e)

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
        embed = discord.Embed(title = "Zakam", description = "He's just a friend", color = 0x630008)
        await message.channel.send(embed = embed)

    if message.content.startswith("$hottie"):
        url = get_url()
        await asyncio.sleep(0.5)
        embed = discord.Embed(title = "Hottie 💯", color = 0x5dc299)
        embed.set_image(url = url)
        await message.channel.send(embed = embed)

    if message.content.startswith("$test"):
        channel = client.get_channel(936365381680005171)
        message = await channel.fetch_message(1060491005981380648)
        print(message.reactions)

    if message.content.startswith("$proj50"):
        message1= message.content.split(" ")
        names = ["ashley", "brandon", "dylan", "kushveer", "lau", "nikhil", "shaan", "yaseen"]
        ids = [881783277277573120, 424502958005288964, 955905841675006014, 211727586638692352, 731513674665033768, 313314610885165056, 211893329984618496, 426048762780319744]
        if (len(message1) > 1):
            message1[1] = message1[1].lower()
            if (message1[1] == "list" or message1[1] == "List"):
                embed = discord.Embed(title = "Possible Names", description = "Ashley, Brandon, Dylan, Kushveer, Lau, Nikhil, Shaan, Yaseen", color = 0xEFABFF)
            elif (message1[1] not in names):
                embed = discord.Embed(title = "Invalid Name", description = "Please do $proj50 list to see members taking part in the program.", color = 0xA3333D)
            else:
                index = names.index(message1[1])
                embed = discord.Embed(title = "Habit Progress", description = "How " + message1[1].capitalize() + " has been progressing", color = 0xF61067)
                search_id = ids[index]
                db = mongo.lebbk
                collection = db["proj50"]
                habits = ["Waking up Early", "Morning Routine", "Exercise", "Reading", "New Skill", "Healthy Diet", "Journaling", "No Fap"]

                for i in range (1, 9):
                    t_count = 0
                    count = 0
                    field_name = "habit" + str(i)
                    for post in collection.find():
                        arr = post[field_name]
                        t_count += 1
                        if (search_id in arr):
                            count += 1
                    if (i == 3 or i == 5 or i == 7):
                        embed.add_field(name = "\u200b", value = "\u200b", inline = True)
                        embed.add_field(name = habits[i-1], value = str(count) + " day(s) out of " + str(t_count), inline = True)
                    else:
                        embed.add_field(name = "\u200b", value = "\u200b", inline = True)
                        embed.add_field(name = habits[i-1], value = str(count) + " day(s) out of " + str(t_count), inline = True)

                streak_count = 0
                t_count = 0
                for post in collection.find():
                    t_count += 1
                    habit_count = 0
                    for j in range(1, 9):
                        field_name = "habit" + str(j)
                        arr = post[field_name]
                        if (search_id in arr):
                            habit_count += 1
                    if (habit_count == 8):
                        streak_count += 1
                    else:
                        streak_count = 0
                embed.add_field(name = "Proj 50", value = str(streak_count) + " day(s) out of " + str(t_count))
        await message.channel.send(embed = embed)


@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    db = mongo.lebbk
    collection = db["proj50"]
    post = collection.find_one({"id": message_id})
    if (post != None):
        new_user = payload.user_id
        if (new_user != 824524451873292319):
            emoji_reaction = str(payload.emoji)
            emojis = ["🌅", "📵", "🏋🏿", "📖", "👨‍💻", "🍳", "✍️", "🧴"]
            for i in range(len(emojis)):
                if (emojis[i] == emoji_reaction):
                    habit_id = "habit" + str(i+1)
                    users = post[habit_id]
                    users.append(new_user)
                    collection.update_one({"id": message_id}, { "$set": { habit_id:  users} })

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    db = mongo.lebbk
    collection = db["proj50"]
    post = collection.find_one({"id": message_id})
    if (post != None):
        new_user = payload.user_id
        if (new_user != 824524451873292319):
            emoji_reaction = str(payload.emoji)
            emojis = ["🌅", "📵", "🏋🏿", "📖", "👨‍💻", "🍳", "✍️", "🧴"]
            for i in range(len(emojis)):
                if (emojis[i] == emoji_reaction):
                    habit_id = "habit" + str(i+1)
                    users = post[habit_id]
                    users.remove(new_user)
                    collection.update_one({"id": message_id}, { "$set": { habit_id:  users} })

@tasks.loop(hours = 2)
async def project_50():
    global proj50_id
    db = mongo.lebbk
    collection = db["proj50"]
    exists = False

    tdy = date.today()
    yesterday = tdy - timedelta(days = 1)

    tdy = tdy.strftime("%Y/%m/%d")
    yesterday = yesterday.strftime("%Y/%m/%d")

    tdy = str(tdy)
    yesterday = str(yesterday)
    print(yesterday)
    date1 = tdy

    for post in collection.find():
        if (post["date"] == date1):
            exists = True

    if (exists == False):
        names = ["ashley", "brandon", "dylan", "kushveer", "lau", "nikhil", "shaan", "yaseen"]
        ids = [881783277277573120, 424502958005288964, 955905841675006014, 211727586638692352, 731513674665033768, 313314610885165056, 211893329984618496, 426048762780319744]
        habits = ["Waking up Early", "Morning Routine", "Exercise", "Reading", "New Skill", "Healthy Diet", "Journaling", "No Fap"]
        embed_yesterday = discord.Embed(title = "Recap of Yesterday", description = "How Le Bobok did:", color = 0xF0803C)
        for i in range(1, 9):
            field_name = "habit" + str(i)
            people = []
            post = collection.find_one({"date": yesterday})
            arr = post[field_name]

            for j in range(0, len(names)):
                if (ids[j] in arr):
                    people.append(names[j])

            name_string = ""
            for person in people:
                if (name_string != ""):
                    name_string = name_string + ", " + person.capitalize()
                else:
                    name_string = person.capitalize()
            if name_string == "":
                name_string = "Nobody"
            embed_yesterday.add_field(name = habits[i-1], value = name_string, inline = True)

        channel = client.get_channel(966104456297074698)
        await channel.send(embed = embed_yesterday)


        count = 0
        for _ in collection.find():
            count += 1
        current_day = count + 1


        embed = discord.Embed(title = "Project 50 Progress - Day " + str(current_day), color = 0x006494)
        embed.add_field(name = "𝟭: Wake up before 8am", value = "🌅", inline = False)
        embed.add_field(name = "𝟮: Morning Routine: 1hr No Distractions", value = "📵", inline = False)
        embed.add_field(name = "𝟯: Exercise for 1 Hour a Day", value = "🏋🏿", inline = False)
        embed.add_field(name = "𝟰: Read 10 Pages a Day", value = "📖", inline = False)
        embed.add_field(name = "𝟱: Dedicate 1 Hour to a New Skill", value = "👨‍💻", inline = False)
        embed.add_field(name = "𝟲: Follow a Healthy Diet", value = "🍳", inline = False)
        embed.add_field(name = "𝟳: Journal Properly", value = "✍️", inline = False)
        embed.add_field(name = "𝟴: NoFap", value = "🧴", inline = False)
        message = await channel.send(embed = embed)

        post = collection.insert_one({"id": message.id, "date" : date1, "habit1": [], "habit2": [], "habit3": [], "habit4": [], "habit5": [], "habit6": [], "habit7": [], "habit8": [], "day": current_day})
        proj50_id = message.id
        emojis = ["🌅", "📵", "🏋🏿", "📖", "👨‍💻", "🍳", "✍️", "🧴"]
        for emoji in emojis:
            await message.add_reaction(emoji)
    else:
        print("alr exists")
        print(date1)

@tasks.loop(seconds = 60)
async def time():
    active_users = []
    db = mongo.lebbk
    alone = []

    for channel in lebbk_channels:
        channel1 = client.get_channel(channel)
        members1 = channel1.members
        if (len(members1) == 1):
            for member in members1:
                alone.append(member.name)
        for member in members1:
            active_users.append(member.name)

    print(active_users)
    for user in active_users:
        collection = db["time"]
        post = collection.find_one({"user":user})
        if (post != None):
            if (user in alone):
                time2 = post["alone_time"]
                time2 += 2
                collection.update_one({"user": user}, { "$set": { "alone_time": time2 } })
            else:
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