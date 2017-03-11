import discord
from discord.ext import commands
import asyncio
import random

class rate:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, name='rate')
    async def _rate(self, context, thing: str=None):
        if context.invoked_subcommand is None:
            if thing:
                isdiscordmember = False
                for member in context.message.server.members:
                    if thing == member.display_name:
                        isdiscordmember = True
                if thing is discord.Member:
                    await self.bot.say('is discord member')
                else:
                    await self.bot.say('is not discord member')
            else:
                await self.bot.say('Do {0}help rate for more information.'.format(context.prefix))
            
    @_rate.command(pass_context=True, name='discordmember')
    async def _discordmember(self, context, *, member: discord.Member=None):
        if member:
            name = member.display_name
            random.seed(name)
            rate = random.randint(0, 10)
            emoji = ''
            if rate >= 5:
                emoji = ':thumbsup:'
            else:
                emoji = ':thumbsdown:'
            await self.bot.say('I give {0} a {1}/10 {2}'.format(name, rate, emoji))
        else:
            await self.bot.say('Do {0}help rate discordmember for more information.'.format(context.prefix))
            
    @_rate.command(pass_context=True, name='ship')
    async def _ship(self, context, member1: discord.Member=None, member2: discord.Member=None):
        if member1 and member2:
            name1 = member1.display_name
            name2 = member2.display_name
            shiplist = [name1, name2]
            shiplist.sort()
            shipname = ' x '.join(shiplist)
            random.seed(shipname)
            rate = random.randint(0, 10)
            emoji = ''
            if rate >= 5:
                emoji = ':heart:'
            else:
                emoji = ':broken_heart:'
            article = 'an' if rate == 8 else 'a'
            await self.bot.say('I give the {0} {1} {2}/10 {3}'.format(shipname, article, rate, emoji))
        else:
            await self.bot.say('Do {0}help rate ship for more information.'.format(context.prefix))

def setup(bot):
    bot.add_cog(rate(bot))


