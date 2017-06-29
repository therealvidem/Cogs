import random
import discord
import datetime
from discord.ext import commands
from .utils import checks
import asyncio
import time
import math
import operator
import urllib.request
import simplejson
from io import StringIO
from .utils.dataIO import dataIO
from __main__ import send_cmd_help, user_allowed
import os, os.path
import threading
from threading import Timer
import requests
import shutil
import re
from .utils.dataIO import dataIO

class test:
    memetypes = [
        "p"
        "m"
        "b"
    ]

    def __init__(self, bot):
        self.bot = bot
        self.base = 'data/test/images/'
        self.base2 = 'data/test/imagesj/'
        self.base3 = 'data/test/imagesm/'
        self.stabbingobjects = dataIO.load_json('data/test/stabbingobjects.json')
        self.memes = dataIO.load_json('data/test/memes.json')
        self.quotes = dataIO.load_json('data/test/quotes.json')
        self.counting = False

    # @commands.group()
    # async def emote(self, context, memetype, num):
    #     if memetype and memetype in memetypes:
    #         memenum = random.randint(1, self.memes[memetype])
    #         if ()
    #     elif memetype and memetype not in memetypes:
    #         await self.bot.say('{} isn\'t a meme type I recognize from my stash!'.format(memetype))

    @commands.group(pass_context=True)
    async def quote(self, context):
        return

    @quote.command(pass_context=True)
    async def add(self, context, author: discord.Member, quote):
        if quote not in self.quotes[str(author)]:
            self.quotes[str(author)] = quote
            dataIO.save_json('data/test/quotes.json', self.quotes)
            await self.bot.delete_message(context.message)
            await self.bot.say('"' + quote + '"\n -' + author.name + '\n' + datetime.now().year)

    @quote.command(pass_context=True)
    async def remove(self, context, author: discord.Member, quotenum):
        if quotenum < len(self.quotes[str(author)]):
            self.quotes[str(author)].remove(self.quotes[str(author)][quotenum])

    @quote.command(pass_context=True)
    async def list(self, context, author: discord.Member):
        if str(author) in self.quotes:
            # objs = ''
            # for obj in self.stabbingobjects['objects']:
            #     objs += '**{}**\n'.format(obj)
            # em = discord.Embed(title='My Knife Collection', color=discord.Color.green())
            # em.add_field(name='\a', value=objs)
            em = discord.Embed(title='Quotes from ' + author.name, colour=0x2F93E0)
            for x in range(len(self.quotes[str(author)])):
                em.add_field(name=x, value=self.quotes[str(author)][x])
            await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def emote(self, context, memetype):
        await self.bot.say(memetype + ' has ' + str(self.memes[memetype]) + ' emotes.')

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3)
    async def pearl(self, context, num: str = None):
        memenum = random.randint(1, self.memes['vp'])
        try:
            await self.bot.send_file(context.message.channel, self.base + 'meme (' + str(num) + ').png')
        except:
            await self.bot.send_file(context.message.channel, self.base + 'meme (' + str(memenum) + ').png')

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3)
    async def bar(self, context, num: str = None):
        if discord.utils.get(context.message.server.roles, name='BAR'):
            memenum = random.randint(1, self.memes['vb'])
            try:
                await self.bot.send_file(context.message.channel, self.base2 + 'meme (' + str(num) + ').png')
            except:
                await self.bot.send_file(context.message.channel, self.base2 + 'meme (' + str(memenum) + ').png')

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3)
    async def meme(self, context, num: str = None):
        if discord.utils.get(context.message.server.roles, name='BAR'):
            memenum = random.randint(1, self.memes['vm'])
            try:
                await self.bot.send_file(context.message.channel, self.base3 + 'meme (' + str(num) + ').png')
            except:
                await self.bot.send_file(context.message.channel, self.base3 + 'meme (' + str(memenum) + ').png')

    @commands.command(pass_context=True)
    async def addvp(self, context, url):
        if discord.utils.get(context.message.server.roles, name='BAR'):
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                count = self.memes['vp'] + 1
                with open(self.base + 'meme (' + str(count) + ').png', 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                self.memes['vp'] = count
                dataIO.save_json('data/test/memes.json', self.memes)
                await self.bot.say('Successfully added emote as vp ' + str(count))
            else:
                await self.bot.say('Unable to add emote.')

    @commands.command(pass_context=True)
    async def addvb(self, context, url):
        if discord.utils.get(context.message.server.roles, name='BAR'):
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                count = self.memes['vb'] + 1
                with open(self.base2 + 'meme (' + str(count) + ').png', 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                self.memes['vb'] = count
                dataIO.save_json('data/test/memes.json', self.memes)
                await self.bot.say('Successfully added emote as vb ' + str(count))
            else:
                await self.bot.say('Unable to add emote.')

    @commands.command(pass_context=True)
    async def addvm(self, context, url):
        if discord.utils.get(context.message.server.roles, name='BAR'):
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                count = self.memes['vm'] + 1
                with open(self.base3 + 'meme (' + str(count) + ').png', 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                self.memes['vm'] = count
                dataIO.save_json('data/test/memes.json', self.memes)
                await self.bot.say('Successfully added emote as vm ' + str(count))
            else:
                await self.bot.say('Unable to add emote.')

    @commands.command(pass_context=True)
    async def rollbetween(self, context, one, two):
        choice = random.randint(int(one), int(two))
        await self.bot.say('You got a ' + str(choice) + '.')

    @commands.command(pass_context=True)
    async def factorial(self, context, n: int = None):
        if n is None:
            await self.bot.say('wat')
        elif n > 0:
            await self.bot.say(str(n) + '! = ' + str(rFactorial(n)))
        elif n < 0:
            await self.bot.say("Are you trying to find the factorial of a negative number? You're batshit crazy, lad!")

    @commands.command(pass_context=True)
    async def permutations(self, context, n: int = None, r: int = None):
        if n is None or r is None:
            await self.bot.say('wat')
        elif n > 0 and r > 0:
            await self.bot.say(str(n) + 'P' + str(r) + ' = ' + str(rFactorial(n) / rFactorial(n - r)))
        elif n < 0 or r < 0:
            await self.bot.say('I dunno what the means.')

    @commands.command(pass_context=True)
    async def combinations(self, context, n: int = None, r: int = None):
        if n is None or r is None:
            await self.bot.say('wat')
        elif n > 0 and r > 0 and n >= r:
            await self.bot.say(str(n) + 'C' + str(r) + ' = ' + str(rFactorial(n) / (rFactorial(n - r) * rFactorial(r))))
        elif n < 0 or r < 0:
            await self.bot.say('I dunno what the means.')

    @commands.command(pass_context=True)
    async def invite(self, context, botid: str = None, server: str = None):
        if botid:
            await self.bot.say(discord.utils.oauth_url(botid, permissions=None, server=server, redirect_uri=None))

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5)
    async def sauce(self, context):
        await self.bot.say(
            '***H̭̓͗̏̅͘E̳̰̠͖͓͕͊͋ͯͭ̿̔Ÿ͓̜͎̪͉́͆ͮ̇́̆̊̒̈͝ ̷̧̖̌ͮ̉̂̿ͪ͗̔V̶̯̩̤̥ͧ͊̋͊ͧ͞S̴̷̳͈̓͗̽̏̇A̶͎͈̔̍ͨ̉̚͞U̼̻͍̬̪̦ͦ͌ͩ̑͋͊̈́ͅC̺̻̪̯̗̖̖͂ͪ̈́̕Ȩ̮̤̫̯̟ͭ͌̅̒̄͘͠ͅ,̗͖̯͙͖̮̪̏́ ̶̨̫̮͎̗̣͋̍̓͟M̐͂͞͏̘̥͎̕I̴̭͉̰͎͈͎͔̗̭ͥ͒͗̊́͘C̷̗̬͙͎̠͇͊̔ͦ̆͠H̡̋͐͗́̚͝҉̫̣̳̦̥̮̗̜ͅĂ͓̹͙̽ͨ̑̋̈́̚͘͠E̢̺̘̳̬͙̅ͪͮ͒͑̒͒̇͂͞L͔̣̟̗͉̹̾͊̈́͋ͭ̑ͥ̕ ͬͯ҉̡̨͓̝̗̺H̰͕͌ͨĘ̳̟͕̹̘̠͇͎́̄͑̀ͅR͈̳ͬ̉Eͣ͞҉̳̘̦͉̞̣***')

    @commands.command(pass_context=True)
    @commands.cooldown(5, 3)
    async def stab(self, context, *, member: discord.Member = None):
        obj = random.choice(self.stabbingobjects['objects'])
        word = random.choice(
            ["shanks", "stabs", "shoves", "impales", "injects", "thrusts", "knifes", "punctures", "jabs", "lunges at",
             "prods"])
        await self.bot.say('{0} {1} {2} with {3}.'.format(context.message.author.name, word, member.mention, obj))

    @commands.command(pass_context=True)
    async def pat(self, context, member: discord.Member = None, n: int = 3):
        member = member or context.message.author
        if n and n <= 650 and n > 0:
            if member.id != self.bot.user.id:
                await self.bot.say(member.mention + ' *' + ('pat' * n) + '*')
            else:
                await self.bot.say('*eternally pats self*')
        else:
            if n > 650:
                await self.bot.say('That\'s too many pats!')
            elif n == -1:
                await self.bot.say(member.mention + ' *' + ('pat' * 650) + '*')
            elif n < -1:
                await self.bot.say('I don\'t know how to pat you that many times.')
            else:
                await self.bot.say('wat')

    @commands.command(pass_context=True)
    async def aaa(self, context, n: int = 10):
        if n and n <= 1987 and n > 0:
            await self.bot.say('***' + ('A' * n) + '***')
        else:
            if n > 1987:
                await self.bot.say('That\'s too loud, calm down!')
            elif n == -1:
                await self.bot.say('***' + ('A' * 1987) + '***')
            elif n < -1:
                await self.bot.say('Are you silent?')
            else:
                await self.bot.say('wat')

    @commands.command(pass_context=True)
    async def ha(self, context, n: int = 10):
        if n and n <= 995 and n > 0:
            await self.bot.say('***' + ('HA' * n) + '***')
        else:
            if n > 995:
                await self.bot.say('That\'s too loud, calm down!')
            elif n == -1:
                await self.bot.say('***' + ('HA' * 995) + '***')
            elif n < -1:
                await self.bot.say('Are you silent?')
            else:
                await self.bot.say('wat')

    @commands.command(pass_context=True)
    async def triggered(self, context, n: int = 1):
        if n and n <= 31 and n > 0:
            await self.bot.say('***' + ('T̰͈ͪ̒̿R̼̘̔̆͜I̗̯̾ͨͣ͘G̾ͫ̍̾̂̊͛G͌̔ͤ҉̺͕̼E̐ͨ̉̾ͤͥͦR̼̘̎̂̐ͩ̏Ȩ̠̣͐̏̇̐D̤̟̦ͧ' * n) + '***')
        else:
            if n > 31:
                await self.bot.say('You\'re triggered too much! Calm down!')
            elif n == -1:
                await self.bot.say(
                    '***' + ('T̰͈ͪ̒̿R̼̘̔̆͜I̗̯̾ͨͣ͘G̾ͫ̍̾̂̊͛G͌̔ͤ҉̺͕̼E̐ͨ̉̾ͤͥͦR̼̘̎̂̐ͩ̏Ȩ̠̣͐̏̇̐D̤̟̦ͧ' * 31) + '***')
            elif n < -1:
                await self.bot.say('Are you actually triggered tho?')
            else:
                await self.bot.say('wat')

    @commands.command(pass_context=True)
    async def ooo(self, context, n: int = 10):
        if n and n <= 1987 and n > 0:
            await self.bot.say('***' + ('O' * n) + '***')
        else:
            if n > 1987:
                await self.bot.say('That\'s too loud, calm down!')
            elif n == -1:
                await self.bot.say('***' + ('O' * 1987) + '***')
            elif n < -1:
                await self.bot.say('Are you silent?')
            else:
                await self.bot.say('wat')

    @commands.command(pass_context=True)
    async def happy(self, context, n: int = 10):
        happyemote = ':smile:'
        if n and n > 0 and n * len(happyemote) < 2000:
            await self.bot.say(':smile:' * n)
        else:
            if n > 2000 - len(happyemote):
                await self.bot.say('You\'re a bit too happy there, bud.')
            elif n == -1:
                await self.bot.say(':smile:' * 280)
            elif n < -1:
                await self.bot.say('Are you silent?')
            else:
                await self.bot.say('wat')

    @commands.command(pass_context=True)
    async def ophiuchus(self, context, n: int = 10):
        emote = ':ophiuchus:'
        if n and n > 0 and n * len(emote) < 2000:
            await self.bot.say(emote * n)
        else:
            if n > 2000 - len(emote):
                await self.bot.say('You\'re a bit too happy there, bud.')
            elif n == -1:
                await self.bot.say(emote * math.floor(2000 / len(emote)))
            elif n < -1:
                await self.bot.say('Are you silent?')
            else:
                await self.bot.say('wat')

    @commands.command(pass_context=True)
    async def ae(self, context, n: int = 10):
        chance = random.randint(1, 2)
        begintext = 'VA'
        if chance == 1:
            endtext = ' LMAO'
        else:
            endtext = 'YEET'
        if n and n > 0 and len(begintext) + n + len(endtext) < 1990:
            await self.bot.say('***' + (begintext + ('E' * n) + endtext) + '***')
        else:
            if n > 1990:
                await self.bot.say('wew that\'s a lot of vae')
            elif n == -1:
                await self.bot.say(
                    '***' + (begintext + ('E' * int((1990 - (len(begintext) + len(endtext))))) + endtext) + '***')
            elif n < -1:
                await self.bot.say('Are you silent?')
            else:
                await self.bot.say('wat')

    @commands.command(pass_context=True)
    async def mmm(self, context, n: int = 10):
        text = 'M'
        if n and n > 0 and (n * len(text)) + 6 < 2000:
            await self.bot.say('***' + (text * n) + '***')
        else:
            if n >= n * len(text):
                await self.bot.say('This is a PG-13 channel.')
            elif n == -1:
                await self.bot.say(text * int(1990 / len(text)))
            elif n < -1:
                await self.bot.say('Are you silent?')
            else:
                await self.bot.say('wat')

    @commands.group()
    async def repeattext(self, context):
        return

    @repeattext.command(pass_context=True)
    async def regular(self, context, text, n: int = 10):
        if n > 0 and (n * len(text)) < 2000:
            await self.bot.say(text * n)
        else:
            if n == -1:
                await self.bot.say(text * math.floor(2000 / len(text)))
            elif n >= n * len(text):
                await self.bot.say('That\'s a bit excessive, don\'t ya think?')
            elif n < -1:
                await self.bot.say('LOUDER')
            else:
                await self.bot.say('wat')

    @repeattext.command(pass_context=True)
    async def bold(self, context, text, n: int = 10):
        if n > 0 and (n * len(text)) + 4 < 2000:
            await self.bot.say('**' + text * n + '**')
        else:
            if n == -1:
                await self.bot.say('**' + text * math.floor(2000 / len(text) - 4) + '**')
            elif n >= n * len(text):
                await self.bot.say('That\'s a bit excessive, don\'t ya think?')
            elif n < -1:
                await self.bot.say('LOUDER')
            else:
                await self.bot.say('wat')

    @repeattext.command(pass_context=True)
    async def italic(self, context, text, n: int = 10):
        if n > 0 and (n * len(text)) + 2 < 2000:
            await self.bot.say('*' + text * n + '*')
        else:
            if n == -1:
                await self.bot.say('*' + text * math.floor(2000 / len(text) - 2) + '*')
            elif n >= n * len(text):
                await self.bot.say('That\'s a bit excessive, don\'t ya think?')
            elif n < -1:
                await self.bot.say('LOUDER')
            else:
                await self.bot.say('wat')

    @repeattext.command(pass_context=True)
    async def boldanditalic(self, context, text, n: int = 10):
        if n > 0 and (n * len(text)) + 6 < 2000:
            await self.bot.say('***' + text * n + '***')
        else:
            if n == -1:
                await self.bot.say('***' + text * math.floor(2000 / len(text) - 6) + '***')
            elif n >= n * len(text):
                await self.bot.say('That\'s a bit excessive, don\'t ya think?')
            elif n < -1:
                await self.bot.say('LOUDER')
            else:
                await self.bot.say('wat')

    @commands.command(pass_context=True)
    async def addstab(self, context, *, obj: str = None):
        if obj and obj not in self.stabbingobjects['objects']:
            obj = obj.rstrip(".");
            allowed = True
            listofpeople = []
            for person in context.message.server.members:
                if obj == person.mention:
                    allowed = False
                    break
            if allowed:
                self.stabbingobjects['objects'].append(obj)
                dataIO.save_json('data/test/stabbingobjects.json', self.stabbingobjects)
                await self.bot.say('Successfully added ' + obj + ' as a stabby stabby object.')
            else:
                await self.bot.say('I can\'t add mentions.')
        else:
            if obj in self.stabbingobjects['objects']:
                await self.bot.say('That\'s already in my knife collection.')
            else:
                await self.bot.say('wat')

    @commands.command(pass_context=True)
    async def removestab(self, context, *, obj: str = None):
        if obj and obj in self.stabbingobjects['objects']:
            self.stabbingobjects['objects'].remove(obj)
            dataIO.save_json('data/test/stabbingobjects.json', self.stabbingobjects)
            await self.bot.say('Successfully removed ' + obj + ' from my knife collection.')
        else:
            await self.bot.say('wat')

    @commands.command(pass_context=True)
    async def liststab(self, context):
        objs = ''
        for obj in self.stabbingobjects['objects']:
            objs += '**{}**\n'.format(obj)
        em = discord.Embed(title='My Knife Collection', color=discord.Color.green())
        em.add_field(name='\a', value=objs)
        # em = discord.Embed(title='My Knife Collection', colour=0x2F93E0)
        # for x in range(0, len(self.stabbingobjects['objects'])):
        #	em.add_field(name=x + 1, value=self.stabbingobjects['objects'][x])
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def eh(self, context, member: discord.Member = None):
        member = member or context.message.author
        await self.bot.say(member.mention + ', eh?')

    @commands.group()
    async def count(self, context):
        if context.invoked_subcommand is None:
            prefix = context.prefix
            await self.bot.say(
                'Do \'{0}count start <start number> [end number] [mention]\' (end number and mention being optional, defaulting to 0 and false, respectively) to start or \'{0}count stop\' to stop any counting operation.'.format(
                    prefix))

    @count.command(pass_context=True)
    async def start(self, context, startnum: int = None, endnum: int = 0, mention: str = 'false'):
        if self.counting == False:
            if startnum:
                chance = random.randint(1, 10)
                if (startnum >= 0 and endnum < startnum):
                    self.counting = True
                    for x in range(int(startnum), endnum - 1, -1):
                        if (self.counting == True):
                            await self.bot.say(str(x) + ',')
                            await asyncio.sleep(1)
                        else:
                            break
                    if (chance == 10):
                        if (str(mention) == 'true'):
                            await self.bot.say(
                                'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcS4fQx4f2n6H0U1H8YuGbcCKFBIWAC0eCwn31Z2fbSqKyH8SB7ke_szKA ' + context.message.author.mention)
                        else:
                            await self.bot.say(
                                'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcS4fQx4f2n6H0U1H8YuGbcCKFBIWAC0eCwn31Z2fbSqKyH8SB7ke_szKA')
                    else:
                        if (str(mention) == 'true'):
                            await self.bot.say('TIME! ' + context.message.author.mention)
                        else:
                            await self.bot.say('TIME!')
                    self.counting = False
                elif (startnum >= 0 and endnum > startnum):
                    self.counting = True
                    for x in range(int(startnum), endnum + 1):
                        if (self.counting == True):
                            await self.bot.say(str(x) + ',')
                            await asyncio.sleep(1)
                        else:
                            break
                    if (chance == 10):
                        if (str(mention) == 'true'):
                            await self.bot.say(
                                'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcS4fQx4f2n6H0U1H8YuGbcCKFBIWAC0eCwn31Z2fbSqKyH8SB7ke_szKA ' + context.message.author.mention)
                        else:
                            await self.bot.say(
                                'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcS4fQx4f2n6H0U1H8YuGbcCKFBIWAC0eCwn31Z2fbSqKyH8SB7ke_szKA')
                    else:
                        if (str(mention) == 'true'):
                            await self.bot.say('TIME! ' + context.message.author.mention)
                        else:
                            await self.bot.say('TIME!')
                    self.counting = False
                else:
                    await self.bot.say('An error occured.')
            else:
                await self.bot.say('An error occured.')
        else:
            await self.bot.say('I\'m already counting.')

    @count.command(pass_context=True)
    async def stop(self, context):
        self.counting = False


def rFactorial(n):
    if (n == 0):
        return 1
    else:
        return n * (rFactorial(n - 1))


def setup(bot):
    n = test(bot)
    bot.add_cog(n)
