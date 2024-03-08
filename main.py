import discord
from discord.ext import commands
from Kindred import kindred_task

print("-"*10, "The Program starts...", "-"*10)

command_prefix = ["."]  # ['!','?','.','%']
client = commands.Bot(command_prefix=command_prefix)

noti_ch = "Discord Channel ID" 

@client.event
async def on_ready():
    subscribed_channel = client.get_channel(noti_ch)
    activity = discord.Activity(type=discord.ActivityType.listening, name="Kindred Callouts")
    await client.change_presence(activity=activity)
    print("{0.user} start listening to Kindred callouts".format(client))
    await subscribed_channel.send("We have logged in as {0.user}".format(client))

client.loop.create_task(kindred_task(client, noti_ch))

client.run("DISCORD_BOT_TOKEN")
