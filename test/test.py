import random
import discord
from discord.ext import commands

class test:
	def __init__(self, bot):
		self.bot = bot
		self.base = 'data/test/images/'
	
	@commands.command(pass_context=True)
	async def pearl(self, context):
		n = random.randint(1,133)
		s = '{}meme_(' + str(n) + ').png'
		s2 = '{}meme_(' + str(n) + ').PNG'
		try:
			await self.bot.send_file(context.message.channel, s.format(self.base))
		except:
			await self.bot.send_file(context.message.channel, s2.format(self.base))

def setup(bot):
	n = test(bot)
	bot.add_cog(n)
