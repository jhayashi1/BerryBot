from discord.ext import commands

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def assemble(self, ctx):
        home = ctx.author.voice.channel
        channels = ctx.guild.voice_channels

        if home is not None:
            for channel in channels:
                for member in channel.members:
                    await member.move_to(home)
        else:
            await ctx.send("You're not in a channel!")

def setup(bot):
    bot.add_cog(AdminCog(bot))