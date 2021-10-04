from discord.ext import commands
from utils import getUserByNameOrID
import discord

class MotdCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Add role or user to subscription list')
    async def subscribe(self, ctx, *args):

        if (args[0].lower == "channel"):
            #TODO Error check this and remove first argument
            del args[0]
            setMotdChannel(args)

        target = await getUserByNameOrID(ctx, args)

        if target is not None:
            response = "User " + target.name +" added to subscription list"
        else:
            try:
                target = discord.utils.get(discord.guild.roles, name=args)
                response = "Role " + target.name + " added to subscription list"
            except Exception as e:
                print(e)
                response = "No user or role found!"
        await ctx.send(response)


def addSubscriber(target):
    return 0
    #TODO add subscription

def removeSubscriber(target):
    return 0
    #TODO remove subscription

def listSubscribers():
    return 0
    #TODO list subscribers for channel

def setMotdChannel(channel):
    return 0
    #TODO set channel and save to text file

def setup(bot):
    bot.add_cog(MotdCog(bot))