import discord
from discord.ext import commands
import asyncio
import random

class rate:
    def __init__(self, bot):
        self.bot = bot
        
    async def ship(member1: discord.Member=None, member2: discord.Member=None):
        if member1 and member2:
            name1 = member1.display_name
            name2 = member2.display_name
            shiplist = [name1.lower(), name2.lower()]
            shiplist.sort()
            shipname = ' x '.join(shiplist)
            random.seed(shipname)
            rate = random.randint(0, 10)
            emoji = ':heart:' if rate >= 5 else ':broken_heart:'
            article = 'an' if rate == 8 else 'a'
            self.bot.say('I give the {} {} {}/10 {}'.format(shipname, article, rate, emoji))
        else:
            self.bot.say('Do \'{}help rate ship\' for more information.'.format(context.prefix))
            
    async def ship(name1: str=None, name2: str=None):
        if name1 and name2:
            shiplist = [name1.lower(), name2.lower()]
            shiplist.sort()
            shipname = ' x '.join(shiplist)
            random.seed(shipname)
            rate = random.randint(0, 10)
            emoji = ':heart:' if rate >= 5 else ':broken_heart:'
            article = 'an' if rate == 8 else 'a'
            self.bot.say('I give the {} {} {}/10 {}'.format(shipname, article, rate, emoji))
        else:
            self.bot.say('Do \'{}help rate ship\' for more information.'.format(context.prefix))

    @commands.group(pass_context=True, name='rate')
    async def _rate(self, context):
        if context.invoked_subcommand is None:
            prefix = context.prefix
            title = '**VidemBot\'s Robust Rating System 9000:**\n'
            message = 'List of commands available for {}rate:\n'.format(prefix)
            message += '``{}rate someone [member]``\n'.format(prefix)
            message += '``{}rate ship [person] [person]``\n'.format(prefix)
            message += '``{}rate thing [thingy]``\n'.format(prefix)
            em = discord.Embed(title=title, description=message, color=discord.Color.dark_blue())
            await self.bot.say(embed=em)
    
    @_rate.command(pass_context=True, name='thing')
    async def _thing(self, context, *, thing: str=None):
        if thing:
            random.seed(thing.lower())
            rate = random.randint(0, 10)
            emoji = ':thumbsup:' if rate >= 5 else ':thumbsdown:'
            await self.bot.say('I give {} a {}/10 {}'.format(thing, rate, emoji))
        else:
            await self.bot.say('Do \'{}rate thing\' for more information.'.format(context.prefix))
    
    @_rate.command(pass_context=True, name='someone')
    async def _someone(self, context, *, member: discord.Member=None):
        if member:
            name = member.display_name
            random.seed(name.lower())
            rate = random.randint(0, 10)
            emoji = ':thumbsup:' if rate >= 5 else ':thumbsdown:'
            await self.bot.say('I give {} a {}/10 {}'.format(name, rate, emoji))
        else:
            await self.bot.say('Do \'{}help rate someone\' for more information.'.format(context.prefix))
            
    @_rate.command(pass_context=True, name='ship')
    async def _ship(self, context, *, member1, member2):
        self.ship(member1, member2)

def setup(bot):
    bot.add_cog(rate(bot))


