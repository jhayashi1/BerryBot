import discord
import os
import utils
from discord.ext import commands
from configparser import ConfigParser

class MotdCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Add role or user to subscription list')
    async def subscribe(self, ctx, *args):

        if (args[0].lower == "channel"):
            #TODO Error check this and remove first argument
            del args[0]
            channel = utils.getChannelByNameOrID(ctx, args)

            if channel is not None:
                response = setMotdChannel(ctx, args)
            else:
                response = "Error setting MOTD channel"

        target = await utils.getUserByNameOrID(ctx, args)

        if target is not None:
            response = await addSubscriber(ctx, target)
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

        try:
            configur = ConfigParser()
            configur.read(path)
            channelId = configur.getint('params', 'motd')

            channel = ctx.bot.get_channel(channelId)
            await channel.set_permissions(target, read_messages=True, send_messages=False)
        except Exception as e:
            print(e)
            return "Error adding user!"

        return "User " + target.name +" added to subscription list"


def removeSubscriber(target):
    return 0
    #TODO remove subscription

def listSubscribers():
    return 0
    #TODO list subscribers for channel

def setMotdChannel(ctx, channel):
    path = "./tools/" + ctx.guild.name + " (" + str(ctx.guild.id) + ")/config.ini"

    #TODO test this
    if not os.path.exists(path):
        os.mknod(path)

    configur = ConfigParser()
    configur.read(path)


    #TODO set channel and save to ini file

def setup(bot):
    bot.add_cog(MotdCog(bot))