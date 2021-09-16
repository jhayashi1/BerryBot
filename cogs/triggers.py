from discord.ext import commands
import discord
import storage
import json
import os

ERROR_MESSAGE = "Usage: trigger [add|remove|list] [trigger] [response]"

class TriggersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trigger(self, ctx, *args):

        check = error_check(args)
        
        if (check == 0):
            add_trigger(ctx, args[1], args[2])
            await ctx.send("Successfully added " + args[1] + " " + args[2])
        elif (check == 1):
            await ctx.send("Successfully removed " + args[1])
        elif (check == 2):
            await ctx.send("TODO: display list")
        else:
            await ctx.send(ERROR_MESSAGE)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id or message.content[0] == ',':
            return None

        response = search_triggers(message)

        if response:
            await message.channel.send(response)


def error_check(args):
    if args[0] == "add":
        if len(args) == 3:
            return 0
    elif args[0] == "remove":
        if len(args) == 2:
            return 1
    elif args[0] == "list":
        return 2

    return -1

def add_trigger(ctx, trigger, response):
    path = "./tools/" + ctx.guild.name + " (" + str(ctx.guild.id) + ")/triggers/"
    filename = "triggers.json"

    #TODO manage duplicate entries
    try:
        with open(path + filename, 'r') as json_file:
            replist = json.load(json_file)
            replist[trigger] = {
                "response": response
            }
    except FileNotFoundError:
        if not os.path.exists(path):
            os.makedirs(path)

        replist = {}
        replist[trigger] = {
                "response": response
            }

    storage.save_json(path + filename, replist)

def search_triggers(message):
    path = "./tools/" + message.guild.name + " (" + str(message.guild.id) + ")/triggers/"
    filename = "triggers.json"

    try:
        with open(path + filename, 'r') as json_file:
            replist = json.load(json_file)
            response = None
            for key in replist.keys():
                if key in message.content:
                    response = replist.get(key)
                    break

            if response:
                response = response.get("response")

            return response
    except FileNotFoundError:
        print("FileNotFoundError")
        return None

def setup(bot):
    bot.add_cog(TriggersCog(bot))