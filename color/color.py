from discord.ext import commands
import asyncio
import random

class color:
	def __init__(self, bot):
		self.bot = bot
		self.hexalphabet = ['A', 'B', 'C', 'D', 'E', 'F']
	
	@commands.command(pass_context=True)
	async def hexcolor(self, context, colr):
		colr = colr.lower().replace('#', '')
		await self.bot.say('http://www.colorhexa.com/' + colr + '.png')
		
	@commands.command(pass_context=True)
	async def rgbcolor(self, context, r, g, b):
		colr = '%02x%02x%02x' % (int(r), int(g), int(b))
		await self.bot.say('http://www.colorhexa.com/' + colr + '.png')
		
	@commands.command(pass_context=True)
	async def randomcolor(self, context):
		r = random.randint(0, 255)
		g = random.randint(0, 255)
		b = random.randint(0, 255)
		colr = '%02x%02x%02x' % (int(r), int(g), int(b))
		await self.bot.say('http://www.colorhexa.com/' + colr + '.png')

def setup(bot):
	n = color(bot)
	bot.add_cog(n)
