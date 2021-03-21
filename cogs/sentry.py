from discord import AuditLogAction
from discord.ext import commands
from datetime import datetime, timedelta

class SentryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_voice_state_update(self, member, before, after):
    #     guild = member.guild
    #     name = guild.get_member_named(str(member))
    #     async for entry in guild.audit_logs(limit=10, action=AuditLogAction.member_move):
    #         event = entry
    #         print(entry)
    #     #check = storage.get_value(str(name), 'sentry_enabled')
    #
    #     #if event.user.name != member.name and event.id != bot.last_event.id and check and bot.sentry_on:
    #         #print("Event: " + event.user.name)
    #         #print("Member: " + member.name)
    #         #bot.last_event = event
    #     if event is not None:
    #         await name.move_to(channel=None)
    #         #await bot.ch.send(name.mention + " nice try idiot")

def setup(bot):
    bot.add_cog(SentryCog(bot))