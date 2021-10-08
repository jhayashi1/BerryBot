import discord
import os
import utils
from discord.ext import commands
from configparser import ConfigParser

class MotdCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(brief='Set motd channel')
    async def motd(self, ctx, arg1):
        channel = await utils.getChannelByNameOrID(ctx, arg1)

        if channel is not None:
            response = setMotdChannel(ctx, channel)
        else:
            response = "Error setting MOTD channel"
        
        await utils.sendResponse(ctx, response)

    @commands.command(brief='Add role or user to subscription list')
    async def subscribe(self, ctx, *args):
        target = await utils.getUserByNameOrID(ctx, args)

        if target is not None:
            response = await addSubscriber(ctx, target)
        else:
            try:
                #TODO Make it able to add roles to motd
                #target = discord.utils.get(ctx.guild.roles, name=' '.join(args))
                response = "Role added to subscription list"
            except Exception as e:
                print(e)
                response = "No user or role found!"

        await utils.sendResponse(ctx, response)
    
    @commands.command(brief='Remove role or user from subscription list')
    async def unsubscribe(self, ctx, target):
        target = await utils.getUserByNameOrID(ctx, target)

        if target is not None:
            response = await removeSubscriber(ctx, target)

    @commands.command(brief='Add role or user to subscription list')
    async def say(self, ctx, args):
        await ctx.send(args)
    
async def addSubscriber(ctx, target):
        path = "./tools/" + ctx.guild.name + " (" + str(ctx.guild.id) + ")/config.ini"

        try:
            channelId = utils.getConfigParam('params', 'motd')

            channel = ctx.bot.get_channel(channelId)
            await channel.set_permissions(target, read_messages=True, send_messages=False)
        except Exception as e:
            print(e)
            return "Error adding user!"

        return "User " + target.name + " added to subscription list"

async def removeSubscriber(ctx, target):
    path = "./tools/" + ctx.guild.name + " (" + str(ctx.guild.id) + ")/config.ini"
    return "User " + target.name + " removed from subscription list"
    #TODO remove subscription


def setMotdChannel(ctx, channel):
    path = "./tools/" + ctx.guild.name + " (" + str(ctx.guild.id) + ")/"
    file = "config.ini"

    #Check for path and config file
    if not utils.checkPath(path, file):
        utils.addConfig(path)
    
    #Set config parser
    configur = ConfigParser()
    configur.read(path + file)

    #Write to config file
    configur.set('params', 'motd', str(channel.id))
    with open(path + file, 'w') as config:
        configur.write(config)

    return "Successfully set motd channel to " + channel.name

def setup(bot):
    bot.add_cog(MotdCog(bot))