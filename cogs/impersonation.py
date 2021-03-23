from discord.ext import commands
from discord.utils import get
from time import sleep
import discord
import requests
import shutil

class ImpersonationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def impersonate(self, ctx, *args):
        converter = commands.MemberConverter()
        member = await converter.convert(ctx=ctx, argument=' '.join(args))
        if (member is not None):
            pfp = member.avatar_url
            r = requests.get(pfp, stream=True)

            if r.status_code == 200:
                r.raw.decode_content = True

                with open("Currentpfp.png", 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

                with open("Currentpfp.png", 'rb') as p:
                    pic = p.read()

                await self.bot.user.edit(avatar=pic)
                await ctx.guild.get_member(self.bot.user.id).edit(nick=' '.join(args))
                await ctx.send("success")
        else:
            await ctx.send("invalid user")

        await ctx.message.delete()

    @commands.command()
    async def default(self, ctx):
        with open("default.png", 'rb') as p:
            pic = p.read()
        await self.bot.user.edit(avatar=pic)
        await ctx.guild.get_member(self.bot.user.id).edit(nick="BerryBot")

    @commands.command()
    async def speak(self, ctx, *args):
        vc = get(ctx.bot.voice_clients, guild=ctx.guild)
        voice_channel = ctx.author.voice.channel

        if vc is None and voice_channel is not None:
            vc = await voice_channel.connect()

        vc.play(discord.FFmpegPCMAudio(executable="./ffmpeg/bin/ffmpeg.exe", source="./audio.wav"))

        while vc.is_playing():
            sleep(.1)

        await ctx.message.delete()

def setup(bot):
    bot.add_cog(ImpersonationCog(bot))