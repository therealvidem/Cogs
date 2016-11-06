import discord
from discord.ext import commands
import asyncio

class reaction:
	def __init__(self, bot):
		self.bot = bot
		self.listensub = {
			'sara': 'Ew!',
			'omg': '0 milligrams?',
			'0mg': 'Oh my god?',
			'syrz': 'It\'s called a dress.',
			'darnit': 'Amethyst, and Pearl, and Steven!',
			'ppap': '*bans '
		}
		self.listenstart = {
			'hayy': '¡Harambe!',
			'japanese': 'I\'m sorry, I dont\'t speak Japanese.',
			'bob': 'http://66.media.tumblr.com/5756bdebeb6a5e675ee45d68b6c09096/tumblr_ntt4qzMvQW1rz6w0do1_500.gif',
			'woah': 'whoa*,  you uneducated swine.'
		}
		
	async def listener(self, message):
		if message.author.id != self.bot.user.id:
			container = ''
			for k, v in self.listensub.items():
				if message.content[0:len(k)].lower() == k:
					if k == 'ppap':
						container = message.author.name + '*'
					await self.bot.send_message(message.channel, v + container)
			for k, v in self.listenstart.items():
				if message.content.lower().find(k) != -1:
					await self.bot.send_message(message.channel, v)
				
def setup(bot):
	n = reaction(bot)
	bot.add_listener(n.listener, "on_message")
	bot.add_cog(n)
