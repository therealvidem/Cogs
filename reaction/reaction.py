import discord
from discord.ext import commands
import asyncio

class reaction:
	def __init__(self, bot):
		self.bot = bot
		
	async def listener(self, message):
		if message.author.id != self.bot.user.id:
			if message.content[0:4].lower() == 'sara':
				await self.bot.send_message(message.channel, 'Ew!')
			elif message.content[0:3].lower() == 'omg':
				await self.bot.send_message(message.channel, '0 milligrams?')
			elif message.content[0:3].lower() == '0mg':
				await self.bot.send_message(message.channel, 'Oh my god?')
			elif message.content[0:4].lower() == 'syrz':
				await self.bot.send_message(message.channel, 'that was one of them sam constantly changed itt')
			if message.content.lower().startswith('hayy') or message.content.lower().startswith('haayy'):
				await self.bot.send_message(message.channel, '¡Harambe!')
			elif message.content.lower().startswith('japanese'):
				await self.bot.send_message(message.channel, 'I\'m sorry, I don\'t speak Japanese.')
			elif message.content.lower().startswith('woah'):
				await self.bot.send_message(message.channel, 'whoa*,  you uneducated swine.')
				
def setup(bot):
	n = reaction(bot)
	bot.add_listener(n.listener, "on_message")
	bot.add_cog(n)
