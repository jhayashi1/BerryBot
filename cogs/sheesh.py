from discord.ext import commands
from time import sleep
import discord

class SheeshCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sheesh(self, ctx):
        id = 133784395612946432

        guilds = self.bot.guilds
        target_channel = None
        check = False

        for guild in guilds:
            for channel in guild.voice_channels:
                for member in channel.members:
                    if member.id == id:
                        target_channel = channel
            if target_channel is not None:
                vc = await target_channel.connect()
                vc.play(discord.FFmpegPCMAudio(executable="./ffmpeg/bin/ffmpeg.exe", source="./tools/audio/sheesh.mp3"))
                while vc.is_playing():
                    sleep(1)
                await vc.disconnect()
                await ctx.message.delete()
                return

        await ctx.send("Joey not found")

async def setup(bot):
    await bot.add_cog(SheeshCog(bot))