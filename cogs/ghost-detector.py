from discord.ext import commands
import discord
from cogs.triggers import ERROR_MESSAGE
import utils

class GhostDetectorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Add user to watchlist for being a ghost')
    async def ghost(self, ctx, *args):
        extra_command = args[0]

        if (extra_command == "add"):
            response = add_ghost(args)
        elif (extra_command == "remove"):
            response = remove_ghost(args)
        elif (extra_command == "list"):
            response = list_ghosts()
        else:
            response = ERROR_MESSAGE
            
        await utils.sendResponse(ctx, response)
    

def add_ghost(args):
    return None

def remove_ghost(args):
    return None

def list_ghosts():
    return None

def setup(bot):
    bot.add_cog(GhostDetectorCog(bot))