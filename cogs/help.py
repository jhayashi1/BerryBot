from discord.ext import commands
import discord

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Brings up the help menu')
    async def help(self, ctx):
        help_embed = discord.Embed(title="BerryBot Commands", color=discord.Color.orange())
        for command in self.bot.walk_commands():
            print(command.brief)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))