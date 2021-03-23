from discord.ext import commands, tasks
from discord.utils import get
from time import sleep
import random
import discord
import requests
import shutil

class ImpersonationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(minutes=random.randint(30, 45))
    async def monitor(self):
        guilds = self.bot.guilds
        for guild in guilds:
            channels = guild.voice_channels
            users = []
            target_channel = None

            #Get channel with most people in it
            for channel in channels:
                if channel.members:
                    temp = []
                    for key in channel.members:
                        temp.append(key)

                        if len(temp) > len(users):
                            users = temp
                            target_channel = channel

            lines = open("./tools/people.txt").read().splitlines()
            target_member = None

            while target_member is None:
                temp = random.choice(lines).split('#')
                temp_member = get(self.bot.get_all_members(), name=temp[0], discriminator=temp[1])
                #print("checking " + temp[0])
                if temp_member not in users and temp_member.status == discord.Status.online:
                    target_member = temp_member

            info = self.get_info(target_member)

            await self.bot.user.edit(avatar=info[0])
            await guild.get_member(self.bot.user.id).edit(nick=info[1])

            vc = await target_channel.connect()
            sleep(random.randint(5, 10) * 60)
            await vc.disconnect()

                    #vc = get(self.bot.voice_clients)

        # if vc is not None:
        #     vc.play(discord.FFmpegPCMAudio(executable="./ffmpeg/bin/ffmpeg.exe", source="./tools/audio/audio.wav"))
        #     while vc.is_playing():
        #         sleep(1)

    @commands.command()
    async def impersonate(self, ctx, *args):
        converter = commands.MemberConverter()
        member = await converter.convert(ctx=ctx, argument=' '.join(args))
        if (member is not None):
            pfp = member.avatar_url
            r = requests.get(pfp, stream=True)

            if r.status_code == 200:
                r.raw.decode_content = True

                with open("./tools/images/Currentpfp.png", 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

                with open("./tools/images/Currentpfp.png", 'rb') as p:
                    pic = p.read()

                await self.bot.user.edit(avatar=pic)
                await ctx.guild.get_member(self.bot.user.id).edit(nick=' '.join(args))
                await ctx.send("success")
        else:
            await ctx.send("invalid user")

        await ctx.message.delete()

    @commands.command()
    async def default(self, ctx):
        with open("./tools/images/default.png", 'rb') as p:
            pic = p.read()
        await self.bot.user.edit(avatar=pic)
        await ctx.guild.get_member(self.bot.user.id).edit(nick="BerryBot")

    @commands.command()
    async def speak(self, ctx, *args):
        vc = get(ctx.bot.voice_clients, guild=ctx.guild)
        voice_channel = ctx.author.voice.channel

        if vc is None and voice_channel is not None:
            vc = await voice_channel.connect()

        vc.play(discord.FFmpegPCMAudio(executable="./ffmpeg/bin/ffmpeg.exe", source="./tools/audio/audio.wav"))

        while vc.is_playing():
            sleep(.1)

        await ctx.message.delete()

    @commands.command()
    async def begin(self, ctx):
        if ctx.author.id == 187718185779200000:
            self.monitor.start()
            await ctx.send("It has begun")
            await ctx.message.delete()
        else:
            await ctx.send("Nice try idiot")

    def get_info(self, member):
        pfp = member.avatar_url
        r = requests.get(pfp, stream=True)
        nick = None

        if member.nick:
            nick = member.nick
        else:
            nick = member.name

        if r.status_code == 200:
            r.raw.decode_content = True

            with open("./tools/images/Currentpfp.png", 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            with open("./tools/images/Currentpfp.png", 'rb') as p:
                pic = p.read()

            return [pic, nick]

def setup(bot):
    bot.add_cog(ImpersonationCog(bot))