import urllib.request
import xmltodict
from discord.ext import commands
import asyncio
import requests
import shutil
from colourlovers import ColourLovers

class color:
	def __init__(self, bot):
		self.bot = bot
		self.cl = ColourLovers()
	
	@commands.command(pass_context=True)
	async def hexcolor(self, context, colr):
		colour = self.cl.color(colr)
		await self.bot.say(colour.image_url)

def setup(bot):
	n = color(bot)
	bot.add_cog(n)
