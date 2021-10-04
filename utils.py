from discord.ext import commands

async def getUserByName(ctx, name):
    converter = commands.MemberConverter()
    try:
        member = await converter.convert(ctx=ctx, argument=' '.join(name))
    except:
        member = -1
    return member