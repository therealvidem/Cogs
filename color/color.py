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
		rand = random.randint(1, 3)
		if rand == 1:
			colr = 'F*0000'
		elif rand == 2:
			colr = '00F*00'
		else:
			colr = '0000F*'
		for x in range(0, 4):
			colr.replace('0', random.randint(0,10), 1)
		colr.replace('*', random.choice(self.hexalphabet))
		await self.bot.say('http://www.colorhexa.com/' + colr + '.png')

def setup(bot):
	n = color(bot)
	bot.add_cog(n)
