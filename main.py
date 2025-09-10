import os
import discord
from discord.ext import commands
from Kindred import kindred_task

print("-"*10, "The Program starts...", "-"*10)

# Bot configuration
command_prefix = ["."]  # ['!','?','.','%']
client = commands.Bot(command_prefix=command_prefix)

# Discord notification channel ID - set via environment variable
noti_ch = int(os.getenv('DISCORD_NOTIFICATION_CHANNEL_ID', '0'))

@client.event
async def on_ready():
    subscribed_channel = client.get_channel(noti_ch)
    activity = discord.Activity(type=discord.ActivityType.listening, name="Kindred Callouts")
    await client.change_presence(activity=activity)
    print("{0.user} start listening to Kindred callouts".format(client))
    await subscribed_channel.send("We have logged in as {0.user}".format(client))

client.loop.create_task(kindred_task(client, noti_ch))

# Start the bot with token from environment variable
discord_token = os.getenv('DISCORD_BOT_TOKEN')
if not discord_token:
    raise ValueError("DISCORD_BOT_TOKEN environment variable not set")

client.run(discord_token)
