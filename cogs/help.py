from discord.ext import commands
import discord

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', brief='Brings up the help menu')
    async def help(self, ctx):
        help_embed = discord.Embed(title="BerryBot Commands", color=discord.Color.orange())
        lines = open("./tools/help.txt").read().splitlines()

        for line in lines:
            command = line.split("\t")
            help_embed.add_field(
                name=command[0],
                value=command[1],
                inline=False
            )

        await ctx.send(embed=help_embed)


def setup(bot):
    bot.add_cog(HelpCog(bot))