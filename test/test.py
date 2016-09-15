import random
import discord
from discord.ext import commands
from .utils import checks
import asyncio

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
			
	@commands.command(pass_context=True)
	@checks.admin_or_permissions(move_members=True)
	async def movevidem(self, ctx, to_channel: discord.Channel):
		type_to = str(to_channel.type)
		if type_to == 'text':
			await self.bot.say('{} is not a valid voice channel'.format(to_channel.name))
		else:
			try:
				if ctx.message.author.id == 1556:
					await self.bot.move_member(member, to_channel)
			except discord.Forbidden:
				await self.bot.say('I have no permission to move members.')
			except discord.HTTPException:
				await self.bot.say('A error occured. Please try again')

def setup(bot):
	n = test(bot)
	bot.add_cog(n)
