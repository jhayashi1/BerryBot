from urllib import response
import discord
import os
import utils
from discord.ext import commands
from configparser import ConfigParser

path = None
FILENAME = 'status-watchlist.json'

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

    @commands.command(brief='Add user to action watchlist')
    async def watch(self, ctx, *args):
        global path
        path = utils.getGuildPath(ctx.guild.name, ctx.guild.id)

        username = ""

        for element in args:
            username += element

        response = utils.add_user_to_json_list(ctx, username, path, FILENAME)

        if not response:
            response = 'Successfully added user "' + username + '" to action watchlist'

        await utils.sendResponse(ctx, response=response)

    @commands.command(brief='Repeat message after the command')
    async def say(self, ctx, args):
        await ctx.send(args)

    @commands.Cog.listener()
    async def on_presence_update(before, after):
        #TODO get channel from config.ini
        new_activity = after.activity

        for element in new_activity:
            if type(element) is discord.Spotify:
                message = element.title

        if message:
            #TODO send response
            return None

        return None


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