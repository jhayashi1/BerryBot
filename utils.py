from discord.ext import commands
from discord.utils import get

async def getUserByNameOrID(ctx, target):
    #Attempt to search by id
    member = ctx.bot.get_user(target)
    if member is not None:
        return member

    #Attempt to search by name
    #TODO search by name and discriminator
    name = ' '.join(target)
    name.split('#')
    length = len(name)
    converter = commands.MemberConverter()
    try:
        #name + discriminator
        if length > 1 and len(name[1]) == 4 and name[1].isdecimal():
            get(ctx.bot.get_all_members(), name=name[0], discriminator=name[1])
        #nickname
        else:
            member = await converter.convert(ctx=ctx, argument=' '.join(str))
    except:
        member = None
    return member