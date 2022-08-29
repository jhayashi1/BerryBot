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
        
        await utils.sendResponse(ctx, response=response)

    @commands.command(brief='Add role or user to subscription list')
    async def say(self, ctx, args):
        await ctx.send(args)


def setMotdChannel(ctx, channel):
    path = utils.getGuildPath(ctx.guild.name, ctx.guild.id) 
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

async def setup(bot):
    await bot.add_cog(MotdCog(bot))