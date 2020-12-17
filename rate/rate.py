from discord.enums import ActivityType
from redbot.core import commands
import discord
from .customconverters import BetterMemberConverter
from discord.ext.commands import cooldown
from discord.utils import get
import random

class Rate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def list_sort(self, thing):
        random.seed(str(self.bot.user.id) + thing.lower())
        return random.random() * 11

    @commands.group(name='rate', autohelp=False)
    @cooldown(3, 10)
    async def _rate(self, ctx):
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

    @_rate.command(name='thing')
    @cooldown(3, 10)
    async def thing(self, ctx, *, thing: str):
        random.seed(str(self.bot.user.id) + thing.lower())
        rate = random.randint(0, 10)
        emoji = ':thumbsup:' if rate >= 5 else ':thumbsdown:'
        article = 'an' if rate == 8 else 'a'
        await ctx.send('I give **{}** {} **{}/10** {}'.format(thing, article, rate, emoji))

    @_rate.command(name='someone')
    @commands.cooldown(rate=3, per=10)
    async def _someone(self, ctx, *, member: BetterMemberConverter):
        if member:
            name = str(member)
            image_url = member.avatar_url
            random.seed(self.id + str(member.id))
            rate = random.randint(0, 10)
            emoji = ':thumbsup:' if rate >= 5 else ':thumbsdown:'
            article = 'an' if rate == 8 else 'a'
            embed = discord.Embed(
                description='I give this person {} **{}/10** {}'.format(article, rate, emoji),
                colour=int(0x2F93E0)
            )
            embed.set_author(name=name, icon_url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Do \'{}help rate someone\' for more information.'.format(ctx.prefix))

    @_rate.command(name='ship')
    @commands.cooldown(rate=3, per=10)
    async def _ship(self, ctx, person1: BetterMemberConverter, person2: BetterMemberConverter):
        if person1 and person2:
            name1 = ''
            name2 = ''
            person1_member = await person1.convert(ctx, person1)
            if person1_member:  
                name1 = str(person1)
                person1 = str(person1_member.id)
            else:
                name1 = str(person1)
            person2_member = await person2.convert(ctx, person2)
            if person2_member:  
                name2 = str(person2)
                person2 = str(person2_member.id)
            else:
                name2 = str(person2)
            random.seed(self.id + ' x '.join(sorted([person1, person2])))
            rate = random.randint(0, 10)
            emoji = ':heart:' if rate >= 5 else ':broken_heart:'
            article = 'an' if rate == 8 else 'a'
            await ctx.send('I give the **{} x {}** ship {} **{}/10** {}'.format(name1, name2, article, rate, emoji))
        else:
            await ctx.send('Do \'{}help rate ship\' for more information.'.format(ctx.prefix))

    @_rate.command(name='regularship')
    @commands.cooldown(rate=3, per=10)
    async def _regularship(self, ctx, person1, person2):
        if person1 and person2:
            shiplist = sorted([person1.lower(), person2.lower()])
            shipname = ' x '.join(shiplist)
            random.seed(self.id + shipname)
            rate = random.randint(0, 10)
            emoji = ':heart:' if rate >= 5 else ':broken_heart:'
            article = 'an' if rate == 8 else 'a'
            await ctx.send('I give the **{} x {}** ship {} **{}/10** {}'.format(person1, person2, article, rate, emoji))
        else:
            await ctx.send('Do \'{}help rate ship\' for more information.'.format(ctx.prefix))

    @_rate.command(name='ratepeople')
    @commands.cooldown(rate=3, per=10)
    async def _ratepeople(self, ctx, *args):
        if len(args) > 1:
            listpeople = []
            for name in args:
                person = discord.utils.find(lambda m: m.name == name or m.nick == name or str(m) == name, ctx.message.server.members)
                if not person:
                    await ctx.send(name + ' does not exist in this server.')
                    return
                else:
                    listpeople.append(person)
            choices = sorted(listpeople, key=lambda i: self.listsort(str(i.id)), reverse=True)
            em = discord.Embed(title='Choices', colour=0x2F93E0)
            for x in range(0, len(choices)):
                em.add_field(name=str(x + 1), value=str(choices[x]), inline=False)
            await ctx.send(embed=em)
        else:
            await ctx.send('Not enough choices to choose from')

    @_rate.command('list')
    @commands.cooldown(rate=3, per=10)
    async def _list(self, ctx, *args):
        if len(args) > 1:
            listthings = list(args)
            listthings.sort(key=self.listsort, reverse=True)
            em = discord.Embed(title='Choices', colour=0x2F93E0)
            for x in range(0, len(listthings)):
                em.add_field(name=str(x + 1), value=listthings[x], inline=False)
            await ctx.send(embed=em)
        else:
            await ctx.send('Not enough choices to choose from')
    
    @_rate.command('spotify')
    async def _spotify(self, ctx, *, member: BetterMemberConverter):
        activity = get(member.activities, type=ActivityType.listening)
        if activity:
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
                url = None
                random.seed(str(self.bot.user.id) + title.lower() + artists_string.lower())
            rate = random.randint(0, 10)
            article = 'an' if rate == 8 else 'a'
            em = discord.Embed(
                title=artists_string,
                description='I give this track {} **{}/10**.'.format(article, rate, self.spotify_rate[rate]),
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
