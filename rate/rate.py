import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
from discord.ext.commands import BadArgument
import asyncio
import random

class rate:
    def __init__(self, bot):
        self.bot = bot
        self.id = bot.user.id
        self.spotify_rate = [
            'It couldn\'t be worse :sick:.',
            'It\'s is pretty trash.',
            'There are a lot of better music.',
            'It\'s not good.',
            'This is at least tolerable.',
            'It could be worse.',
            'Hm, this is a little decent.',
            'Hey, this is pretty good!',
            'I could get down to this!',
            'Wow, now *this* is good music!',
            'HOLY SHIT THIS IS AN ABSOLUTE BANGER!'
        ]

    def listsort(self, thing):
        random.seed(self.id + thing.lower())
        return random.random() * 11

    @commands.group(pass_context=True, name='rate')
    async def rate(self, context):
        if context.invoked_subcommand is None:
            prefix = context.prefix
            title = '**Videm\'s Robust Rating System 9000:**\n'
            message = 'List of commands available for {}rate:\n'.format(prefix)
            message += '``{}rate someone [member]``\n'.format(prefix)
            message += '``{}rate ship [person] [person]``\n'.format(prefix)
            message += '``{}rate regularship [person] [person]``\n'.format(prefix)
            message += '``{}rate thing [thingy]``\n'.format(prefix)
            message += '``{}rate list [thingies]``\n'.format(prefix)
            message += '``{}rate people [people]``\n'.format(prefix)
            message += '``{}rate spotify [member]``\n'.format(prefix)
            em = discord.Embed(title=title, description=message, color=discord.Color.dark_blue())
            await self.bot.say(embed=em)

    @rate.command(pass_context=True)
    async def thing(self, context, *, thing: str):
        if thing:
            random.seed(self.id + thing.lower())
            rate = random.randint(0, 10)
            emoji = ':thumbsup:' if rate >= 5 else ':thumbsdown:'
            article = 'an' if rate == 8 else 'a'
            await self.bot.say('I give **{}** {} **{}/10** {}'.format(thing, article, rate, emoji))
        else:
            await self.bot.say('Do \'{}rate thing\' for more information.'.format(context.prefix))

    @rate.command(pass_context=True)
    async def someone(self, context, *, member:discord.Member=None):
        if not member:
            member = context.message.author
        name = str(member)
        image_url = member.avatar_url
        random.seed(self.id + member.id)
        rate = random.randint(0, 10)
        emoji = ':thumbsup:' if rate >= 5 else ':thumbsdown:'
        article = 'an' if rate == 8 else 'a'
        embed = discord.Embed(
            description='I give this person {} **{}/10** {}'.format(article, rate, emoji),
            colour=int(0x2F93E0)
        )
        embed.set_author(name=name, icon_url=image_url)
        await self.bot.say(embed=embed)

    @rate.command(pass_context=True)
    async def ship(self, context, person1, person2):
        if person1 and person2:
            memberconverter1 = MemberConverter(context, person1)
            memberconverter2 = MemberConverter(context, person2)
            name1 = ''
            name2 = ''
            try:
                person1 = memberconverter1.convert()
                name1 = str(person1)
                person1 = person1.id
            except BadArgument:
                name1 = str(person1)
                pass
            try:
                person2 = memberconverter2.convert()
                name2 = str(person2)
                person2 = person2.id
            except BadArgument:
                name2 = str(person2)
                pass
            shiplist = sorted([str(name1).lower(), str(name2).lower()])
            shipname = ' x '.join(shiplist)
            random.seed(self.id + ' x '.join(sorted([person1, person2])))
            rate = random.randint(0, 10)
            emoji = ':heart:' if rate >= 5 else ':broken_heart:'
            article = 'an' if rate == 8 else 'a'
            await self.bot.say('I give the **{} x {}** ship {} **{}/10** {}'.format(name1, name2, article, rate, emoji))
        else:
            await self.bot.say('Do \'{}help rate ship\' for more information.'.format(context.prefix))

    @rate.command(pass_context=True)
    async def regularship(self, context, person1: str, person2: str):
        if person1 and person2:
            shiplist = sorted([person1.lower(), person2.lower()])
            shipname = ' x '.join(shiplist)
            random.seed(self.id + shipname)
            rate = random.randint(0, 10)
            emoji = ':heart:' if rate >= 5 else ':broken_heart:'
            article = 'an' if rate == 8 else 'a'
            await self.bot.say('I give the **{} x {}** ship {} **{}/10** {}'.format(person1, person2, article, rate, emoji))
        else:
            await self.bot.say('Do \'{}help rate ship\' for more information.'.format(context.prefix))

    @rate.command(pass_context=True)
    async def ratepeople(self, context, *args):
        if len(args) > 1:
            listpeople = []
            for name in args:
                person = discord.utils.find(lambda m: m.name == name or m.nick == name or str(m) == name, context.message.server.members)
                if not person:
                    await self.bot.say(name + ' does not exist in this server.')
                    return
                else:
                    listpeople.append(person)
            choices = sorted(listpeople, key=lambda i: self.listsort(i.id), reverse=True)
            em = discord.Embed(title='Choices', colour=0x2F93E0)
            for x in range(0, len(choices)):
                em.add_field(name=str(x + 1), value=str(choices[x]), inline=False)
            await self.bot.send_message(context.message.channel, embed=em)
        else:
            await self.bot.say('Not enough choices to choose from')

    @rate.command(pass_context=True)
    async def list(self, context, *args):
        if len(args) > 1:
            listthings = list(args)
            listthings.sort(key=self.listsort, reverse=True)
            em = discord.Embed(title='Choices', colour=0x2F93E0)
            for x in range(0, len(listthings)):
                em.add_field(name=str(x + 1), value=listthings[x], inline=False)
            await self.bot.send_message(context.message.channel, embed=em)
        else:
            await self.bot.say('Not enough choices to choose from')

def setup(bot):
    bot.add_cog(rate(bot))
