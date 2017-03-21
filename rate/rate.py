import discord
from discord.ext import commands
import asyncio
import random

class rate:
    def __init__(self, bot):
        self.bot = bot
        self.id = bot.user.id

    @commands.group(pass_context=True, name='rate')
    async def _rate(self, context):
        if context.invoked_subcommand is None:
            prefix = context.prefix
            title = '**Videm\'s Robust Rating System 9000:**\n'
            message = 'List of commands available for {}rate:\n'.format(prefix)
            message += '``{}rate someone [member]``\n'.format(prefix)
            message += '``{}rate ship [person] [person]``\n'.format(prefix)
            message += '``{}rate thing [thingy]``\n'.format(prefix)
            message += '``{}rate list [thingies]``\n'.format(prefix)
            em = discord.Embed(title=title, description=message, color=discord.Color.dark_blue())
            await self.bot.say(embed=em)
    
    @_rate.command(pass_context=True, name='thing')
    async def _thing(self, context, *, thing: str=None):
        if thing:
            random.seed(self.id + thing.lower())
            rate = random.randint(0, 10)
            emoji = ':thumbsup:' if rate >= 5 else ':thumbsdown:'
            article = 'an' if rate == 8 else 'a'
            await self.bot.say('I give **{}** {} **{}/10** {}'.format(thing, article, rate, emoji))
        else:
            await self.bot.say('Do \'{}rate thing\' for more information.'.format(context.prefix))
    
    @_rate.command(pass_context=True, name='someone')
    async def _someone(self, context, *, member: discord.Member=None):
        if member:
            name = member.display_name
            random.seed(self.id + name.lower())
            rate = random.randint(0, 10)
            emoji = ':thumbsup:' if rate >= 5 else ':thumbsdown:'
            article = 'an' if rate == 8 else 'a'
            await self.bot.say('I give **{}** {} **{}/10** {}'.format(name, article, rate, emoji))
        else:
            await self.bot.say('Do \'{}help rate someone\' for more information.'.format(context.prefix))
            
    @_rate.command(pass_context=True, name='ship')
    async def _ship(self, context, member1, member2):
        if member1 and member2:
            name1 = str(member1)
            name2 = str(member2)
            shiplist = [name1.lower(), name2.lower()]
            shiplist.sort()
            shipname = ' x '.join(shiplist)
            random.seed(self.id + shipname)
            rate = random.randint(0, 10)
            emoji = ':heart:' if rate >= 5 else ':broken_heart:'
            article = 'an' if rate == 8 else 'a'
            await self.bot.say('I give the **{} x {}** ship {} **{}/10** {}'.format(name1, name2, article, rate, emoji))
        else:
            await self.bot.say('Do \'{}help rate ship\' for more information.'.format(context.prefix))
            
    @_rate.command(pass_context=True, name='list')
    async def _list(self, context, *args):
        author = context.message.author
        choices = list(args)
        if len(choices) > 1:
            random.seed(', '.join(choices))
            random.shuffle(choices)
            em = discord.Embed(title='Choices', colour=0x2F93E0)
            em.set_author(name=str(author), icon_url=author.avatar_url)
            for x in range(0, len(choices)):
                em.add_field(name=x + 1, value=choices[x])
            await self.bot.send_message(context.message.channel, embed=em)
        else:
            await self.bot.say('Not enough choices to choose from')

def setup(bot):
    bot.add_cog(rate(bot))


