import random
import discord
from discord.ext import commands

class test:
	def __init__(self, bot):
		self.bot = bot
		self.base = 'data/test/images/'
		
	pearlimages = ["{}pearl1.png", "{}pearl2.png", "{}pearl3.png"]
	
	@commands.command(pass_context=True)
	async def pearl(self, context):
		await self.bot.send_file(context.message.channel, random.choice(pearlimages).format(self.base))

def setup(bot):
	n = test(bot)
	bot.add_cog(n)
