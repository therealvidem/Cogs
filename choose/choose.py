import discord
import random
from discord.ext import commands
import asyncio

class choose:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def choosebetween(self, ctx, *args):
		choices = list(args)
		if len(choices) > 1:
			await self.bot.say(random.choice(choices))
		else:
			await self.bot.say('Not enough choices to choose from.')

def setup(bot):
	n = choose(bot)
	bot.add_cog(n)
