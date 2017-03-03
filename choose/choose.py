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
		
	@commands.command(pass_context=True)
	async def chooserate(self, ctx, *args):
		author = ctx.message.author
		choices = list(args)
		if len(choices) > 1:
			random.shuffle(choices)
			em = discord.Embed(title='Choices', colour=0x2F93E0)
			em.set_author(name=str(author), icon_url=author.avatar_url)
			for x in range(1, len(choices)):
				em.add_field(name=x, value=choices[x], inline=True)
			await self.bot.send_message(ctx.message.channel, embed=em)
		else:
			await self.bot.say('Not enough choices to choose from')

def setup(bot):
	n = choose(bot)
	bot.add_cog(n)
