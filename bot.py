import discord
import os
import storage
from discord.ext import commands

path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
token = open("token.txt").read()

intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.messages = True

bot = commands.Bot(command_prefix=',', intents=intents)

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension('cogs.' + name)


@bot.event
async def on_ready():
    print("bird up")
    for guild in bot.guilds:
        for member in guild.members:
            if storage.check_info(member) == "Error":
                storage.add_entry(str(member), member.id, member.guild.id)

bot.run(token)