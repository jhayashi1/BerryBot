import os
import json
from configparser import ConfigParser
from genericpath import isfile
from discord.ext import commands
from discord.utils import get
from shutil import copyfile

replist = {}

def getGuildPath(name, id):
    return "./tools/" + name + " (" + str(id) + ")"

def checkPath(path, *args):
    val = 1

    if not os.path.exists(path):
            os.makedirs(path)
            val = 0
    
    if args:
        filename = ''.join(args)
        if not isfile(path + filename):
            val = 0

    return val

def addConfig(path):
    copyfile("./tools/configEx.ini", path + "config.ini")

#TODO getint is not working
def getConfigParam(path, *args):
    configur = ConfigParser()
    configur.read(path)
    return configur.getint(*args)

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
    name = ''.join(target)
    print("Searching for user " + name)
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

#Save json info at directory
def save_json(path, dict):
    with open(path, 'w') as json_file:
        json.dump(dict, json_file, indent=4)

#Find json file at directory
def where_json(file_name):
    return os.path.exists(file_name)

#Adds user info to db when they are not found in the db
#TODO call this method when user joins guild
def add_user_entry(name, id, guild):
    replist[name] = {
        "memberID": id,
        "guildID": guild,
        "sentry_enabled": False
    }
    save_json('varStorage.json', replist)
    return "done"


#Deprecated method of saving json
def save_to_json(dict):
    with open('varStorage.json', 'w') as fp:
        json.dump(dict, fp, indent=4)

#Deprecated method of loading info from json file
def load_from_json():
    try:
        with open('varStorage.json') as json_file:
            global replist
            replist = json.load(json_file)
    except json.decoder.JSONDecodeError:
        add_user_entry("Placeholder", 0, 0)

def check_info(name):
    load_from_json()
    try:
        return replist[name]
    except:
        return "Error"
    