from discord.ext import commands

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_check = True
        self.chat_react = False

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
        self.voice_check = False

    @commands.command()
    async def close(self, ctx):
        await self.bot.close()

    @commands.command()
    async def react(self, ctx):
        if self.chat_react:
            self.chat_react = False
        else:
            self.chat_react = True

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 198587944783577088:
            if "banning" in message.content and "bot" in message.content:
                await message.author.move_to(channel=None)
                await message.channel.send("not today fucko")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id == self.bot.user.id:
            if before is not None and after is None and self.voice_check:
                await before.channel.connect()
                print("Was disconnected")
            elif before is not None and after is None:
                self.voice_check = True
                print("Disconnect command")
            else:
                print("no pass")

    @commands.Cog.listener()
    async def on_message(self, message):
        emojis = ['amogus', 'yayou', 'league']

        for emoji in message.guild.emojis:
            if emoji.name in emojis:
                await message.add_reaction(emoji=emoji)



def setup(bot):
    bot.add_cog(AdminCog(bot))

def disconnect_member(member):
    print("yeet")