import random
import discord
from discord.ext import commands
from .utils import checks
import asyncio
import time
import urllib.request
import simplejson
from io import StringIO
try:
    from cleverbot import Cleverbot as Clv
except:
    Clv = False
from .utils.dataIO import dataIO
from __main__ import send_cmd_help, user_allowed
import os, os.path
import threading
from threading import Timer
import requests
import shutil
from .utils.dataIO import dataIO

class test:
	def __init__(self, bot):
		self.bot = bot
		self.base = 'data/test/images/'
		self.base2 = 'data/test/imagesj/'
		self.base3 = 'data/test/imagesm/'
		self.memes = dataIO.load_json('data/test/memes.json')
		self.counting = False
		
	@commands.command(pass_context=True, invoke_without_command=True)
	async def memecount(self, context, memetype):
		await self.bot.say(memetype + ' has ' + str(self.memes[memetype]) + ' emotes.')
	
	@commands.command(pass_context=True, invoke_without_command=True)
	async def pearl(self, context, num = '0'):
		memenum = random.randint(1, self.memes['vp'])
		try:
			await self.bot.send_file(context.message.channel, self.base + 'meme_(' + str(num) + ').png')
		except:
			await self.bot.send_file(context.message.channel, self.base + 'meme_(' + str(memenum) + ').png')
			
	@commands.command(pass_context=True, invoke_without_command=True)
	async def bar(self, context, num = '0'):
		memenum = random.randint(1, self.memes['vb'])
		try:
			await self.bot.send_file(context.message.channel, self.base2 + 'meme (' + str(num) + ').png')
		except:
			await self.bot.send_file(context.message.channel, self.base2 + 'meme (' + str(memenum) + ').png')
			
	@commands.command(pass_context=True, invoke_without_command=True)
	async def meme(self, context, num = '0'):
		memenum = random.randint(1, self.memes['vm'])
		try:
			await self.bot.send_file(context.message.channel, self.base3 + 'meme (' + str(num) + ').png')
		except:
			await self.bot.send_file(context.message.channel, self.base3 + 'meme (' + str(memenum) + ').png')
			
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
	async def getchannelid(self, context):
		await self.bot.say(str(message.channel.id))

	@commands.command(pass_context=True)
	@checks.admin_or_permissions(kick_members=True)
	async def addvp(self, context, url):
		count = self.memes['vp'] + 1
		r = requests.get(url, stream=True)
		if r.status_code == 200:
			with open(self.base + 'meme_(' + str(count) + ').png', 'wb') as f:
				r.raw.decode_content = True
				shutil.copyfileobj(r.raw, f)
		# urllib.request.urlretrieve(url, self.base + 'memes (' + str(count) + ').png')
		self.memes['vp'] = count
		dataIO.save_json('data/test/memes.json', self.memes)
		await self.bot.say('Successfully added emote as vp ' + str(count))
		
	@commands.command(pass_context=True)
	@checks.admin_or_permissions(kick_members=True)
	async def addvb(self, context, url):
		count = self.memes['vb'] + 1
		r = requests.get(url, stream=True)
		if r.status_code == 200:
			with open(self.base2 + 'meme (' + str(count) + ').png', 'wb') as f:
				r.raw.decode_content = True
				shutil.copyfileobj(r.raw, f)
		# urllib.request.urlretrieve(url, self.base + 'memes (' + str(count) + ').png')
		self.memes['vb'] = count
		dataIO.save_json('data/test/memes.json', self.memes)
		await self.bot.say('Successfully added emote as vb ' + str(count))
		
	@commands.command(pass_context=True)
	@checks.admin_or_permissions(kick_members=True)
	async def addvm(self, context, url):
		count = self.memes['vm'] + 1
		r = requests.get(url, stream=True)
		if r.status_code == 200:
			with open(self.base3 + 'meme (' + str(count) + ').png', 'wb') as f:
				r.raw.decode_content = True
				shutil.copyfileobj(r.raw, f)
		# urllib.request.urlretrieve(url, self.base + 'memes (' + str(count) + ').png')
		self.memes['vm'] = count
		dataIO.save_json('data/test/memes.json', self.memes)
		await self.bot.say('Successfully added emote as vm ' + str(count))
		
	@commands.command(pass_context=True)
	async def rollbetween(self, context, one, two):
		choice = random.randint(int(one), int(two))
		await self.bot.say('You got a ' + str(choice) + '.')
		
	@commands.command(pass_context=True)
	async def factorial(self, context, n):
		if (int(n) >= 0):
			await self.bot.say(n + '! = ' + str(rFactorial(int(n))))
		elif (int(n) < 0):
			await self.bot.say("Are you trying to find the factorial of a negative number? You're batshit crazy, lad!")
		else:
			await self.bot.say('An error occured.')
	
	@commands.group(pass_context=True, name='count')
	async def _count(self, context):
		if context.invoked_subcommand is None:
			prefix = context.prefix
			await self.bot.say('Do \'{}count start [start number] {end number} {mention}\' (end number and mention being optional, defaulting to 0 and false, respectively) to start or \'{}count stop\' to stop any counting operation.').format(prefix)
	
	@_count.command(pass_context=True, name='start')
	async def _start(self, context, startnum: int=None, endnum: int=0, mention: str='false'):
		if self.counting == False:
			if startnum and endnum:
				chance = random.randint(1, 10)
				if (int(startnum) >= 0 and endnum < int(startnum)):
					self.counting = True
					for x in range(int(startnum), endnum - 1, -1):
						if (self.counting == True):
							await self.bot.say(str(x) + ',')
							await asyncio.sleep(1)
						else:
							break
					if (chance == 10):
						if (str(mention) == 'true'):
							await self.bot.say('https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcS4fQx4f2n6H0U1H8YuGbcCKFBIWAC0eCwn31Z2fbSqKyH8SB7ke_szKA ' + context.message.author.mention)
						else:
							await self.bot.say('https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcS4fQx4f2n6H0U1H8YuGbcCKFBIWAC0eCwn31Z2fbSqKyH8SB7ke_szKA')
					else:
						if (str(mention) == 'true'):
							await self.bot.say('TIME! ' + context.message.author.mention)
						else:
							await self.bot.say('TIME!')
					self.counting = False
				elif (int(startnum) >= 0 and endnum > int(startnum)):
					self.counting = True
					for x in range(int(startnum), endnum + 1):
						if (self.counting == True):
							await self.bot.say(str(x) + ',')
							await asyncio.sleep(1)
						else:
							break
					if (chance == 10):						
						if (str(mention) == 'true'):
							await self.bot.say('https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcS4fQx4f2n6H0U1H8YuGbcCKFBIWAC0eCwn31Z2fbSqKyH8SB7ke_szKA ' + context.message.author.mention)
						else:
							await self.bot.say('https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcS4fQx4f2n6H0U1H8YuGbcCKFBIWAC0eCwn31Z2fbSqKyH8SB7ke_szKA')
					else:
						if (str(mention) == 'true'):
							await self.bot.say('TIME! ' + context.message.author.mention)
						else:
							await self.bot.say('TIME!')
					self.counting = False
				else:
					await self.bot.say('An error occured.')
			else:
				await self.bot.say('An error occured.')
		else:
			await self.bot.say('I\'m already counting.')
			
	@_count.command(pass_context=True, name='stop')
	async def _stop(self, context):
		self.counting = False
		
def rFactorial(n):
	if (n == 0):
		return 1
	else:
		return n * (rFactorial(n - 1))

def setup(bot):
	n = test(bot)
	bot.add_cog(n)
