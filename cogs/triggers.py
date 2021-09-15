from discord.ext import commands
import discord

class TriggersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trigger(self, ctx, *args):
        
        await ctx.send(args)

def setup(bot):
    bot.add_cog(TriggersCog(bot))