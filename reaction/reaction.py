import discord
from discord.ext import commands
import asyncio
import random

class reaction:
	def __init__(self, bot):
		self.bot = bot
		self.listenstart = {
			'sara': 'Ew!',
			'syrz': 'It\'s called a dress.'
		}
		self.listensub = {
			'kys': 'Kind your sorrow?',
			'secret code': 'mewmewmew',
			'woah': 'whoa*,  you uneducated swine.',
			'are you ok': 'https://i.imgur.com/4hthkl5.jpg',
			'are you gonna be ok': 'https://i.imgur.com/4hthkl5.jpg',
			'are u gonna b ok': 'https://i.imgur.com/4hthkl5.jpg',
			'r u gonna be ok': 'https://i.imgur.com/4hthkl5.jpg',
			'r you gonna b ok': 'https://i.imgur.com/4hthkl5.jpg',
			'r you gonna be ok': 'https://i.imgur.com/4hthkl5.jpg',
			'r u gonna b ok': 'https://i.imgur.com/4hthkl5.jpg',
			'are u gonna be ok': 'https://i.imgur.com/4hthkl5.jpg',
			'are u ok': 'https://i.imgur.com/4hthkl5.jpg',
			'r u ok': 'https://i.imgur.com/4hthkl5.jpg',
			'r you ok': 'https://i.imgur.com/4hthkl5.jpg'
		}
		self.foreseelist = [
			'foresee',
			'predict',
			'think',
			'anticipate',
			'foretell',
			'prophesy'
		]
		
	async def listener(self, message):
		if not message.author.bot:
			container = ''
			for k, v in self.listenstart.items():
				if message.content[:len(k)].lower() == k:
					ok = False
					if len(message.content) > len(k):
						if message.content[len(k):len(k) + 1] == ' ':
							ok = True
					else:
						ok = True
					if ok:
						if k == 'i' or k == "i'm" or k == "i've":
							container = 'I ' + random.choice(self.foreseelist) + ' ' + message.author.name + ' will say, "' + message.content + '"'
							await asyncio.sleep(random.randint(1, 10))
						await self.bot.send_message(message.channel, v + container)
			for k, v in self.listensub.items():
				if message.content.lower().find(k) != -1:
					await self.bot.send_message(message.channel, v)
			"""if message.content == 'vcnor FORM THE WEIRD QUARTET!' and self.bot.user.id == '224328344769003520':
				await asyncio.sleep(0.5)
				await self.bot.send_message(message.channel, 'VIDEM!')
			elif message.content == 'VIDEM!' and message.author.id == '224328344769003520' and self.bot.user.id == '276425303276912640':
				await asyncio.sleep(0.5)
				await self.bot.send_message(message.channel, 'CATALINA!')
			elif message.content == 'CATALINA!' and message.author.id == '276425303276912640' and self.bot.user.id == '283325760851410944':
				await asyncio.sleep(0.5)
				await self.bot.send_message(message.channel, 'MADISON!')
			elif message.content == 'MADISON!' and message.author.id == '283325760851410944' and self.bot.user.id == '283327246150926336':
				await asyncio.sleep(0.5)
				await self.bot.send_message(message.channel, 'AND RACHEL!')
			elif message.content == 'AND RACHEL!' and message.author.id == '283327246150926336' and (self.bot.user.id == '224328344769003520' or self.bot.user.id == '276425303276912640' or self.bot.user.id == '283325760851410944'):
				await asyncio.sleep(0.5)
				await self.bot.send_message(message.channel, 'AND WE ARE THE WEIRD QUARTET!')
			elif message.content == 'AND WE ARE THE WEIRD QUARTET!' and message.author.id == '283325760851410944' and self.bot.user.id == '283327246150926336':
				await self.bot.send_message(message.channel, 'AND WE ARE TEH WEIRD QUARTET!')"""
			
	'''async def voicelistener(self, before, after):
		if not message.author.bot:
			if before.voice.voice_channel is None and after.voice.voice_channel:
				channel = [c for c in after.server.channels if c.id == '132586673383931904']
				await asyncio.sleep(random.randint(1, 10))
				await self.bot.send_message(channel[0], 'I ' + random.choice(self.foreseelist) + ' that ' + after.name + ' will join the voice channel.')
			elif before.voice.voice_channel and after.voice.voice_channel is None:
				channel = [c for c in after.server.channels if c.id == '132586673383931904']
				await asyncio.sleep(random.randint(1, 10))
				await self.bot.send_message(channel[0], 'I ' + random.choice(self.foreseelist) + ' that ' + after.name + ' will leave the voice channel.')'''
				
def setup(bot):
	n = reaction(bot)
	bot.add_listener(n.listener, "on_message")
	'''bot.add_listener(n.voicelistener, "on_voice_state_update")'''
	bot.add_cog(n)
