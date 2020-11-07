from redbot.core import commands
from redbot.core import Config
from .customconverters import BetterMemberConverter
import random
import discord
import math
import names

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=22945132051920)
        default_global = {
            'stabbing_objects': []
        }
        self.config.register_global(**default_global)
        self.stabbing_verbs = [
            "shanks", 
            "stabs", 
            "shoves", 
            "impales", 
            "injects", 
            "thrusts",
            "knifes",
            "punctures", 
            "jabs", 
            "lunges at",
            "prods"
        ]
        self.stabbing_objects_value = self.config.stabbing_objects
        self.counting = False

    # @commands.group()
    # async def emote(self, ctx, memetype, num):
    #     if memetype and memetype in memetypes:
    #         memenum = random.randint(1, self.memes[memetype])
    #         if ()
    #     elif memetype and memetype not in memetypes:
    #         await ctx.send('{} isn\'t a meme type I recognize from my stash!'.format(memetype))

    @commands.command()
    async def spongebob(self, ctx, *, msg: str):
        capitalize = True if msg[0].isupper() else False
        newmsg = []
        for char in msg:
            if capitalize:
                newmsg.append(char.upper())
            else:
                newmsg.append(char.lower())
            if char != ' ':
                capitalize = not capitalize
        await ctx.send(''.join(newmsg))

    @commands.command(autohelp=False)
    @commands.cooldown(3, 5)
    async def randomname(self, ctx, num: int=1, gender: str=None):
        if gender is not None and gender != 'female':
            gender = 'male'
        if num > 10:
            await ctx.send('You may only print ten names at a time!')
            return
        msg = names.get_full_name(gender=gender)
        for _ in range(1, num):
            msg += ', ' + names.get_full_name()
        await ctx.send(msg)

    @commands.command()
    async def rollbetween(self, ctx, one: int, two: int):
        choice = random.randint(one, two)
        await ctx.send('You got a {}!'.format(choice))

    @commands.command()
    @commands.cooldown(1, 5)
    async def sauce(self, ctx):
        await ctx.send('***H̭̓͗̏̅͘E̳̰̠͖͓͕͊͋ͯͭ̿̔Ÿ͓̜͎̪͉́͆ͮ̇́̆̊̒̈͝ ̷̧̖̌ͮ̉̂̿ͪ͗̔V̶̯̩̤̥ͧ͊̋͊ͧ͞S̴̷̳͈̓͗̽̏̇A̶͎͈̔̍ͨ̉̚͞U̼̻͍̬̪̦ͦ͌ͩ̑͋͊̈́ͅC̺̻̪̯̗̖̖͂ͪ̈́̕Ȩ̮̤̫̯̟ͭ͌̅̒̄͘͠ͅ,̗͖̯͙͖̮̪̏́ ̶̨̫̮͎̗̣͋̍̓͟M̐͂͞͏̘̥͎̕I̴̭͉̰͎͈͎͔̗̭ͥ͒͗̊́͘C̷̗̬͙͎̠͇͊̔ͦ̆͠H̡̋͐͗́̚͝҉̫̣̳̦̥̮̗̜ͅĂ͓̹͙̽ͨ̑̋̈́̚͘͠E̢̺̘̳̬͙̅ͪͮ͒͑̒͒̇͂͞L͔̣̟̗͉̹̾͊̈́͋ͭ̑ͥ̕ ͬͯ҉̡̨͓̝̗̺H̰͕͌ͨĘ̳̟͕̹̘̠͇͎́̄͑̀ͅR͈̳ͬ̉Eͣ͞҉̳̘̦͉̞̣***')

    @commands.command()
    @commands.cooldown(5, 3)
    async def stab(self, ctx, *, member: str):
        member = await BetterMemberConverter().convert(ctx, member)
        stabbing_objects = await self.stabbing_objects_value()
        if stabbing_objects:
            obj = random.choice(stabbing_objects)
            word = random.choice(self.stabbing_verbs)
            await ctx.send('{0} {1} {2} with {3}.'.format(ctx.message.author.name, word, member.mention, obj))
        else:
            await ctx.send('My knife collection is empty!')
    
    @commands.command()
    async def addstab(self, ctx, *, obj: str):
        async with self.stabbing_objects_value() as stabbing_objects:
            if obj not in stabbing_objects:
                obj = obj.rstrip()
                stabbing_objects.append(obj)
                await ctx.send('Successfully added {} as a stabby stabby object.'.format(obj))
            else:
                await ctx.send('That\'s already in my knife collection.')

    @commands.command()
    async def removestab(self, ctx, *, obj: str):
        async with self.stabbing_objects_value() as stabbing_objects:
            if obj in stabbing_objects:
                obj = obj.rstrip()
                stabbing_objects.remove(obj)
                await ctx.send('Successfully removed {} as a stabby stabby object.'.format(obj))
            else:
                await ctx.send('I can\'t find that in my knife collection.')

    @commands.command()
    async def liststab(self, ctx):
        objs = ''
        stabbing_objects = await self.stabbing_objects_value()
        for obj in stabbing_objects:
            objs += '**{}**\n'.format(obj)
        em = discord.Embed(
            title='My Knife Collection', 
            color=discord.Color.red(),
            description=objs
        )
        await ctx.send(embed=em)

    @commands.command()
    async def pat(self, ctx, member: str=None, n: int=3):
        member = await BetterMemberConverter().convert(ctx, member) if member else ctx.author
        if n and n <= 650 and n > 0:
            if member.id != self.bot.user.id:
                await ctx.send(member.mention + ' *' + ('pat' * n) + '*')
            else:
                await ctx.send('*eternally pats self*')
        else:
            if n > 650:
                await ctx.send('That\'s too many pats!')
            elif n == -1:
                await ctx.send(member.mention + ' *' + ('pat' * 650) + '*')
            elif n < -1:
                await ctx.send('I don\'t know how to pat you that many times.')
            else:
                await ctx.send('wat')

    @commands.command()
    async def aaa(self, ctx, n: int=10):
        if n and n <= 1987 and n > 0:
            await ctx.send('***' + ('A' * n) + '***')
        else:
            if n > 1987:
                await ctx.send('That\'s too loud, calm down!')
            elif n == -1:
                await ctx.send('***' + ('A' * 1987) + '***')
            elif n < -1:
                await ctx.send('Are you silent?')
            else:
                await ctx.send('wat')

    @commands.command()
    async def ha(self, ctx, n: int=10):
        if n and n <= 995 and n > 0:
            await ctx.send('***' + ('HA' * n) + '***')
        else:
            if n > 995:
                await ctx.send('That\'s too loud, calm down!')
            elif n == -1:
                await ctx.send('***' + ('HA' * 995) + '***')
            elif n < -1:
                await ctx.send('Are you silent?')
            else:
                await ctx.send('wat')

    @commands.command()
    async def triggered(self, ctx, n: int=1):
        if n and n <= 31 and n > 0:
            await ctx.send('***' + ('T̰͈ͪ̒̿R̼̘̔̆͜I̗̯̾ͨͣ͘G̾ͫ̍̾̂̊͛G͌̔ͤ҉̺͕̼E̐ͨ̉̾ͤͥͦR̼̘̎̂̐ͩ̏Ȩ̠̣͐̏̇̐D̤̟̦ͧ' * n) + '***')
        else:
            if n > 31:
                await ctx.send('You\'re triggered too much! Calm down!')
            elif n == -1:
                await ctx.send(
                    '***' + ('T̰͈ͪ̒̿R̼̘̔̆͜I̗̯̾ͨͣ͘G̾ͫ̍̾̂̊͛G͌̔ͤ҉̺͕̼E̐ͨ̉̾ͤͥͦR̼̘̎̂̐ͩ̏Ȩ̠̣͐̏̇̐D̤̟̦ͧ' * 31) + '***')
            elif n < -1:
                await ctx.send('Are you actually triggered tho?')
            else:
                await ctx.send('wat')

    @commands.command()
    async def ooo(self, ctx, n: int=10):
        if n and n <= 1987 and n > 0:
            await ctx.send('***' + ('O' * n) + '***')
        else:
            if n > 1987:
                await ctx.send('That\'s too loud, calm down!')
            elif n == -1:
                await ctx.send('***' + ('O' * 1987) + '***')
            elif n < -1:
                await ctx.send('Are you silent?')
            else:
                await ctx.send('wat')

    @commands.command()
    async def happy(self, ctx, n: int=10):
        happyemote = ':smile:'
        if n and n > 0 and n * len(happyemote) < 2000:
            await ctx.send(':smile:' * n)
        else:
            if n > 2000 - len(happyemote):
                await ctx.send('You\'re a bit too happy there, bud.')
            elif n == -1:
                await ctx.send(':smile:' * 280)
            elif n < -1:
                await ctx.send('Are you silent?')
            else:
                await ctx.send('wat')

    @commands.command()
    async def ophiuchus(self, ctx, n: int=10):
        emote = ':ophiuchus:'
        if n and n > 0 and n * len(emote) < 2000:
            await ctx.send(emote * n)
        else:
            if n > 2000 - len(emote):
                await ctx.send('You\'re a bit too happy there, bud.')
            elif n == -1:
                await ctx.send(emote * math.floor(2000 / len(emote)))
            elif n < -1:
                await ctx.send('Are you silent?')
            else:
                await ctx.send('wat')

    @commands.command()
    async def ae(self, ctx, n: int=10):
        chance = random.randint(1, 2)
        begintext = 'VA'
        if chance == 1:
            endtext = ' LMAO'
        else:
            endtext = 'YEET'
        if n and n > 0 and len(begintext) + n + len(endtext) < 1990:
            await ctx.send('***' + (begintext + ('E' * n) + endtext) + '***')
        else:
            if n > 1990:
                await ctx.send('wew that\'s a lot of vae')
            elif n == -1:
                await ctx.send(
                    '***' + (begintext + ('E' * int((1990 - (len(begintext) + len(endtext))))) + endtext) + '***')
            elif n < -1:
                await ctx.send('Are you silent?')
            else:
                await ctx.send('wat')

    @commands.command()
    async def mmm(self, ctx, n: int=10):
        text = 'M'
        if n and n > 0 and (n * len(text)) + 6 < 2000:
            await ctx.send('***' + (text * n) + '***')
        else:
            if n >= n * len(text):
                await ctx.send('This is a PG-13 channel.')
            elif n == -1:
                await ctx.send(text * int(1990 / len(text)))
            elif n < -1:
                await ctx.send('Are you silent?')
            else:
                await ctx.send('wat')

    @commands.group()
    async def repeattext(self, ctx):
        return

    @repeattext.command()
    async def regular(self, ctx, text, n: int=10):
        if n > 0 and (n * len(text)) < 2000:
            await ctx.send(text * n)
        else:
            if n == -1:
                await ctx.send(text * math.floor(2000 / len(text)))
            elif n >= n * len(text):
                await ctx.send('That\'s a bit excessive, don\'t ya think?')
            elif n < -1:
                await ctx.send('LOUDER')
            else:
                await ctx.send('wat')

    @repeattext.command()
    async def bold(self, ctx, text, n: int=10):
        if n > 0 and (n * len(text)) + 4 < 2000:
            await ctx.send('**' + text * n + '**')
        else:
            if n == -1:
                await ctx.send('**' + text * math.floor(2000 / len(text) - 4) + '**')
            elif n >= n * len(text):
                await ctx.send('That\'s a bit excessive, don\'t ya think?')
            elif n < -1:
                await ctx.send('LOUDER')
            else:
                await ctx.send('wat')

    @repeattext.command()
    async def italic(self, ctx, text, n: int=10):
        if n > 0 and (n * len(text)) + 2 < 2000:
            await ctx.send('*' + text * n + '*')
        else:
            if n == -1:
                await ctx.send('*' + text * math.floor(2000 / len(text) - 2) + '*')
            elif n >= n * len(text):
                await ctx.send('That\'s a bit excessive, don\'t ya think?')
            elif n < -1:
                await ctx.send('LOUDER')
            else:
                await ctx.send('wat')

    @repeattext.command()
    async def boldanditalic(self, ctx, text, n: int=10):
        if n > 0 and (n * len(text)) + 6 < 2000:
            await ctx.send('***' + text * n + '***')
        else:
            if n == -1:
                await ctx.send('***' + text * math.floor(2000 / len(text) - 6) + '***')
            elif n >= n * len(text):
                await ctx.send('That\'s a bit excessive, don\'t ya think?')
            elif n < -1:
                await ctx.send('LOUDER')
            else:
                await ctx.send('wat')
    
    @commands.command()
    async def scream(self, ctx, *, text):
        await ctx.send('***' + text * math.floor(2000 / len(text) - 6) + '***')