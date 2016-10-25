from discord.ext import commands
import asyncio

class color:
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(pass_context=True)
	async def hexcolor(self, context, colr):
		colr = colr.lower().replace('#', '')
		await self.bot.say('http://www.colorhexa.com/' + colr + '.png')

def setup(bot):
	n = color(bot)
	bot.add_cog(n)
