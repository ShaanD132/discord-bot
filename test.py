collection = ""
search_id = ""
embed = ""
habits = ""
i = 0

t_count = 0
streak = 0
for post in collection.find():
    t_count += 1
    count = 0
    for i in range(1, 9):
        field_name = "habit" + str(i)
        arr = post[field_name]
        if (search_id in arr):
            count += 1
            streak += 1
        else:
            streak = 0

        if (i == 3 or i == 5 or i == 7):
            embed.add_field(name = "\u200b", value = "\u200b", inline = True)
            embed.add_field(name = habits[i-1], value = str(count) + " day(s) out of " + str(t_count), inline = True)

    embed.add_field(name = "\u200b", value = "\u200b", inline = True)
    embed.add_field(name = habits[i-1], value = str(count) + " day(s) out of " + str(t_count), inline = True)
embed.add_field(name = "Proj 50", value = str(streak) + " day(s) out of " + str(t_count))