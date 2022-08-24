import discord
from discord.ext import commands
import random
import praw

class RedditCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reddit(self, ctx, arg1):
        print(arg1)
        try:
            r = praw.Reddit(client_id='HrUKB0WP3a6A6Q',
                            client_secret='rca8u8gHsBLR8xbmho-5FysK8i0cwA',
                            user_agent='Discord bot')

            user = r.redditor(arg1)
            submissions = list(user.submissions.new())
            submission = random.choice(submissions)
            url = submission.url

            embed = discord.Embed(
                title=str(submission.title + " from r/" + str(submission.subreddit)),
                colour=discord.Colour.orange(),
                description="`" + url + "`"
            )
            if submission.is_self or "youtube.com" in submission.selftext:
                embed.add_field(name="**Submission Text:**", value=submission.selftext, inline=False)
            else:
                embed.set_image(url=url)

            embed.set_author(name='u/' + user.name,
                             icon_url=user.icon_img)
            embed.set_footer(text=submission.permalink)

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send("Error! Invalid user")
            print(e)

async def setup(bot):
    await bot.add_cog(RedditCog(bot))