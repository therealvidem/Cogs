import discord
import urllib.request, json
from discord.ext import commands
import asyncio
import datetime
import random

months_and_seasons = [
    'Winter',
    'December',
    'January',
    'February',
    'Spring',
    'March',
    'April',
    'May',
    'Summer',
    'June',
    'July',
    'August',
    'Autumn',
    'September',
    'October',
    'November'
]

def in_server(id):
    def predicate(ctx):
        return ctx.message.server.id == id
    return commands.check(predicate)
    
def lower_first_letter(s):
    return s[0].lower() + s[1:]

class everfell:
    def __init__(self, bot):
        self.bot = bot
        self.prompt_url = 'https://ineedaprompt.com/dictionary/default/prompt?q=adverb+verb+adjective+adjective+location'
		
    @commands.command(pass_context=True)
    @in_server('370045272887132162')
    async def everfellprompt(self, ctx):
        with urllib.request.urlopen(self.prompt_url) as url:
            data = json.loads(url.read().decode())
            choice1 = random.choice(months_and_seasons)
            index = months_and_seasons.index(choice1)
            choice2 = random.choice(months_and_seasons[:index] + months_and_seasons[index + 1:])
            await self.bot.say('{} and {} {}'.format(choice1, choice2, lower_first_letter(data['english'])))
			
def setup(bot):
    n = everfell(bot)
    bot.add_cog(n)
