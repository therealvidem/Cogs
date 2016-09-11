from discord.ext import commands

class test:
	def __init__(self, bot):
		self.bot = bot
		self.base = 'data/downloader/videmcogs/test/data/images/'

	@commands.command(pass_context=True)
	async def pearl(self, context):
	   await self.bot.send_file(context.message.channel, '{}pearl.png'.format(self.base))

def setup(bot):
	n = test(bot)
	bot.add_cog(n)
