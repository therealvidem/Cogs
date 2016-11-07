from discord.ext import commands
import asyncio

class color:
	def __init__(self, bot):
		self.bot = bot
		self.hexalphabet = {'A', 'B', 'C', 'D', 'E', 'F'}
	
	@commands.command(pass_context=True)
	async def hexcolor(self, context, colr):
		colr = colr.lower().replace('#', '')
		await self.bot.say('http://www.colorhexa.com/' + colr + '.png')
		
	@commands.command(pass_context=True)
	async def rgbcolor(self, context, r, g, b):
		colr = '%02x%02x%02x' % (int(r), int(g), int(b))
		await self.bot.say('http://www.colorhexa.com/' + colr + '.png')
		
	@commands.command()
	async def randomcolor(self, context):
		colr = rgbcol(random.randint(1, 3))
		for x in range(0, 4):
			colr.replace('0', random.randint(0,10), 1)
		colr.replace('*', hexalphabet[random.randint(0, 5)])
		await self.bot.say('http://www.colorhexa.com/' + colr + '.png')

def rgbcol(x):
	return {
		'1': 'F*0000',
		'2': '00F*00',
		'3': '0000F*'
	}[x]

def setup(bot):
	n = color(bot)
	bot.add_cog(n)
