from discord.ext import commands
import discord
from cogs.triggers import ERROR_MESSAGE
import utils
import json

class GhostDetectorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Add user to watchlist for being a ghost')
    async def ghost(self, ctx, *args):
        extra_command = args[0]

        if extra_command == "add":
            response = add_ghost(ctx, args)
        elif extra_command == "remove":
            response = remove_ghost(args)
        elif extra_command == "list":
            response = list_ghosts()
        else:
            response = ERROR_MESSAGE
            
        await utils.sendResponse(ctx, response)

    @commands.Cog.listener()
    async def on_message(self, message):
        #If the user is the bot or the message is a command
        if message.author.bot:
            return

        if message.author.status == discord.Status.offline:
            await message.add_reaction('👻')
    

async def add_ghost(ctx, args):
    path = utils.getGuildPath(ctx.guild.name, ctx.guild.id) + "/"
    filename = 'ghost-watchlist.json'
    username = ""

    for element in args:
        username += element
    
    member = await utils.getUserByNameOrID(ctx, username)

    if not member:
        return "Could not find member with name " + username

    if utils.checkPath(path, filename):
        with open(path + filename, 'r') as json_file:
            replist = json.load(json_file)
            try:
                if replist[member.id]:
                    return "Member " + username + "already on ghost watchlist"
            except KeyError:
                replist[member.id] = {
                    "name": member.name + "#" + member.discriminator,
                    "nickname": member.nick
                }
    else:
        replist = {}
        replist[member.id] = {
                    "name": member.name + "#" + member.discriminator,
                    "nickname": member.nick
        }

    utils.save_json(path + filename, replist)

    return "Successfully added member " + username + " to ghost watchlist"

def remove_ghost(args):
    return None

def list_ghosts():
    return None

async def setup(bot):
    await bot.add_cog(GhostDetectorCog(bot))