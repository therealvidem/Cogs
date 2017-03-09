
import discord
from discord.ext import commands
import asyncio
import random

class rate:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, name='rate')
    async def _rate(self, context, *, member: discord.Member=None):
        channel = context.message.channel
        if member is not None:
            name = member.display_name
            random.seed(name)
            rate = random.randint(0, 10)
            emoji = ''
            if rate >= 5:
                emoji = ':thumbsup:'
            else:
                emoji = ':thumbsdown:'
            self.bot.send_message(channel, 'I give {0} a {1}/10 {2}'.format(name, rate, emoji)
        
    # @_rate.command(pass_context=True, name='

def setup(bot):
    n = rate(bot)
    bot.add_listener(n.listener, "on_message")
    bot.add_cog(n)
