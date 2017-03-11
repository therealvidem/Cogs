import discord
from discord.ext import commands
import asyncio
import random

class rate:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, name='rate')
    async def _rate(self, context):
        if context.invoked_subcommand is None:
            await self.bot.send_message(context.message.channel, 'Do {0}help rate for more information.'.format(context.prefix))
            
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
            
    @_rate.command(pass_context=True, name='discordship')
    async def _discordship(self, context, *, member1: discord.Member=None, member2: discord.Member=None):
        if member1 and member2:
            name1 = member1.display_name
            name2 = member2.display_name
            random.seed(name1 + name2)
            rate = random.randint(0, 10)
            emoji = ''
            if rate >= 5:
                emoji = ':heart:'
            else:
                emoji = ':broken_heart:'
            await self.bot.say('I give the {0} x {1} a {2}/10 {3}'.format(name1, name2, rate, emoji))

def setup(bot):
    bot.add_cog(rate(bot))


