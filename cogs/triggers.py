from discord.ext import commands
import discord
import json
import utils

ERROR_MESSAGE = "Usage: ,trigger [add|remove|list] [\"trigger\"] [\"response\"]"
FILENAME = "triggers.json"
path = None
#TODO make sure that this new format works

class TriggersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trigger(self, ctx, *args):
        #Check the args
        check = error_check(args)
        path = utils.getGuildPath(ctx.guild.name, ctx.guild.id) + "/"

        #Initalize response variables
        response = None
        embed = None

        #Add command
        if (check == 0):
            response = add_trigger(ctx, args[1], args[2])
        #Remove command
        elif (check == 1):
            response = remove_trigger(ctx, args[1])
        #List command
        elif (check == 2):
            embed = list_triggers(ctx)
        #Error
        else:
            response = ERROR_MESSAGE

        await utils.sendResponse(ctx, response=response, embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        #If the user is the bot or the message is a command
        if message.author.bot or message.content[0] == ',':
            return

        #Search server list for triggers in the message
        response = search_triggers(message)

        if response:
            await message.channel.send(response)


def error_check(args):
    if not args:
        return -1
    if args[0] == "add":
        if len(args) == 3:
            return 0
    elif args[0] == "remove":
        if len(args) == 2:
            return 1
    elif args[0] == "list":
        return 2

    return -1


def add_trigger(trigger, response):
    if utils.checkPath(path):
        with open(path + FILENAME, 'r') as json_file:
            replist = json.load(json_file)
            try:
                if replist[trigger]:
                    return "Trigger '" + trigger + "' already exists!"
            except KeyError:
                replist[trigger] = {
                    "response": response
                }
    else:
        replist = {}
        replist[trigger] = {
            "response": response
        }

    utils.save_json(path + FILENAME, replist)
    return "Successfully added trigger '" + trigger + "'"


def remove_trigger(trigger):
    try:
        with open(path + FILENAME, 'r') as json_file:
            replist = json.load(json_file)
            if replist[trigger]:
                del replist[trigger]
    except (FileNotFoundError, KeyError):
        return "Cannot remove trigger '" + trigger + "'!"

    utils.save_json(path + FILENAME, replist)

    return "Removed '" + trigger + "' from trigger list"


def list_triggers():
    triggers_embed = discord.Embed(
        title="BerryBot Triggers", color=discord.Color.orange())

    try:
        with open(path + FILENAME, 'r') as json_file:
            replist = json.load(json_file)
            for key in replist.keys():
                response = replist[key]["response"]
                triggers_embed.add_field(
                    name=key,
                    value=response,
                    inline=False
                )

        return triggers_embed
    except FileNotFoundError:
        return triggers_embed


def search_triggers(message):
    try:
        with open(path + FILENAME, 'r') as json_file:
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
        return None

async def setup(bot):
    await bot.add_cog(TriggersCog(bot))
