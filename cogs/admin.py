from discord.ext import commands
import discord

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

    @commands.command()
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
    bot.add_cog(AdminCog(bot))