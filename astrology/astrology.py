import discord
from discord.ext import commands
import asyncio
import random
import os
import calendar
import collections
import simplejson as json
from datetime import datetime
from geopy.geocoders import GoogleV3
from flatlib.datetime import Datetime
from flatlib.chart import Chart
from flatlib.geopos import GeoPos
from flatlib import const
from flatlib import angle
from .utils.dataIO import dataIO
from bs4 import BeautifulSoup
import aiohttp

house_nums = ['nulla', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']

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
        # print(json.dumps(self.profiles[member.id]))
        if name not in self.profiles[member.id]:
            if send_message:
                await self.bot.say('That profile doesn\'t exist!')
            return
        return self.profiles[member.id][name]

    async def change_prop(self, context, name, property, new_value):
        if not await self.profile_exists(context, name):
            return
        authorid = context.message.author.id
        profile = self.profiles[authorid][name]
        if property not in profile:
            await self.bot.say('{} does not exist as a property!'.format(property))
            return
        if property == 'creator':
            await self.bot.say('You can\'t edit the creator of this profile!')
            return
        if property == 'name':
            if new_value.lower() in [x.lower() for x in self.profiles[authorid]]:
                await self.bot.say('You can\'t change the profile\'s to {} since there\'s already a profile named that!')
                return
        if new_value == profile[property]:
            await self.bot.say('Nothing was changed.')
            return 
        old_value = profile[property]
        if not new_value:
            profile[property] = ''
            if not await self.get_chart(context, name):
                profile[property] = old_value
                return
            dataIO.save_json(self.profile_path, self.profiles)
            await self.bot.say('Successfully reset the {} of {}!'.format(property, name))
            return
        if new_value.isdecimal():
            new_value = int(new_value)
        profile[property] = new_value
        if not await self.get_chart(context, name):
            profile[property] = old_value
            return
        dataIO.save_json(self.profile_path, self.profiles)
        await self.bot.say('Successfully changed the {} of {} to {}!'.format(property, name, new_value))

    async def get_chart(self, context, name, member: discord.Member=None, send_message=True):
        authorid = None
        if member:
            authorid = member.id
        else:
            authorid = context.message.author.id
        if not await self.profile_exists(context, name, member):
            return
        if name in self.chart_cache:
            return self.chart_cache[name]
        profile = self.profiles[authorid][name]
        year = profile['year']
        month = profile['month']
        if month in list(calendar.month_name):
            month = int(list(calendar.month_name).index(month))
        else:
            month = int(month)
        day = profile['day']
        hour = profile['hour']
        minute = profile['minute']
        try:
            dt = datetime(year, month, day, hour, minute)
        except ValueError as e:
            await self.bot.say(str(e).capitalize())
            return
        except TypeError as e:
            await self.bot.say('That\'s not a number!')
            return
        formatted_date = dt.strftime('%Y/%m/%d')
        formatted_time = dt.strftime('%H:%M')
        location = self.locator.geocode(profile['location'])
        if not location:
            await self.bot.say('That\'s not a valid location!')
            return
        tz = self.locator.timezone([location.latitude, location.longitude])
        tz_offset = tz.utcoffset(dt).total_seconds() / 3600
        latitude = location.latitude
        longitude = location.longitude
        if profile['latitude'] and profile['longitude']:
            latitude = profile['latitude']
            longitude = profile['longitude']
        chart = Chart(Datetime(formatted_date, formatted_time, tz_offset), GeoPos(latitude, longitude), IDs=const.LIST_OBJECTS, hsys=const.HOUSES_PLACIDUS)
        self.chart_cache[name] = chart
        if len(self.chart_cache) > 50:
            del self.chart_cache[0]
        return chart

    @commands.group(pass_context=True, invoke_without_command=True)
    async def astrology(self, context):
        infomessage = 'Welcome to videm\'s Astrology Cog!\n'
        infomessage += 'This is an astrology cog in which you can create and store mutliple profiles on the bot to make (not draw) charts.\n\n'
        infomessage += 'To create a profile, use this command:\n'
        infomessage += '{prefix}astrology profile create [profile name] [birthyear] [birthmonth] [birthday] [birthhour] [birthminute] [location]\n'
        infomessage += 'You may use a city as a location.\n\n'
        infomessage += 'Use "{prefix}astrology commandlist" for more information!'
        infomessage = infomessage.format(prefix=context.prefix)
        em = discord.Embed(title='Videm\'s Astrology Cog', colour=0xFF3E28)
        em.set_thumbnail(url='https://www.syracusenewtimes.com/wp-content/uploads/2015/12/astrology.jpg')
        em.add_field(name='Info:', value=infomessage)
        await self.bot.say(embed=em)

    @astrology.command(pass_context=True)
    async def commandlist(self, context):
        commandmessage = '**"{prefix}astrology profile [profile name]"** to view the properties of a profile.\n'
        commandmessage += '**"{prefix}astrology profile list"** to view a list of your profiles.\n'
        commandmessage += '**"{prefix}astrology profile planets [profile name]"** to view the planet/asteroid signs of the profile.\n'
        commandmessage += '**"{prefix}astrology profile houses [profile name]"** to view the house signs of the profile.\n'
        commandmessage += '**"{prefix}astrology profile remove [profile name]"** to remove a profile.\n'
        commandmessage += '**"{prefix}astrology profile edit [profile name] [property name] [new value]"** to edit the property of a profile.\n'
        commandmessage += '**"{prefix}astrology get sign [profile name] [planet]"** to get a specific planet sign.\n'
        commandmessage += '**"{prefix}astrology get house [profile name] [house number]"** to get a specific house sign.\n'
        commandmessage = commandmessage.format(prefix=context.prefix)
        em = discord.Embed(title='Astrology Cog Command List', colour=0xFF3E28)
        em.set_thumbnail(url='https://www.syracusenewtimes.com/wp-content/uploads/2015/12/astrology.jpg')
        em.add_field(name='Commands:', value=commandmessage)
        await self.bot.say(embed=em)

    @astrology.command(pass_context=True)
    async def reset_all(self, context):
        if self.bot.is_owner(context.message.author.id): 
            self.profiles = []
            dataIO.save_json(self,profile_path, self.profiles)
            await self.bot.say('Successfully resetted all profiles!')

    @astrology.command(pass_context=True)
    async def define(self, context, *, word: str):
        word = word.replace(' ', '-')
        url = 'http://www.astrologyweekly.com/dictionary/{}.php'.format(word)
        async with aiohttp.get(url) as response:
            soupObject = BeautifulSoup(await response.text(), 'html.parser')
        try:
            definition = soupObject.find(class_='blog-post').findAll('fieldset')[0].get_text()
            await self.bot.say(definition)
        except:
            await self.bot.say('Either that definition doesn\'t exist, or something went wrong.')

    @astrology.group(pass_context=True, invoke_without_command=True)
    async def profile(self, context, name: str, member: discord.Member=None):
        if not await self.profile_exists(context, name, member):
            return
        if member:
            authorid = member.id
        else:
            authorid = context.message.author.id
        profile = self.profiles[authorid][name]
        em = discord.Embed(title='{}\'s Birth Profile'.format(name), colour=0x2F93E0)
        for propname, prop in profile.items():
            if propname != 'creator': 
                if isinstance(prop, str):
                    if not prop:
                        prop = 'N/A'
                    else:
                        prop = prop.lower().title()
                em.add_field(name=propname.title(), value=prop)
        await self.bot.say(embed=em)

    @profile.command(pass_context=True)
    async def create(self, context, name: str, birth_year: int, birth_month, birth_day: int, birth_hour: int, birth_minute: int, *, location: str):
        authorid = context.message.author.id
        if authorid not in self.profiles:
            self.profiles[authorid] = {}
        if name.lower() in [x.lower() for x in self.profiles[authorid]]:
            await self.bot.say('That person is already exists!')
            return
        if birth_month.isdecimal():
            birth_month = int(birth_month)
        self.profiles[authorid][name] = {
            'creator': context.message.author.id,
            'name': name,
            'year': birth_year,
            'month': birth_month,
            'day': birth_day,
            'hour': birth_hour,
            'minute': birth_minute,
            'location': location,
            'latitude': '',
            'longitude': ''
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

    @profile.command(pass_context=True)
    async def edit(self, context, name: str, property: str, new_value: str=None):
        await self.change_prop(context, name, property, new_value)

    @profile.command(pass_context=True)
    async def list(self, context, member: discord.Member=None):
        if member:
            authorid = member.id
        else:
            authorid = context.message.author.id
        if not authorid in self.profiles:
            await self.bot.say('You don\'t have any profiles! Do "{}astrology profile create" to create a profile!'.format(context.prefix))
            return
        em = discord.Embed(title='Profiles of {}'.format(str(context.message.author)), colour=0x2F93E0)
        for name, profile in self.profiles[authorid].items():
            month = profile['month']
            if isinstance(month, int):
                month = list(calendar.month_name)[month]
            em.add_field(name=name, value='{} {}, {} {}:{}'.format(month, str(profile['day']), str(profile['year']), str(profile['hour']), str(profile['minute'])))
        await self.bot.say(embed=em)

    @profile.command(pass_context=True)
    async def planets(self, context, name: str, member: discord.Member=None):
        chart = await self.get_chart(context, name, member)
        if not chart:
            return
        em = discord.Embed(title='Signs of {}'.format(name), colour=0x2F93E0)
        for obj in const.LIST_OBJECTS:
            sign = chart.get(obj).sign
            angles = angle.toString(chart.get(obj).signlon).split(':')
            em.add_field(name=obj, value='{} {} {}\' {}"'.format(angles[0][1:], sign, angles[1], angles[2]))
        await self.bot.say(embed=em)

    @profile.command(pass_context=True)
    async def houses(self, context, name: str, member: discord.Member=None):
        chart = await self.get_chart(context, name, member)
        if not chart:
            return
        em = discord.Embed(title='Houses of {}'.format(name), colour=0x2F93E0)
        for obj in const.LIST_HOUSES:
            sign = chart.get(obj).sign
            em.add_field(name=house_nums[int(obj[5:])], value=sign)
        await self.bot.say(embed=em)

    @astrology.group(pass_context=True)
    async def get(self, context):
        return

    @get.command(pass_context=True)
    async def sign(self, context, name: str, object: str, member: discord.Member=None):
        chart = await self.get_chart(context, name, member)
        if not chart:
            return
        object = next(x for x in const.LIST_OBJECTS if x.lower() == object.lower())
        try:
            sign = chart.get(object).sign
            angles = angle.toString(chart.get(object).signlon).split(':')
            await self.bot.say('{}\'s sign in {} is {} {} {}\' {}"'.format(name, object, angles[0][1:], sign, angles[1], angles[2]))
        except:
            await self.bot.say('That\'s not a valid astrological object!')

    @get.command(pass_context=True)
    async def house(self, context, name: str, house_num: int, member: discord.Member=None):
        chart = await self.get_chart(context, name, member)
        if not chart:
            return
        house = next(x for x in const.LIST_HOUSES if x.lower() == 'house' + str(house_num))
        try:
            sign = chart.get(house).sign
            await self.bot.say('{}\'s sign in House {} is {}.'.format(name, house_num, sign))
        except AttributeError:
            await self.bot.say('That\'s not a valid house!')

def check_folders():
    if not os.path.exists('data/astrology'):
        os.makedirs('data/astrology')

def check_files():
    f = 'data/astrology/profiles.json'
    if not dataIO.is_valid_json(f):
        dataIO.save_json(f, {})

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(astrology(bot))