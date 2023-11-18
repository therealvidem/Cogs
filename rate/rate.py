import random
import re
import discord
from discord.enums import ActivityType
from .customconverters import BetterMemberConverter
from redbot.core import commands
from discord.utils import get
from typing import Optional

EMBED_COLOR = 0x01f30a

class Rate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.id = str(bot.user.id)
        self.song_rate = [
            "It couldn't be worse :sick:.",
            "It's pretty trash.",
            'There are a lot of better music.',
            "It's not good.",
            'This is at least tolerable.',
            'It could be worse.',
            'Hm, this is a little decent.',
            'Hey, this is pretty good!',
            'I could get down to this!',
            'Wow, now *this* is good music!',
            'HOLY SHIT THIS IS AN ABSOLUTE BANGER!'
        ]
    
    def get_rate(self, thing, out_of=10):
        if isinstance(thing, str):
            random.seed(f'{self.id}{thing.lower()}')
        else:
            random.seed(f'{self.id}{thing}')
        return int(random.random() * (out_of + 1))

    @commands.group(name='rate')
    @commands.cooldown(rate=3, per=10)
    async def _rate(self, _):
        pass

    @_rate.command(name='thing')
    @commands.cooldown(rate=3, per=10)
    async def _thing(self, ctx, *, thing: str):
        if thing:
            rate = self.get_rate(thing)
            emoji = ':thumbsup:' if rate >= 5 else ':thumbsdown:'
            article = 'an' if rate == 8 else 'a'
            await ctx.send(f'I give **{thing}** {article} **{rate}/10** {emoji}')
        else:
            await ctx.send(f"Do '{ctx.prefix}rate thing' for more information.")

    @_rate.command(name='someone')
    @commands.cooldown(rate=3, per=10)
    async def _someone(self, ctx, *, member: Optional[BetterMemberConverter]):
        member = member or ctx.author
        if member:
            name = str(member)
            image_url = member.display_avatar.url
            rate = self.get_rate(member.id)
            emoji = ':thumbsup:' if rate >= 5 else ':thumbsdown:'
            article = 'an' if rate == 8 else 'a'
            embed = discord.Embed(
                description=f'I give this person {article} **{rate}/10** {emoji}',
                colour=EMBED_COLOR
            )
            embed.set_author(name=name, icon_url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Do '{ctx.prefix}help rate someone' for more information.")

    @_rate.command(name='ship')
    @commands.cooldown(rate=3, per=10)
    async def _ship(self, ctx, person1: str, person2: str):
        if person1 and person2:
            converter = BetterMemberConverter()
            person1_member = await converter.convert(ctx, person1)
            if person1_member:
                name1 = str(person1_member)
                person1 = str(person1_member.id)
            else:
                name1 = person1
            person2_member = await converter.convert(ctx, person2)
            if person2_member:  
                name2 = str(person2_member)
                person2 = str(person2_member.id)
            else:
                name2 = person2
            shipname = ' x '.join(sorted([name1, name2]))
            rate = self.get_rate(' x '.join(sorted([person1, person2])))
            emoji = ':heart:' if rate >= 5 else ':broken_heart:'
            article = 'an' if rate == 8 else 'a'
            await ctx.send(f'I give the **{shipname}** ship {article} **{rate}/10** {emoji}')
        else:
            await ctx.send(f"Do '{ctx.prefix}help rate ship' for more information.")

    @_rate.command(name='regularship')
    @commands.cooldown(rate=3, per=10)
    async def _regularship(self, ctx, person1: str, person2: str):
        if person1 and person2:
            shiplist = sorted([person1, person2])
            shipname = ' x '.join(shiplist)
            rate = self.get_rate(shipname.lower())
            emoji = ':heart:' if rate >= 5 else ':broken_heart:'
            article = 'an' if rate == 8 else 'a'
            await ctx.send(f'I give the **{shipname}** ship {article} **{rate}/10** {emoji}')
        else:
            await ctx.send(f"Do '{ctx.prefix}help rate ship' for more information.")

    @_rate.command(name='people')
    @commands.cooldown(rate=3, per=10)
    async def _people(self, ctx, *args):
        if len(args) > 1:
            converter = BetterMemberConverter()
            listpeople = []
            for arg in args:
                member = await converter.convert(ctx, arg)
                listpeople.append(member)
                if not member:
                    await ctx.send(f'Unknown member: {arg}')
                    return
            choices = sorted(listpeople, key=self.get_rate, reverse=True)
            em = discord.Embed(title='Choices', colour=EMBED_COLOR)
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
            listthings.sort(key=self.get_rate, reverse=True)
            em = discord.Embed(title='Choices', colour=EMBED_COLOR)
            for x in range(0, len(listthings)):
                em.add_field(name=str(x + 1), value=listthings[x], inline=False)
            await ctx.send(embed=em)
        else:
            await ctx.send('Not enough choices to choose from')
    
    @_rate.command('song')
    async def _song(self, ctx, *, member: Optional[BetterMemberConverter]):
        member = member or ctx.author
        activity = get(member.activities, type=ActivityType.listening)
        if not activity:
            member = ctx.guild.get_member(member.id)
            activity = get(member.activities, type=ActivityType.listening)
        if not activity and len(member.activities) > 0:
            # TODO: Bad code, refactor later
            for a in ctx.author.activities:
                if hasattr(a, 'state') and hasattr(a, 'details') and hasattr(a, 'name') and a.name == 'YouTube Music':
                    activity = a
            if not activity:
                activity = discord.utils.find(lambda a: hasattr(a, 'state') and hasattr(a, 'details'), ctx.author.activities)
        if activity:
            if type(activity) == discord.activity.Spotify:
                title = activity.title
                track_id = activity.track_id
                url = 'https://open.spotify.com/track/' + track_id
                image_url = activity.album_cover_url
                primary_artist = activity.artists[0]
                secondary_artists = activity.artists[1:]
                artists_string = primary_artist
                for i in range(0, len(secondary_artists)):
                    if i < len(secondary_artists) - 1:
                        artists_string += ', ' + secondary_artists[i]
                    else:
                        artists_string += ' and ' + secondary_artists[i]
                rate = self.get_rate(track_id)
            else:
                if activity.state.startswith('by '):
                    artists_string = activity.state[3:]
                else:
                    artists_string = activity.state
                title = activity.details
                # Only supports YouTube Music
                if 'large_image' in activity.assets and activity.assets['large_image']:
                    match = re.search(r'lh3\.googleusercontent\.com.+', activity.assets['large_image'].replace('\n', ''))
                    image_url = f'https://{match.group()}' if match else None
                url = None
                rate = self.get_rate(f'{title}{artists_string}')
            article = 'an' if rate == 8 else 'a'
            em = discord.Embed(
                title=artists_string,
                description=f'I give this track {article} **{rate}/10**. {self.song_rate[rate]}',
                colour=EMBED_COLOR
            )
            if url:
                em.set_author(name=title, url=url)
            else:
                em.set_author(name=title)
            if image_url:
                em.set_thumbnail(url=image_url)
            await ctx.send(embed=em)
        else:
            await ctx.send(f'{member} is not listening to anything.')
