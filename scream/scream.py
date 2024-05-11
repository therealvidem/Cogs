import math
import random
from redbot.core import commands
from redbot.core.bot import Red

from scream.customconverters import BetterMemberConverter

class Scream(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
    
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
