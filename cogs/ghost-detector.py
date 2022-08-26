from discord.ext import commands
import discord
from cogs.triggers import ERROR_MESSAGE
import utils
import json

ERROR_MESSAGE = "error"
FILENAME = "ghost-watchlist.json"
path = None

class GhostDetectorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Add user to watchlist for being a ghost')
    async def ghost(self, ctx, *args):
        #Set the path for the file
        global path
        path = utils.getGuildPath(ctx.guild.name, ctx.guild.id) + "/"
        extra_command = args[0]

        #Initialize response and embed
        response = None
        embed = None

        #Parse the extra command
        if extra_command == "add":
            response = await add_ghost(ctx, args)
        elif extra_command == "remove":
            response = await remove_ghost(ctx, args)
        elif extra_command == "list":
            embed = list_ghosts()
        else:
            response = ERROR_MESSAGE

        #Send response  
        await utils.sendResponse(ctx, response=response, embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        global path
        path = utils.getGuildPath(message.guild.name, message.guild.id) + "/"

        #If the user is the bot, ignore it
        if message.author.bot:
            return

        #If the user appears offline and they're on the watchlist, react with the ghost emoji
        if message.author.status == discord.Status.offline and check_watchlist(message.author):
            await message.add_reaction('👻')
    
#Add user to ghost watchlist
async def add_ghost(ctx, args):
    #Get username and member object
    username = list_to_username(args)
    member = await utils.getUserByNameOrID(ctx, username)

    #If the member cannot be found, return an error message
    if member is None:
        return "Could not find member with name " + username

    #If the path exists, try to add the user to the watchlist 
    if utils.checkPath(path, FILENAME):
        with open(path + FILENAME, 'r') as json_file:
            replist = json.load(json_file)
            #If the user is already on the watchlist, return error message
            try:
                if replist[member.id]:
                    return "Member " + username + "already on ghost watchlist"
            #If the user is not on the watchlist, add them 
            except KeyError:
                replist[member.id] = {
                    "name": member.name + "#" + member.discriminator,
                    "nickname": member.nick
                }
    #If the path doesn't exists, add the user to the watchlist
    else:
        replist = {}
        replist[member.id] = {
                    "name": member.name + "#" + member.discriminator,
                    "nickname": member.nick
        }
    #Save the updated json file
    utils.save_json(path + FILENAME, replist)

    return 'Successfully added member "' + username + '" to ghost watchlist'
    
#Remove user from ghost watchlist
async def remove_ghost(ctx, args):    
    #Get username and member object
    username = list_to_username(args)
    member = await utils.getUserByNameOrID(ctx, username)

    try:
        with open(path + FILENAME, 'r') as json_file:
            replist = json.load(json_file)
            #If the member exists in the json file, remove them
            if replist[str(member.id)]:
                del replist[str(member.id)]
    #If the file doesn't exist or the member doesn't exist in the file, return error message
    except (FileNotFoundError, KeyError):
        return 'User "' + username + '" not found in ghost watchlist'

    #Save the updated json file
    utils.save_json(path + FILENAME, replist)

    return 'Removed "' + username + '" from ghost watchlist' 

#Retrieve a list of all of the members on the watchlist
def list_ghosts():
    list_embed = discord.Embed(title="Ghost Watchlist", color=discord.Colour.blurple())

    try:
        with open(path + FILENAME, 'r') as json_file:
            replist = json.load(json_file)
            #Loop through json file
            for key in replist.keys():
                #Retrieve user's name from entry and add to embed
                name = replist[key]["name"]
                #TODO fix this
                list_embed.add_field(
                    name=name,
                    value=None,
                    inline=False
                )

        return list_embed
    except FileNotFoundError:
        return list_embed

#Check watchlist for member
def check_watchlist(sender):
    try:
        with open(path + FILENAME, 'r') as json_file:
            replist = json.load(json_file)
            #If user exists in watchlist, return true
            if replist[str(sender.id)]:
                return True
    #If file or user doesn't exist, return false
    except (FileNotFoundError, KeyError):
        return False

    return False

def list_to_username(args):
    username = ""

    for element in args[1:]:
        username += element
    
    return username

async def setup(bot):
    await bot.add_cog(GhostDetectorCog(bot))