from redbot.core import commands
import discord
from .customconverters import BetterMemberConverter
from discord.ext.commands import BadArgument
from discord.ext.commands import cooldown
import asyncio
import random

class Rate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def list_sort(self, thing):
        random.seed(str(self.bot.user.id) + thing.lower())
        return random.random() * 11

    @commands.group(name='rate', autohelp=False)
    @cooldown(3, 10)
    async def rate(self, ctx):
        if ctx.invoked_subcommand is None:
            prefix = ctx.prefix
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
            await ctx.send(embed=em)

    @rate.command(name='thing')
    @cooldown(3, 10)
    async def thing(self, ctx, *, thing: str):
        random.seed(str(self.bot.user.id) + thing.lower())
        rate = random.randint(0, 10)
        emoji = ':thumbsup:' if rate >= 5 else ':thumbsdown:'
        article = 'an' if rate == 8 else 'a'
        await ctx.send('I give **{}** {} **{}/10** {}'.format(thing, article, rate, emoji))

    @rate.command(name='someone')
    @cooldown(3, 10)
    async def someone(self, ctx, *, member: str=None):
        member = await BetterMemberConverter().convert(ctx, member) if member else ctx.message.author
        name = str(member)
        image_url = member.avatar_url
        random.seed(str(self.bot.user.id) + str(member.id))
        rate = random.randint(0, 10)
        emoji = ':thumbsup:' if rate >= 5 else ':thumbsdown:'
        article = 'an' if rate == 8 else 'a'
        em = discord.Embed(
            description='I give this person {} **{}/10** {}'.format(article, rate, emoji),
            colour=0x2F93E0
        )
        em.set_author(name=name, icon_url=image_url)
        await ctx.send(embed=em)

    @rate.command(name='ship')
    @cooldown(3, 10)
    async def ship(self, ctx, person1: str, person2: str):
        if person1 and person2:
            memberconverter1 = BetterMemberConverter()
            memberconverter2 = BetterMemberConverter()
            name1 = ''
            name2 = ''
            try:
                person1 = await memberconverter1.convert(ctx, person1)
                name1 = str(person1)
                person1 = str(person1.id)
            except:
                name1 = person1
                pass
            try:
                person2 = await memberconverter2.convert(ctx, person2)
                name2 = str(person2)
                person2 = str(person2.id)
            except:
                name2 = person2
                pass
            shiplist = sorted([name1.lower(), name2.lower()])
            shipname = ' x '.join(shiplist)
            random.seed(str(self.bot.user.id) + ' x '.join(sorted([person1, person2])))
            rate = random.randint(0, 10)
            emoji = ':heart:' if rate >= 5 else ':broken_heart:'
            article = 'an' if rate == 8 else 'a'
            await ctx.send('I give the **{}** ship {} **{}/10** {}'.format(shipname, article, rate, emoji))

    @rate.command(name='regularship')
    @cooldown(3, 10)
    async def regularship(self, ctx, person1: str, person2: str):
        shiplist = sorted([person1.lower(), person2.lower()])
        shipname = ' x '.join(shiplist)
        random.seed(str(self.bot.user.id) + shipname)
        rate = random.randint(0, 10)
        emoji = ':heart:' if rate >= 5 else ':broken_heart:'
        article = 'an' if rate == 8 else 'a'
        await ctx.send('I give the **{} x {}** ship {} **{}/10** {}'.format(person1, person2, article, rate, emoji))

    @rate.command(name='listpeople')
    @cooldown(3, 10)
    async def listpeople(self, ctx, *args):
        if len(args) > 1:
            listpeople = []
            for name in args:
                person = await BetterMemberConverter().convert(ctx, name)
                if not person:
                    await ctx.send(name + ' does not exist in this server.')
                    return
                else:
                    listpeople.append(person)
            choices = sorted(listpeople, key=lambda i: self.list_sort(str(i.id)), reverse=True)
            em = discord.Embed(title='Choices', colour=0x2F93E0)
            for x in range(0, len(choices)):
                em.add_field(name=str(x + 1), value=str(choices[x]), inline=False)
            await ctx.send(embed=em)
        else:
            await ctx.send('Not enough choices to choose from')

    @rate.command(name='list')
    @cooldown(3, 10)
    async def list(self, ctx, *args):
        if len(args) > 1:
            listthings = list(args)
            listthings.sort(key=self.list_sort, reverse=True)
            em = discord.Embed(title='Choices', colour=0x2F93E0)
            for x in range(0, len(listthings)):
                em.add_field(name=str(x + 1), value=listthings[x], inline=False)
            await ctx.send(embed=em)
        else:
            await ctx.send('Not enough choices to choose from')
    
    @rate.command(name='spotify')
    @cooldown(3, 10)
    async def spotify(self, ctx, *, member: str=None):
        member = await BetterMemberConverter().convert(ctx, member) if member else ctx.message.author
        activity = member.activity
        if activity and activity.type == discord.ActivityType.listening:
            if type(activity) == discord.activity.Spotify:
                title = activity.title
                track_id = activity.track_id
                url = 'https://open.spotify.com/track/' + track_id
                image_url = activity.album_cover_url
                primary_artist = activity.artists[0]
                secondary_artists = activity.artists[1:]
                artists_string = 'by {}'.format(primary_artist)
                for i in range(0, len(secondary_artists)):
                    if i < len(secondary_artists) - 1:
                        artists_string += ', ' + secondary_artists[i]
                    else:
                        artists_string += ' and ' + secondary_artists[i]
                random.seed(str(self.bot.user.id) + track_id.lower())
            else:
                artists_string = 'by {}'.format(activity.state)
                title = activity.details
                image_url = None
                random.seed(str(self.bot.user.id) + title.lower() + artists_string.lower())
            rate = random.randint(0, 10)
            article = 'an' if rate == 8 else 'a'
            em = discord.Embed(
                title=artists_string,
                description='I give this track {} **{}/10**.'.format(article, rate),
                colour=int(0x2F93E0)
            )
            if url:
                em.set_author(name=title, url=url)
            else:
                em.set_author(name=title)
            if image_url:
                em.set_thumbnail(url=image_url)
            await ctx.send(embed=em)
        else:
            await ctx.send('{} is not listening to anything on Spotify.'.format(member))