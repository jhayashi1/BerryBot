import discord
import random
import storage
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.messages = True
bot = commands.Bot(command_prefix=',', intents=intents)

bot.sentry_on = False


def send_quote(ctx, title, quote, image):
    embed = discord.Embed(
        title=title,
        description=quote,
        colour=discord.Colour.blue()
    )

    embed.set_thumbnail(url=image)
    return embed


def predicate(event):
    return event.action is discord.AuditLogAction.member_move or event.action is discord.AuditLogAction.member_disconnect


@bot.event
async def on_ready():
    print("bird up")
    bot.ch = bot.get_channel(748586297328664638)
    bot.guild = bot.get_guild(177593112753995776)
    bot.last_event = await bot.guild.audit_logs().find(predicate)


@bot.event
async def on_voice_state_update(member, before, after):
    #TODO: Update function to kick user
    guild = member.guild
    event = await guild.audit_logs().find(predicate)
    name = str(guild.get_member_named(str(event.user)))
    check = storage.get_value(name, 'sentry_enabled')

    if event.user.name != member.name and event.id != bot.last_event.id and check and bot.sentry_on:
        print("Event: " + event.user.name)
        print("Member: " + member.name)
        bot.last_event = event


@bot.command()
async def refreshdb(ctx):
    members = ctx.guild.members
    for member in members:
        if storage.checkInfo(member) == "Error":
            storage.addEntry(str(member), member.id, member.guild.id)

    await ctx.send("Refreshed database!")


@bot.command()
async def get(ctx, *args):
    try:
        converter = commands.MemberConverter()
        name = await converter.convert(ctx=ctx, argument=' '.join(args))
        info = storage.checkInfo(str(name))
        embed = discord.Embed(
            title=str(name),
            colour=discord.Colour.blue()
        )
        for key, value in info.items():
            embed.add_field(name=key, value=value, inline=False)
        await ctx.send(embed=embed)
    except:
        await ctx.send("Invalid User!")

@bot.command()
async def hello(ctx):
    await ctx.send("yeet")


@bot.command()
async def mode(ctx, arg1):
    if arg1 == 'i':
        await bot.change_presence(status=discord.Status.idle)
        await ctx.send("Changed to idle")
    elif arg1 == 'o':
        await bot.change_presence(status=discord.Status.online)
        await ctx.send("Changed to online")
    else:
        await bot.ch.send("Incorrect argument")


@bot.command()
async def quote(ctx, arg1):
    print(ctx.author.name + " quoted " + arg1)

    if arg1.lower() == "vishnu":
        channel = bot.get_channel(397952381511270400)
        quote_list = await channel.history().flatten()
        quote = random.choice(quote_list).content
        image_link = "https://cdn.discordapp.com/avatars/177592593952014336/187405c7faa6d947b8bc4f016d7e2d51.png?size=128"
        await ctx.send(embed=send_quote(ctx, "Vishnu", quote, image_link))
    elif arg1.lower() == "cameron":
        channel = bot.get_channel(405570948960354346)
        quote_list = await channel.history().flatten()
        quote = random.choice(quote_list).content
        image_link = "https://cdn.discordapp.com/avatars/198587944783577088/d383f2612bcf68348d5afb339af1b584.png?size=128"
        await ctx.send(embed=send_quote(ctx, "Cameron", quote, image_link))
    elif arg1.lower() == "jared":
        channel = bot.get_channel(431654881359822848)
        quote_list = await channel.history().flatten()
        quote = random.choice(quote_list).content
        image_link = "https://cdn.discordapp.com/avatars/187718185779200000/f4f75feca475e8fcd1a86db32f93b3eb.png?size=128"
        await ctx.send(embed=send_quote(ctx, "Jared", quote, image_link))
    elif arg1.lower() == "andrew":
        channel = bot.get_channel(405571631944171527)
        quote_list = await channel.history().flatten()
        quote = random.choice(quote_list).content
        image_link = "https://cdn.discordapp.com/avatars/198297488786980865/cd5c660007a9a17d33498581b7b15ab3.png?size=128"
        await ctx.send(embed=send_quote(ctx, "Andrew", quote, image_link))
    elif arg1.lower() == "max":
        channel = bot.get_channel(405573706774216714)
        quote_list = await channel.history().flatten()
        quote = random.choice(quote_list).content
        image_link = "https://cdn.discordapp.com/avatars/217467339669635073/f66ee4b572d39bb697c7e4b9406c58ca.png?size=128"
        await ctx.send(embed=send_quote(ctx, "Max", quote, image_link))
    elif arg1.lower() == "jon":
        channel = bot.get_channel(498996904710111232)
        quote_list = await channel.history().flatten()
        quote = random.choice(quote_list).content
        image_link = "https://cdn.discordapp.com/avatars/249716884876820481/609225e2e6d8581885e0931d6b9f61e2.png?size=128"
        await ctx.send(embed=send_quote(ctx, "Jon", quote, image_link))
    elif arg1.lower() == "gay":
        channel = bot.get_channel(405573202933317632)
        quote_list = await channel.history().flatten()
        quote = random.choice(quote_list).content
        image_link = "https://cdn.discordapp.com/avatars/198324497655398402/776e76df7dda87a86666665256dda05b.png?size=128"
        await ctx.send(embed=send_quote(ctx, "Gay Person", quote, image_link))
    else:
        await ctx.send("Target not recognized")


@bot.command()
async def sentry(ctx):
    if not bot.sentry_on:
        await ctx.send("Sentry on...")
    else:
        await ctx.send("Sentry off...")

    bot.sentry_on = not bot.sentry_on


@bot.command()
async def watch(ctx, *args):
    try:
        converter = commands.MemberConverter()
        target = await converter.convert(ctx=ctx, argument=' '.join(args))
        print(str(target))
        storage.toggle_info(str(target), 'sentry_enabled')
        await ctx.send("Toggled sentry to " + str(storage.get_value(str(target), 'sentry_enabled')) + " for " + str(target))
    except:
        await ctx.send("Invalid User!")


@bot.command()
async def connect(ctx):
    try:
        channel = ctx.author.voice.channel
        await channel.connect()
    except:
        await ctx.send("You're not connected to a channel!")


@bot.command()
async def disconnect(ctx):
    await ctx.voice_client.disconnect()


@bot.command()
async def close(ctx):
    await bot.close()

bot.run("")
