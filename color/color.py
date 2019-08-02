from redbot.core import commands
import asyncio
import random

class Color(commands.Cog):
	def __init__(self):
		pass
	
	@commands.command(name='hexcolor')
	async def hexcolor(self, context, colr):
		colr = colr.lower().replace('#', '')
		await context.send('http://www.colorhexa.com/' + colr + '.png')
		
	@commands.command(name='rgbcolor')
	async def rgbcolor(self, context, r, g, b):
		colr = '%02x%02x%02x' % (int(r), int(g), int(b))
		await context.send('http://www.colorhexa.com/' + colr + '.png')
		
	@commands.command(name='randomcolor')
	async def randomcolor(self, context):
		r = random.randint(0, 255)
		g = random.randint(0, 255)
		b = random.randint(0, 255)
		colr = '%02x%02x%02x' % (int(r), int(g), int(b))
		await context.send('http://www.colorhexa.com/' + colr + '.png')