import configparser
from discord.ext import commands
from utils import getUserByNameOrID
from configparser import ConfigParser
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
            await addSubscriber(ctx, target)
            response = "User " + target.name +" added to subscription list"
        else:
            try:
                #TODO Make it able to add roles to motd
                #target = discord.utils.get(ctx.guild.roles, name=' '.join(args))
                response = "Role " + target.name + " added to subscription list"
            except Exception as e:
                print(e)
                response = "No user or role found!"
        await ctx.send(response)
        await ctx.message.delete()

    @commands.command(brief='Add role or user to subscription list')
    async def say(self, ctx, args):
        await ctx.send(args)
    
async def addSubscriber(ctx, target):
        path = "./tools/" + ctx.guild.name + " (" + str(ctx.guild.id) + ")/config.ini"

        configur = ConfigParser()
        configur.read(path)
        channelId = configur.getint('params', 'motd')

        channel = ctx.bot.get_channel(channelId)
        await channel.set_permissions(target, read_messages=True, send_messages=False)


def removeSubscriber(target):
    return 0
    #TODO remove subscription

def listSubscribers():
    return 0
    #TODO list subscribers for channel

def setMotdChannel(ctx, channel):
    path = "./tools/" + ctx.guild.name + " (" + str(ctx.guild.id) + ")/config.ini"

    configur = ConfigParser()
    configur.read(path)
    #TODO set channel and save to ini file

def setup(bot):
    bot.add_cog(MotdCog(bot))