from genericpath import isfile
import os
from discord.ext import commands
from discord.utils import get

def checkPath(path, *args):
    val = 1

    if not os.path.exists(path):
            os.makedirs(path)
            val = 0
    
    if args:
        if not isfile(path + args):
            with open(path + args, 'w') as file:
                pass
            val = 0
    return val

async def sendResponse(ctx, response):
    await ctx.send(response)
    await ctx.message.delete()

async def getUserByNameOrID(ctx, target):
    #Attempt to search by id
    #TODO This might not work
    member = ctx.bot.get_user(target)
    if member is not None:
        return member

    #Attempt to search by name
    #TODO search by name and discriminator
    name = ' '.join(target)
    print(name)
    length = len(name)
    converter = commands.MemberConverter()
    try:
        #name + discriminator
        if length > 1 and len(name[1]) == 4 and name[1].isdecimal():
            member = get(ctx.bot.get_all_members(), name=name[0], discriminator=name[1])
        #nickname
        else:
            member = await converter.convert(ctx=ctx, argument=''.join(name))
    except:
        member = None
    return member

async def getChannelByNameOrID(ctx, target):

    #Attempt to search by id
    channel = ctx.bot.get_channel(target)
    if channel is not None:
        return channel
    
    #Attempt to search by name
    name = ''.join(target)
    print(target)

    channel = get(ctx.bot.get_all_channels(), name=name)

    return channel