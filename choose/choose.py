import discord
import random
from discord.ext import commands
import asyncio

class choose:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def choosebetween(self, ctx, *args):
		choices = args.items()
		await self.bot.say(random.choice(choices))
		
	@commands.command(pass_context=True)
	async def chooserate(self, ctx, *args):
		author = ctx.message.author
		choices = args.items().shuffle()
		em = discord.Embed(title='Choices', colour=0x2F93E0)
		em.set_author(name=str(author), icon_url=author.avatar_url)
		await client.send_message(ctx.message.channel, embed=em)

def setup(bot):
	n = choose(bot)
	bot.add_cog(n)
