import urllib.request
import xmltodict
from discord.ext import commands
import asyncio
import requests
import shutil

class color:
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(pass_context=True)
	async def hexcolor(self, context, colr):
		colr.replace('#', '')
		hdr = {'Accept': 'text/html,application/xhtml+xml,*/*',"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"}
		file = urllib.request.urlopen('http://www.colourlovers.com/api/color/' + colr, header = hdr)
		data = file.read()
		file.close()
		data = xmltodict.parse(data)
		table = render_to_response('my_template.html', {'data': data})
		img = table['colors']['color']['imageUrl']
		await self.bot.say(img)

def setup(bot):
	n = color(bot)
	bot.add_cog(n)
