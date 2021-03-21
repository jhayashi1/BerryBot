from discord.ext import commands
import requests
import shutil

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
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def impersonate(self, ctx, *args):
        converter = commands.MemberConverter()
        member = await converter.convert(ctx=ctx, argument=' '.join(args))
        if (member is not None):
            pfp = member.avatar_url
            r = requests.get(pfp, stream=True)

            if r.status_code == 200:
                r.raw.decode_content = True

                with open("Currentpfp.png", 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

                with open("Currentpfp.png", 'rb') as p:
                    pic = p.read()

                await self.bot.user.edit(avatar=pic)
                await ctx.guild.get_member(self.bot.user.id).edit(nick=' '.join(args))
                await ctx.send("success")
        else:
            await ctx.send("invalid user")

        await ctx.message.delete()

    @commands.command()
    async def default(self, ctx):
        with open("default.png", 'rb') as p:
            pic = p.read()
        await self.bot.user.edit(avatar=pic)
        await ctx.guild.get_member(self.bot.user.id).edit(nick="BerryBot")


    @commands.command()
    async def close(self, ctx):
        await self.bot.close()

def setup(bot):
    bot.add_cog(AdminCog(bot))