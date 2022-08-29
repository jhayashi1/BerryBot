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
        path = utils.getGuildPath(ctx.guild.name, ctx.guild.id) 
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
            embed = utils.json_list_to_embed(path, FILENAME)
        else:
            response = ERROR_MESSAGE

        #Send response  
        await utils.sendResponse(ctx, response=response, embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        global path
        path = utils.getGuildPath(message.guild.name, message.guild.id) 

        #If the user is the bot, ignore it
        if message.author.bot:
            return

        #If the user appears offline and they're on the watchlist, react with the ghost emoji
        if message.author.status == discord.Status.offline and utils.check_json_list_for_user(message.author.id, path, FILENAME):
            await message.add_reaction('👻')
    
#Add user to ghost watchlist
async def add_ghost(ctx, args):
    #Get username and member object
    username = list_to_username(args)

    #Attempt to add user to ghost watchlist
    response = utils.add_user_to_json_list(ctx, username, path, FILENAME)
        
    #If the function did not return an error message, set response to success message
    if not response:
        response = 'Successfully added member "' + username + '" to ghost watchlist'

    return response
    
#Remove user from ghost watchlist
async def remove_ghost(ctx, args):    
    #Get username and member object
    username = list_to_username(args)

    #Attempt to remove user from ghost watchlist
    response = utils.remove_user_from_json_list(ctx, username, path, FILENAME)

    #If the function did not return an error message, set the resposne to success message
    if not response:
        response = 'Removed "' + username + '" from ghost watchlist' 

    return response

def list_to_username(args):
    username = ""

    for element in args[1:]:
        username += element
    
    return username

async def setup(bot):
    await bot.add_cog(GhostDetectorCog(bot))