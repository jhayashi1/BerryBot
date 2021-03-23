from discord.ext import commands

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def connect(self, ctx):
        try:
            channel = ctx.author.voice.channel
            await channel.connect()
        except:
            await ctx.send("You're not connected to a channel!")

    @commands.command()
    async def join(self, ctx, *args):
        try:
            converter = commands.MemberConverter()
            member = await converter.convert(ctx=ctx, argument=' '.join(args))
            await member.voice.channel.connect()
        except:
            await ctx.send("User not in voice channel or invalid user")


    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def close(self, ctx):
        await self.bot.close()

def setup(bot):
    bot.add_cog(AdminCog(bot))