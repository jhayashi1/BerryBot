from discord.ext import commands
import discord

ERROR_MESSAGE = "Usage: trigger [add|remove|list] [trigger] [response]"

class TriggersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trigger(self, ctx, *args):

        check = error_check(args)
        
        if (check == 0):
            await ctx.send("Successfully added " + args[1] + " " + args[2])
        elif (check == 1):
            await ctx.send("Successfully removed " + args[1])
        elif (check == 2):
            await ctx.send("TODO: display list")
        else:
            await ctx.send(ERROR_MESSAGE)

def error_check(args):
    if args[0] == "add":
        if len(args) == 3:
            return 0
    elif args[0] == "remove":
        if len(args) == 2:
            return 1
    elif args[0] == "list":
        return 2

    return -1

def setup(bot):
    bot.add_cog(TriggersCog(bot))