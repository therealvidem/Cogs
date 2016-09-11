import random
import discord
from discord.ext import commands

class test:
	def __init__(self, bot):
		self.bot = bot
		self.base = 'data/test/images/'
	
	@commands.command(pass_context=True)
	async def pearl(self, context):
		await self.bot.send_file(context.message.channel, "meme_" + str(random.randint(1,133).format(self.base))

def setup(bot):
	n = test(bot)
	bot.add_cog(n)
