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
