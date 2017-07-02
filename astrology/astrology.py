import discord
from discord.ext import commands
import asyncio
import random
import os
import collections
from datetime import datetime
from geopy.geocoders import GoogleV3
from flatlib.datetime import Datetime
from flatlib.chart import Chart
from flatlib.geopos import GeoPos
from flatlib import const
from .utils.dataIO import dataIO

class astrology:
    def __init__(self, bot):
        self.bot = bot
        self.profile_path = 'data/astrology/profiles.json'
        self.profiles = dataIO.load_json(self.profile_path)
        self.chart_cache = collections.OrderedDict()
        self.locator = GoogleV3()

    async def profile_exists(self, context, name: str=None, member: discord.Member=None, send_message: bool=True):
        if not member:
            member = context.message.author
        if not name:
            if send_message:
                await self.bot.say('You don\'t have any profiles! Do "{}astrology profile create" to create a profile!'.format(context.prefix))
            return
        if member.id not in self.profiles:
            if send_message:
                await self.bot.say('You don\'t have any profiles! Do "{}astrology profile create" to create a profile!'.format(context.prefix))
            return
        if name not in self.profiles[member.id]:
            if send_message:
                await self.bot.say('That profile doesn\'t exist!')
            return
        return self.profiles[member.id][name]

    async def is_owner(self, context, name, member: discord.Member=None, send_message: bool=True):
        if not member:
            member = context.message.author
        profile = await self.profile_exists(context, name)
        if profile:
            if profile['creator'] != member.id:
                if send_message:
                    await self.bot.say('You are not the owner of that profile!')
                return False
            return True
        return False

    @commands.group(pass_context=True, invoke_without_command=True)
    async def astrology(self, context):
        message = 'Welcome to videm\'s Astrology Cog!\n'
        message += 'This is an astrology-centered cog in which you can create and store mutliple profiles on the bot to make (not draw) charts.\n\n'
        message += 'To create a profile, use this command:\n'
        message += '{prefix}astrology profile create [profile name] [birthyear] [birthmonth] [birthday] [birthhour] [birthminute] [location]\n'
        message += 'You may use a city as a location.\n\n'
        message += 'After you create a profile, you can view its properties by executing "{prefix}astrology profile [profile_name]".\n'
        message += 'You can then look at each of the profile\'s planet signs by executing "{prefix}astrology get sign [profile_name] [planet]".\n'
        message += 'Do {prefix}astrology commandlist for more information!'
        message = message.format(prefix=context.prefix)
        em = discord.Embed(title='Videm\'s Astrology Cog', colour=0xFF3E28)
        em.set_thumbnail(url='https://www.syracusenewtimes.com/wp-content/uploads/2015/12/astrology.jpg')
        em.add_field(name='Info:', value=message)
        await self.bot.say(embed=em)

    @astrology.group(pass_context=True, invoke_without_command=True)
    async def profile(self, context, name: str):
        if not await self.profile_exists(context, name):
            return
        authorid = context.message.author.id
        profile = self.profiles[authorid][name]
        em = discord.Embed(title='{}\'s Birth Profile'.format(name), colour=0x2F93E0)
        for propname, prop in profile.items():
            if propname != 'creator':
                if isinstance(prop, str):
                    prop = prop.lower().title()
                em.add_field(name=propname.title(), value=prop)
        await self.bot.say(embed=em)

    @profile.command(pass_context=True)
    async def create(self, context, name: str, birth_year: int, birth_month: int, birth_day: int, birth_hour: int, birth_minute: int, location: str):
        authorid = context.message.author.id
        if authorid not in self.profiles:
            self.profiles[authorid] = {}
        if name in self.profiles:
            await self.bot.say('That person is already exists!')
            return
        self.profiles[authorid][name] = {
            'creator': context.message.author.id,
            'name': name,
            'year': birth_year,
            'month': birth_month,
            'day': birth_day,
            'hour': birth_hour,
            'minute': birth_minute,
            'location': location
        }
        if not await self.get_chart(context, name):
            del self.profiles[authorid][name]
            return
        dataIO.save_json(self.profile_path, self.profiles)
        await self.bot.say('Successfully created profile for {}'.format(name))

    @profile.command(pass_context=True)
    async def remove(self, context, name: str):
        if not await self.profile_exists(context, name):
            return
        authorid = context.message.author.id
        del self.profiles[authorid][name]
        dataIO.save_json(self.profile_path, self.profiles)
        await self.bot.say('Successfully removed {}\'s profile!'.format(name))

    @astrology.command(pass_context=True)
    async def reset_all(self, context):
        if self.bot.is_owner(context.message.author.id): 
            self.profiles = []
            dataIO.save_json(self,profile_path, self.profiles)
            await self.bot.say('Successfully resetted all profiles!')

    async def change_prop(self, context, name, property, new_value):
        if not await self.profile_exists(context, name) or not await self.is_owner(context, name):
            return
        authorid = context.message.author.id
        profile = self.profiles[authorid][name]
        if property not in profile:
            await self.bot.say('{} does not exist as a property!'.format(property))
            return
        if property == 'creator':
            await self.bot.say('You can\'t edit the creator of this profile!')
            return
        if isinstance(profile[property], int):
            try:
                new_value = int(new_value)
            except:
                await self.bot.say('That\'s not a proper number!')
                return
        profile[property] = new_value
        dataIO.save_json(self.profile_path, self.profiles)
        await self.bot.say('Changed the {} of {} to {}!'.format(property, name, new_value))

    @profile.command(pass_context=True)
    async def edit(self, context, name: str, property: str, new_value):
        await self.change_prop(context, name, property, new_value)

    @profile.command(pass_context=True)
    async def list(self, context):
        authorid = context.message.author.id
        if not authorid in self.profiles:
            await self.bot.say('You don\'t have any profiles! Do "{}astrology profile create" to create a profile!'.format(context.prefix))
            return
        em = discord.Embed(title='Profiles of {}'.format(context.message.author.name), colour=0x2F93E0)
        for name, profile in self.profiles[authorid].items():
            em.add_field(name=name, value='{}/{}/{}'.format(str(profile['year']), str(profile['month']), str(profile['day'])))
        await self.bot.say(embed=em)

    @profile.command(pass_context=True)
    async def view(self, context, member: discord.Member, name: str):
        if name:
            if not await self.profile_exists(context, name, member):
                return
            authorid = member.id
            profile = self.profiles[authorid][name]
            em = discord.Embed(title='{}\'s Birth Profile'.format(name), colour=0x2F93E0)
            for propname, prop in profile.items():
                if propname != 'creator':
                    if isinstance(prop, str):
                        prop = prop.lower().title()
                    em.add_field(name=propname.title(), value=prop)
            await self.bot.say(embed=em)
        else:
            authorid = member.id
            if not authorid in self.profiles:
                await self.bot.say('That person doesn\'t have any profiles!'.format(context.prefix))
                return
            em = discord.Embed(title='Profiles of {}'.format(member.name), colour=0x2F93E0)
            for name, profile in self.profiles[authorid].items():
                em.add_field(name=name, value='{}/{}/{}'.format(str(profile['year']), str(profile['month']), str(profile['day'])))
            await self.bot.say(embed=em)

    async def get_chart(self, context, name, send_message=True):
        authorid = context.message.author.id
        if not await self.profile_exists(context, name) or not await self.is_owner(context, name):
            return
        if name in self.chart_cache:
            return self.chart_cache[name]
        profile = self.profiles[authorid][name]
        year = profile['year']
        month = profile['month']
        day = profile['day']
        hour = profile['hour']
        minute = profile['minute']
        try:
            dt = datetime(year, month, day, hour, minute)
        except ValueError as e:
            await self.bot.say(str(e).capitalize())
            return
        formatted_date = dt.strftime('%Y/%m/%d')
        formatted_time = dt.strftime('%H:%M')
        location = self.locator.geocode(profile['location'])
        if not location:
            await self.bot.say('That\'s not a valid location!')
            return
        tz = self.locator.timezone([location.latitude, location.longitude])
        tz_offset = tz.utcoffset(dt).total_seconds() / 3600
        chart = Chart(Datetime(formatted_date, formatted_time, tz_offset), GeoPos(location.latitude, location.longitude), IDs=const.LIST_OBJECTS)
        self.chart_cache[name] = chart
        if len(self.chart_cache) > 50:
            del self.chart_cache[0]
        return chart

    @profile.command(pass_context=True)
    async def planets(self, context, name: str):
        chart = await self.get_chart(context, name)
        if not chart:
            return
        em = discord.Embed(title='Signs of {}'.format(name), colour=0x2F93E0)
        for obj in const.LIST_OBJECTS:
            sign = chart.get(obj).sign
            em.add_field(name=obj, value=sign)
        await self.bot.say(embed=em)

    @astrology.group(pass_context=True)
    async def get(self, context):
        return

    @get.command(pass_context=True)
    async def sign(self, context, name: str, object: str):
        chart = await self.get_chart(context, name)
        if not chart:
            return
        object = (x for x in const.LIST_OBJECTS if x.lower() == object.lower()) or None
        try:
            sign = chart.get(object).sign
            await self.bot.say('{}\'s sign in {} is {}.'.format(name, object, sign))
        except KeyError:
            await self.bot.say('That\'s not a valid astrological object!')

    @get.command(pass_context=True)
    async def house(self, context, name: str, house_num: int):
        chart = await self.get_chart(context, name)
        if not chart:
            return
        house = (x for x in const.LIST_HOUSES if x.lower() == 'house' + str(house)) or None
        try:
            sign = chart.get(house).sign
            await self.bot.say('{}\'s sign in House {} is {}.'.format(name, house_num, sign))
        except KeyError:
            await self.bot.say('That\'s not a valid house!')

def check_folders():
    if not os.path.exists('data/astrology'):
        print('test')
        os.makedirs('data/astrology')

def check_files():
    f = 'data/astrology/profiles.json'
    if not dataIO.is_valid_json(f):
        dataIO.save_json(f, {})

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(astrology(bot))