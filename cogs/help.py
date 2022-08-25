from discord.ext import commands
import discord
import utils

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #TODO double check to make sure the embed works
    @commands.command(brief='Brings up the help menu')
    async def help(self, ctx):
        help_embed = discord.Embed(title="BerryBot Commands", color=discord.Color.orange())
        for command in self.bot.walk_commands():
            help_embed.add_field(
                name=command.name,
                value=command.brief,
                inline=True
            )

        await utils.sendResponse(ctx, embed=help_embed)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))