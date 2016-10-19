import random
import discord
from discord.ext import commands
from .utils import checks
import asyncio
import time
try:
    from cleverbot import Cleverbot as Clv
except:
    Clv = False
from .utils.dataIO import dataIO
from __main__ import send_cmd_help, user_allowed
import os, os.path
import threading
from threading import Timer

class test:
	def __init__(self, bot):
		self.bot = bot
		self.base = 'data/test/images/'
		self.base2 = 'data/test/imagesj/'
		self.baselen = len([name for name in os.listdir('root/Red-DiscordBot/' + self.base) if os.path.isfile(name)])
		self.base2len = len([name for name in os.listdir('root/Red-DiscordBot/' + self.base2) if os.path.isfile(name)])
		self.clv = Clv()
		
	async def listener(self, message):
		if message.author.id != self.bot.user.id:
			if message.content.lower().startswith('hayy') or message.content.lower().startswith('haayy'):
				await self.bot.send_message(message.channel, '¡Harambe!')
			elif message.content.lower().startswith('japanese'):
				await self.bot.send_message(message.channel, 'I\'m sorry, I don\'t speak Japanese.')
	
	@commands.command(pass_context=True, invoke_without_command=True)
	async def pearl(self, context, message):
		try:
			await self.bot.send_file(context.message.channel, '{}meme (' + str(random.randInt(self.baselen)) + ').png'.format(self.base))
		except:
			await self.bot.say('An error occured.')
			
	@commands.command(pass_context=True, invoke_without_command=True)
	async def bar(self, context, message):
		try:
			await self.bot.send_file(context.message.channel, '{}meme (' + str(random.randInt(self.base2len)) + ').png'.format(self.base2))
		except:
			await self.bot.say('An error occured.')
			
	@commands.command(pass_context=True)
	@checks.admin_or_permissions(move_members=True)
	async def movevidem(self, context, message, to_channel: discord.Channel):
		type_to = str(to_channel.type)
		if type_to == 'text':
			await self.bot.say('{} is not a valid voice channel'.format(to_channel.name))
		else:
			try:
				if message.author.id == '138838298742226944':
					await self.bot.move_member(message.author, to_channel)
			except discord.Forbidden:
				await self.bot.say('I have no permission to move members.')
			except discord.HTTPException:
				await self.bot.say('An error occured. Please try again')
				
	@commands.command(pass_context=True)
	async def getchannelid(self, context, mesage):
		await self.bot.say(message.channel.id)
				
	@commands.command(pass_context=True)
	async def rateship(self, context, message, message2):
		stringthing = 'qwertyuiopasdfghjklzxcvbnm'

def setup(bot):
	n = test(bot)
	bot.add_listener(n.listener, "on_message")
	bot.add_cog(n)
