import discord
import random
import storage
import praw
from discord.ext import commands
from PyDictionary import PyDictionary

dictionary = PyDictionary()
token = open("token.txt").read()
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


def validate_user(mem):
    return storage.get_value(str(mem), 'sentry_enabled')


@bot.event
async def on_ready():
    print("bird up")
    bot.ch = bot.get_channel(625905125864505364)
    bot.guild = bot.get_guild(177593112753995776)
    bot.last_event = await bot.guild.audit_logs().find(predicate)

    for guild in bot.guilds:
        for member in guild.members:
            if storage.check_info(member) == "Error":
                storage.add_entry(str(member), member.id, member.guild.id)


# @bot.event
# async def on_voice_state_update(member, before, after):
#     guild = member.guild
#     event = await guild.audit_logs().find(predicate)
#     name = guild.get_member_named(str(event.user))
#     check = storage.get_value(str(name), 'sentry_enabled')
#
#     if event.user.name != member.name and event.id != bot.last_event.id and check and bot.sentry_on:
#         print("Event: " + event.user.name)
#         print("Member: " + member.name)
#         bot.last_event = event
#         await name.move_to(channel=None)
#         await bot.ch.send(name.mention + " nice try idiot")

@bot.command()
async def refreshdb(ctx):
    members = ctx.guild.members
    for member in members:
        if storage.check_info(member) == "Error":
            storage.add_entry(str(member), member.id, member.guild.id)

    await ctx.send("Refreshed database!")


@bot.command()
async def get(ctx, *args):
    if not validate_user(ctx.author):
        try:
            converter = commands.MemberConverter()
            name = await converter.convert(ctx=ctx, argument=' '.join(args))
            info = storage.check_info(str(name))
            embed = discord.Embed(
                title=str(name),
                colour=discord.Colour.blue()
            )
            for key, value in info.items():
                embed.add_field(name=key, value=value, inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send("Invalid User!")
    else:
        await ctx.send("You have insufficient permissions to access this command")

@bot.command()
async def assemble(ctx):
    home = ctx.author.voice.channel
    channels = ctx.guild.voice_channels

    if home is not None:
        for channel in channels:
            for member in channel.members:
                await member.move_to(home)
    else:
        await ctx.send("You're not in a channel!")


@bot.command()
async def sentry(ctx):
    if not validate_user(ctx.author):
        if not bot.sentry_on:
            await ctx.send("Sentry on...")
        else:
            await ctx.send("Sentry off...")

        bot.sentry_on = not bot.sentry_on
    else:
        await ctx.send("You have insufficient permissions to access this command")


@bot.command()
async def watch(ctx, *args):
    if not validate_user(ctx.author):
        try:
            converter = commands.MemberConverter()
            target = await converter.convert(ctx=ctx, argument=' '.join(args))
            print(str(target))
            storage.toggle_info(str(target), 'sentry_enabled')
            await ctx.send(
                "Toggled sentry to " + str(storage.get_value(str(target), 'sentry_enabled')) + " for " + str(target))
        except:
            await ctx.send("Invalid User!")
    else:
        await ctx.send("You have insufficient permissions to access this command")


@bot.command()
async def reddit(ctx, arg1):
    try:
        r = praw.Reddit(client_id='HrUKB0WP3a6A6Q',
                        client_secret='rca8u8gHsBLR8xbmho-5FysK8i0cwA',
                        user_agent='Discord bot')

        user = r.redditor(arg1)
        submissions = list(user.submissions.new())
        submission = random.choice(submissions)
        url = submission.url

        embed = discord.Embed(
            title=str(submission.title + " from r/" + str(submission.subreddit)),
            colour=discord.Colour.orange(),
            description="`" + url + "`"
        )
        if submission.is_self or "youtube.com" in submission.selftext:
            embed.add_field(name="**Submission Text:**", value=submission.selftext, inline=False)
        else:
            embed.set_image(url=url)

        embed.set_author(name='u/' + user.name,
                         icon_url=user.icon_img)
        embed.set_footer(text=submission.permalink)

        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send("Error! Invalid user")
        print(e)


@bot.command()
async def connect(ctx):
    try:
        channel = ctx.author.voice.channel
        await channel.connect()
    except:
        await ctx.send("You're not connected to a channel!")


@bot.command()
async def sam(ctx):
    lines = open("adjectives.txt").readlines()
    meaning = None

    while meaning is None:
        word = random.choice(lines)
        meaning = dictionary.meaning(word).get('Adjective')[0]

    embed = discord.Embed(
        title=word,
        colour=discord.Colour.orange(),
        description=dictionary.meaning(word).get('Adjective')[0])
    await ctx.send("Sam is very " + word)
    await ctx.send(embed=embed)
    await ctx.message.delete()


@bot.command()
async def disconnect(ctx):
    await ctx.voice_client.disconnect()


@bot.command()
async def close(ctx):
    await bot.close()


bot.run(token)
