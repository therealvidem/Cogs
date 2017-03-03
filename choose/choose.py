import discord
import random
from discord.ext import commands
import asyncio

class choose:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def choose(self, ctx, *args):
		choices = args.items()
		await self.bot.say(random.choice(choices))

def setup(bot):
	n = choose(bot)
	bot.add_cog(n)
