import discord
from discord.ext import commands
import asyncio

class reaction:
	def __init__(self, bot):
		self.bot = bot
		
	async def listener(self, message):
		if message.author.id != self.bot.user.id:
			if message.content.lower() == 'sara':
				await self.bot.send_message(message.channel, 'Ew!')
				
def setup(bot):
	n = reaction(bot)
	bot.add_listener(n.listener, "on_message")
	bot.add_cog(n)
