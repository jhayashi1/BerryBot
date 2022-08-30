import os
import json
import discord
from configparser import ConfigParser
from genericpath import isfile
from discord.ext import commands
from discord.utils import get
from shutil import copyfile

replist = {}

def getGuildPath(name, id):
    return "./servers/" + name + " (" + str(id) + ")/"

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
    copyfile("./servers/configEx.ini", path + "config.ini")

#TODO getint is not working
def getConfigParam(path, *args):
    configur = ConfigParser()
    configur.read(path)
    return configur.getint(*args)

async def sendResponse(ctx, response=None, embed=None):
    await ctx.send(content=response, embed=embed)
    #await ctx.message.delete()

async def getUserByNameOrID(ctx, target):
    #Attempt to search by id
    member = ctx.bot.get_user(target)
    if member is not None:
        return member

    #Attempt to search by name
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

#Add user to json list, return none if successful, error message if not
async def add_user_to_json_list(ctx, username, path, filename):
    #Get member object
    member = await getUserByNameOrID(ctx, username)

    #If the member cannot be found, return an error message
    if member is None:
        return "Could not find member with name " + username

    #If the path exists, try to add the user to the watchlist 
    if checkPath(path, filename):
        with open(path + filename, 'r') as json_file:
            replist = json.load(json_file)
            #If the user is already on the watchlist, return error message
            try:
                if replist[member.id]:
                    return "Member " + username + " already on the list"
            #If the user is not on the watchlist, add them 
            except KeyError:
                replist[member.id] = {
                    "name": member.name + "#" + member.discriminator,
                    "nickname": member.nick
                }
    #If the path doesn't exists, add the user to the watchlist
    else:
        replist = {}
        replist[member.id] = {
                    "name": member.name + "#" + member.discriminator,
                    "nickname": member.nick
        }
    #Save the updated json file
    save_json(path + filename, replist)

    return None

#Remove user from json list, return none if successful, error message if not
async def remove_user_from_json_list(ctx, username, path, filename):    
    #Get member object
    member = await getUserByNameOrID(ctx, username)

    try:
        with open(path + filename, 'r') as json_file:
            replist = json.load(json_file)
            #If the member exists in the json file, remove them
            if replist[str(member.id)]:
                del replist[str(member.id)]
    #If the file doesn't exist or the member doesn't exist in the file, return error message
    except (FileNotFoundError, KeyError):
        return 'User "' + username + '" not found in file "' + filename + '"'

    #Save the updated json file
    save_json(path + filename, replist)

    return None

#Check json for user based on their id
async def check_json_list_for_user(id, path, filename):
    try:
        with open(path + filename, 'r') as json_file:
            replist = json.load(json_file)
            #If user exists in watchlist, return true
            if replist[str(id)]:
                return True
    #If file or user doesn't exist, return false
    except (FileNotFoundError, KeyError):
        return False

    return False

#Retrieve a list of all of the members in a json list as an embed
def json_list_to_embed(title, path, filename):
    list_embed = discord.Embed(title=title, color=discord.Colour.blurple())

    try:
        with open(path + filename, 'r') as json_file:
            replist = json.load(json_file)
            #Loop through json file
            for key in replist.keys():
                #Retrieve user's name from entry and add to embed
                name = replist[key]["name"]
                #TODO fix this
                list_embed.add_field(
                    name=name,
                    value=None,
                    inline=False
                )

        return list_embed
    except FileNotFoundError:
        return list_embed

#Deprecated method of saving json
# def save_to_json(dict):
#     with open('varStorage.json', 'w') as fp:
#         json.dump(dict, fp, indent=4)

#Deprecated method of loading info from json file
# def load_from_json():
#     try:
#         with open('varStorage.json') as json_file:
#             global replist
#             replist = json.load(json_file)
#     except json.decoder.JSONDecodeError:
#         add_user_entry("Placeholder", 0, 0)

# def check_info(name):
#     load_from_json()
#     try:
#         return replist[name]
#     except:
#         return "Error"