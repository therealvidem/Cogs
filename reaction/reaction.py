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
			'bob': 'http://66.media.tumblr.com/5756bdebeb6a5e675ee45d68b6c09096/tumblr_ntt4qzMvQW1rz6w0do1_500.gif',
			'darnit': 'Amethyst, and Pearl, and Steven!',
			'ppap': '*bans '
		}
		self.listenstart = {
			'hayy': '¡Harambe!',
			'japanese': 'I\'m sorry, I dont\'t speak Japanese.',
			'woah': 'whoa*,  you uneducated swine.'
		}
		
	async def listener(self, message):
		if message.author.id != self.bot.user.id:
			container = ''
			for k, v in self.listensub.items():
				if message.content[0:len(k)].lower() == k:
					await.self.bot.send_message(message.channel, 'test')
					if k == 'ppap':
						await.self.bot.send_message(message.channel, 'test2')
						container = message.author.username + '*'
					await self.bot.send_message(message.channel, v + container)
			for k, v in self.listenstart.items():
				if message.content.lower().startswith(k):
					await self.bot.send_message(message.channel, v)
			# if message.content[0:4].lower() == 'sara':
			#	await self.bot.send_message(message.channel, 'Ew!')
			# elif message.content[0:3].lower() == 'omg':
			#	await self.bot.send_message(message.channel, '0 milligrams?')
			# elif message.content[0:3].lower() == '0mg':
			#	await self.bot.send_message(message.channel, 'Oh my god?')
			# elif message.content[0:4].lower() == 'syrz':
			#	await self.bot.send_message(message.channel, 'that was one of them sam constantly changed itt')
			# if message.content.lower().startswith('hayy') or message.content.lower().startswith('haayy'):
			#	await self.bot.send_message(message.channel, '¡Harambe!')
			# elif message.content.lower().startswith('japanese'):
			#	await self.bot.send_message(message.channel, 'I\'m sorry, I don\'t speak Japanese.')
			# elif message.content.lower().startswith('woah'):
			#	await self.bot.send_message(message.channel, 'whoa*,  you uneducated swine.')
				
def setup(bot):
	n = reaction(bot)
	bot.add_listener(n.listener, "on_message")
	bot.add_cog(n)
