from discord.ext import commands
from datetime import datetime
import json
import os
import storage
import utils

class LoggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.storage = {}
        self.enabled = True
    
    @commands.command(brief='Command to enable/disable voice and chat logging')
    async def logging(self, ctx, arg1):
        if arg1 == "enable":
            if self.enabled:
                await ctx.send("Logging is already enabled")
            else:
                self.enabled = True
                await ctx.send("Logging enabled")
        elif arg1 == "disable":
            if not self.enabled:
                await ctx.send("Logging is already disabled")
            else:
                self.enabled = False
                log_message(ctx.message)
                await ctx.send("Logging disabled")
        else:
            await ctx.send("logging [enable | disable]")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id == self.bot.user.id or not self.enabled:
            return None

        name = member.name + "#" + member.discriminator
        path = "./tools/" + member.guild.name + " (" + str(member.guild.id) + ")/voice chat/"
        filename = name + ".json"
        now = datetime.now()

        if before.channel is None:
            self.storage[name] = {
                "date": now.strftime("%m/%d/%y"),
                "before_time": now.strftime("%H:%M:%S"),
                "after_time": 0,
                "duration": 0
            }
        elif after.channel is None and self.storage[name]:
            self.storage[name]["after_time"] = now.strftime("%H:%M:%S")

            self.storage[name]["duration"] = str(datetime.strptime(self.storage[name]["after_time"], "%H:%M:%S") - datetime.strptime(self.storage[name]["before_time"], "%H:%M:%S"))

            if utils.checkPath(path):
                print("Opening json for " + name)
                with open(path + filename, 'r') as json_file:
                    replist = json.load(json_file)
                    replist[len(replist)] = self.storage[name]
            else:
                print("No voice log detected for " + name + " creating voice log...")
                replist = {}
                replist[0] = self.storage[name]

            storage.save_json(path + filename, replist)
            self.storage[name].clear()
            print(self.storage)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id or not self.enabled:
            return None

        log_message(message)

def log_message(message):
    sender = message.author
    name = sender.name + "#" + sender.discriminator
    path = "./tools/" + sender.guild.name + " (" + str(sender.guild.id) + ")/text chat/"
    filename = name + ".json"
    now = datetime.now()

    try:
        with open(path + filename, 'r') as json_file:
            replist = json.load(json_file)
            replist[len(replist)] = {
                "date": now.strftime("%m/%d/%y"),
                "time": now.strftime("%H:%M:%S"),
                "channel": message.channel.name,
                "message": message.content
            }
    except FileNotFoundError:
        print("No chat log detected for " + name + " adding chat log...")
        utils.checkPath(path)
        replist = {}
        replist[0] = {
                "date": now.strftime("%m/%d/%y"),
                "time": now.strftime("%H:%M:%S"),
                "channel": message.channel.name,
                "message": message.content
            }

    storage.save_json(path + filename, replist)

def setup(bot):
    bot.add_cog(LoggingCog(bot))