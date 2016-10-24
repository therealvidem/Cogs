import urllib.request
import xmltodict
from discord.ext import commands
import asyncio

class color:
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(pass_context=True)
	async def hexcolor(self, context, colr):
		colr.replace('#', '')
		file = urllib2.urlopen('http://www.colourlovers.com/api/color/' + colr)
		data = file.read()
		file.close()
		data = xmltodict.parse(data)
		table = render_to_response('my_template.html', {'data': data})
		img = table['colors']['color']['imageUrl']
		await self.bot.say(img)

def setup(bot):
	n = color(bot)
	bot.add_cog(n)
