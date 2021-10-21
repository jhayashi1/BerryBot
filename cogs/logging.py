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
                response = "Logging is already enabled"
            else:
                self.enabled = True
                response = "Logging enabled"
        elif arg1 == "disable":
            if not self.enabled:
                response = "Logging is already disabled"
            else:
                self.enabled = False
                log_message(ctx.message)
                response = "Logging disabled"
        else:
            response = "logging [enable | disable]"

        utils.sendResponse(ctx, response)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        #If the user is the bot or logging is not enabled
        if member.id == self.bot.user.id or not self.enabled:
            return None

        name = member.name + "#" + member.discriminator
        path = "./tools/" + member.guild.name + " (" + str(member.guild.id) + ")/voice chat/"
        filename = name + ".json"
        now = datetime.now()

        #If the user joined a channel, log the current time
        if before.channel is None:
            self.storage[name] = {
                "date": now.strftime("%m/%d/%y"),
                "before_time": now.strftime("%H:%M:%S"),
                "after_time": 0,
                "duration": 0
            }
        #If the user left the channel, store the logged time
        elif after.channel is None and self.storage[name]:
            #Calculate amount of time in channel
            self.storage[name]["after_time"] = now.strftime("%H:%M:%S")
            self.storage[name]["duration"] = str(datetime.strptime(self.storage[name]["after_time"], "%H:%M:%S") - datetime.strptime(self.storage[name]["before_time"], "%H:%M:%S"))

            #If the storage file exists, append time to json
            if utils.checkPath(path):
                print("Opening json for " + name)
                with open(path + filename, 'r') as json_file:
                    replist = json.load(json_file)
                    replist[len(replist)] = self.storage[name]
            #Create new file if the storage file for user doesn't exist
            else:
                print("No voice log detected for " + name + " creating voice log...")
                replist = {}
                replist[0] = self.storage[name]

            #Save json file and clear user's data
            storage.save_json(path + filename, replist)
            self.storage[name].clear()
            print(self.storage)

    @commands.Cog.listener()
    async def on_message(self, message):
        #If the user is the bot or logging is not enabled
        if message.author.id == self.bot.user.id or not self.enabled:
            return None

        log_message(message)

def log_message(message):
    sender = message.author
    name = sender.name + "#" + sender.discriminator
    path = "./tools/" + sender.guild.name + " (" + str(sender.guild.id) + ")/text chat/"
    filename = name + ".json"
    now = datetime.now()

    #If the path exists, log the message info
    if utils.checkPath(path):
        with open(path + filename, 'r') as json_file:
            replist = json.load(json_file)
            replist[len(replist)] = {
                "date": now.strftime("%m/%d/%y"),
                "time": now.strftime("%H:%M:%S"),
                "channel": message.channel.name,
                "message": message.content
            }
    #If the file path doesn't exist, create a new file and log the message info
    else:
        print("No chat log detected for " + name + " adding chat log...")
        replist = {}
        replist[0] = {
                "date": now.strftime("%m/%d/%y"),
                "time": now.strftime("%H:%M:%S"),
                "channel": message.channel.name,
                "message": message.content
            }

    #Save the new info to the json file
    storage.save_json(path + filename, replist)

def setup(bot):
    bot.add_cog(LoggingCog(bot))