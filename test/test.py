import random
import discord
from discord.ext import commands
from .utils import checks
import asyncio
import time
import operator
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
		self.stabbingobjects = dataIO.load_json('data/test/stabbingobjects.json')
		self.coffee = dataIO.load_json('data/test/coffee.json')
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
	@checks.admin()
	async def addvp(self, context, url):
		r = requests.get(url, stream=True)
		if r.status_code == 200:
			count = self.memes['vp'] + 1
			with open(self.base + 'meme_(' + str(count) + ').png', 'wb') as f:
				r.raw.decode_content = True
				shutil.copyfileobj(r.raw, f)
			self.memes['vp'] = count
			dataIO.save_json('data/test/memes.json', self.memes)
			await self.bot.say('Successfully added emote as vp ' + str(count))
		else:
			await self.bot.say('Unable to add emote.')
		
	@commands.command(pass_context=True)
	@checks.admin()
	async def addvb(self, context, url):
		r = requests.get(url, stream=True)
		if r.status_code == 200:
			count = self.memes['vb'] + 1
			with open(self.base2 + 'meme_(' + str(count) + ').png', 'wb') as f:
				r.raw.decode_content = True
				shutil.copyfileobj(r.raw, f)
			self.memes['vb'] = count
			dataIO.save_json('data/test/memes.json', self.memes)
			await self.bot.say('Successfully added emote as vb ' + str(count))
		else:
			await self.bot.say('Unable to add emote.')
		
	@commands.command(pass_context=True)
	@checks.admin()
	async def addvm(self, context, url):
		r = requests.get(url, stream=True)
		if r.status_code == 200:
			count = self.memes['vm'] + 1
			with open(self.base3 + 'meme_(' + str(count) + ').png', 'wb') as f:
				r.raw.decode_content = True
				shutil.copyfileobj(r.raw, f)
			self.memes['vm'] = count
			dataIO.save_json('data/test/memes.json', self.memes)
			await self.bot.say('Successfully added emote as vm ' + str(count))
		else:
			await self.bot.say('Unable to add emote.')
		
	@commands.command(pass_context=True)
	async def rollbetween(self, context, one, two):
		choice = random.randint(int(one), int(two))
		await self.bot.say('You got a ' + str(choice) + '.')
		
	@commands.command(pass_context=True)
	async def factorial(self, context, n: int=None):
		if n is None:
			await self.bot.say('wat')
		elif n > 0:
			await self.bot.say(str(n) + '! = ' + str(rFactorial(n)))
		elif n < 0:
			await self.bot.say("Are you trying to find the factorial of a negative number? You're batshit crazy, lad!")
			
	@commands.command(pass_context=True)
	async def permutations(self, context, n: int=None, r: int=None):
		if n is None or r is None:
			await self.bot.say('wat')
		elif n > 0 and r > 0:
			await self.bot.say(str(n) + 'P' + str(r) + ' = ' + str(rFactorial(n) / rFactorial(n - r)))
		elif n < 0 or r < 0:
			await self.bot.say('I dunno what the means.')
	
	@commands.command(pass_context=True)
	async def combinations(self, context, n: int=None, r: int=None):
		if n is None or r is None:
			await self.bot.say('wat')
		elif n > 0 and r > 0 and n >= r:
			await self.bot.say(str(n) + 'C' + str(r) + ' = ' + str(rFactorial(n) / (rFactorial(n - r) * rFactorial(r))))
		elif n < 0 or r < 0:
			await self.bot.say('I dunno what the means.')

	@commands.group(pass_context=True, name='coffee')
	async def _coffee(self, context):
		if context.invoked_subcommand is None:
			if context.message.server.id not in self.coffee:
				self.coffee[context.message.server.id] = {}
			await self.bot.say('Do {}help coffee.'.format(context.prefix)) 

	@_coffee.command(pass_context=True, name='plus')
	@checks.admin()
	async def _plus(self, context, member: discord.Member=None):
		if member:
			if member.id not in self.coffee[context.message.server.id]:
				self.coffee[context.message.server.id][member.id] = 0
			numcoffee = self.coffee[context.message.server.id][member.id] + 1
			self.coffee[context.message.server.id][member.id] = numcoffee
			dataIO.save_json('data/test/coffee.json', self.coffee)
			await self.bot.say('Gave 1 coffee to ' + member.mention + '!')
	
	@_coffee.command(pass_context=True, name='subtract')
	@checks.admin()
	async def _subtract(self, context, member: discord.Member=None):
		if member:
			if member.id not in self.coffee[context.message.server.id]:
				self.coffee[context.message.server.id][member.id] = 0
			numcoffee = max(0, self.coffee[context.message.server.id][member.id] - 1)
			self.coffee[context.message.server.id][member.id] = numcoffee
			dataIO.save_json('data/test/coffee.json', self.coffee)
			await self.bot.say('Took 1 coffee from ' + member.mention + '!')
			
	@_coffee.command(pass_context=True, name='give')
	@checks.admin()
	async def _give(self, context, member: discord.Member=None, n: int=1):
		if member:
			if member.id not in self.coffee[context.message.server.id]:
				self.coffee[context.message.server.id][member.id] = 0
			numcoffee = self.coffee[context.message.server.id][member.id] + n
			self.coffee[context.message.server.id][member.id] = numcoffee
			dataIO.save_json('data/test/coffee.json', self.coffee)
			await self.bot.say('Gave ' + str(n) + ' coffee to ' + member.mention + '!')
			
	@_coffee.command(pass_context=True, name='set')
	@checks.admin()
	async def _set(self, context, member: discord.Member=None, numcoffee: int=1):
		if member:
			if member.id not in self.coffee[context.message.server.id]:
				self.coffee[context.message.server.id][member.id] = 0
			self.coffee[context.message.server.id][member.id] = numcoffee
			dataIO.save_json('data/test/coffee.json', self.coffee)
			await self.bot.say('Set ' + member.mention + '\'s number of coffee to ' + str(numcoffee) + '!')
			
	@_coffee.command(pass_context=True, name='reset')
	async def _reset(self, context, member: discord.Member=None):
		if member:
			try:
				self.coffee[context.message.server.id].pop(member.id, None)
			except KeyError:
				await self.bot.say('Person doesn\'t exist.')
			
	@_coffee.command(pass_context=True, name='list')
	async def _list(self, context):
		em = discord.Embed(title='Coffee Leaderboard', color=discord.Color.red())
		i = 0
		for person,value in sorted(self.coffee[context.message.server.id].items()):
			i += 1
			personname = ''
			for p in context.message.server.members:
				if p.id == person:
					personname = p.name
			coffeetext = 'coffees' if value > 1 else 'coffee'
			em.add_field(name=str(i) + '. ' + personname + '\a', value=str(value) + ' ' + coffeetext)
		await self.bot.say(embed=em)
	
	@commands.command(pass_context=True)
	async def sauce(self, context):
		await self.bot.say('***H̭̓͗̏̅͘E̳̰̠͖͓͕͊͋ͯͭ̿̔Ÿ͓̜͎̪͉́͆ͮ̇́̆̊̒̈͝ ̷̧̖̌ͮ̉̂̿ͪ͗̔V̶̯̩̤̥ͧ͊̋͊ͧ͞S̴̷̳͈̓͗̽̏̇A̶͎͈̔̍ͨ̉̚͞U̼̻͍̬̪̦ͦ͌ͩ̑͋͊̈́ͅC̺̻̪̯̗̖̖͂ͪ̈́̕Ȩ̮̤̫̯̟ͭ͌̅̒̄͘͠ͅ,̗͖̯͙͖̮̪̏́ ̶̨̫̮͎̗̣͋̍̓͟M̐͂͞͏̘̥͎̕I̴̭͉̰͎͈͎͔̗̭ͥ͒͗̊́͘C̷̗̬͙͎̠͇͊̔ͦ̆͠H̡̋͐͗́̚͝҉̫̣̳̦̥̮̗̜ͅĂ͓̹͙̽ͨ̑̋̈́̚͘͠E̢̺̘̳̬͙̅ͪͮ͒͑̒͒̇͂͞L͔̣̟̗͉̹̾͊̈́͋ͭ̑ͥ̕ ͬͯ҉̡̨͓̝̗̺H̰͕͌ͨĘ̳̟͕̹̘̠͇͎́̄͑̀ͅR͈̳ͬ̉Eͣ͞҉̳̘̦͉̞̣***')
	
	@commands.command(pass_context=True)
	async def stab(self, context, *, member: discord.Member=None):
		obj = random.choice(self.stabbingobjects['objects'])
		word = random.choice(["shanks", "stabs", "shoves", "impales", "injects", "thrusts", "knifes", "punctures", "jabs",
				      "lunges at", "prods"]
		await self.bot.say('{0} {1} {2} with {3}.'.format(context.message.author.name, word, member.mention, obj))
		
	@commands.command(pass_context=True)
	async def pat(self, context, member: discord.Member=None, n: int=3):
		member = member or context.message.author
		if n and n <= 650 and n > 0:
			if member.id != self.bot.user.id:
				await self.bot.say(member.mention + ' *' + ('pat' * n) + '*')
			else:
				await self.bot.say('*eternally pats self*')
		else:
			if n > 650:
				await self.bot.say('That\'s too many pats!')
			elif n == -1:
				await self.bot.say(member.mention + ' *' + ('pat' * 650) + '*')
			elif n < -1:
				await self.bot.say('I don\'t know how to pat you that many times.')
			else:
				await self.bot.say('wat')
				
	@commands.command(pass_context=True)
	async def aaa(self, context, n: int=10):
		if n and n <= 1987 and n > 0:
			await self.bot.say('***' + ('A' * n) + '***')
		else:
			if n > 1987:
				await self.bot.say('That\'s too loud, calm down!')
			elif n == -1:
				await self.bot.say('***' + ('A' * 1987) + '***')
			elif n < -1:
				await self.bot.say('Are you silent?')
			else:
				await self.bot.say('wat')
		
	@commands.command(pass_context=True)
	async def addstab(self, context, *, obj: str=None):
		if obj and obj not in self.stabbingobjects['objects']:
			obj = obj.rstrip(".");
			allowed = True
			listofpeople = []
			for person in context.message.server.members:
				if obj == person.mention:
					allowed = False
					break
			if allowed:
				self.stabbingobjects['objects'].append(obj)
				dataIO.save_json('data/test/stabbingobjects.json', self.stabbingobjects)
				await self.bot.say('Successfully added ' + obj + ' as a stabby stabby object.')
			else:
				await self.bot.say('I can\'t add mentions.')
		else:
			if obj in self.stabbingobjects['objects']:
				await self.bot.say('That\'s already in my knife collection.')			
			else:
				await self.bot.say('wat')
			
	@commands.command(pass_context=True)
	async def removestab(self, context, *, obj: str=None):
		if obj and obj in self.stabbingobjects['objects']:
			self.stabbingobjects['objects'].remove(obj)
			dataIO.save_json('data/test/stabbingobjects.json', self.stabbingobjects)
			await self.bot.say('Successfully removed ' + obj + ' from my knife collection.')
		else:
			await self.bot.say('wat')
			
	@commands.command(pass_context=True)
	async def liststab(self, context):
		objs = ''
		for obj in self.stabbingobjects['objects']:
			objs += '**{}**\n'.format(obj)
		em = discord.Embed(title='My Knife Collection', color=discord.Color.green())
		em.add_field(name='\a', value=objs)
		#em = discord.Embed(title='My Knife Collection', colour=0x2F93E0)
		#for x in range(0, len(self.stabbingobjects['objects'])):
		#	em.add_field(name=x + 1, value=self.stabbingobjects['objects'][x])
		await self.bot.say(embed=em)
	
	@commands.command(pass_context=True)
	async def eh(self, context, member: discord.Member=None):
		member = member or context.message.author
		await self.bot.say(member.mention + ', eh?')
	
	@commands.group(pass_context=True, name='count')
	async def _count(self, context):
		if context.invoked_subcommand is None:
			prefix = context.prefix
			await self.bot.say('Do \'{0}count start <start number> [end number] [mention]\' (end number and mention being optional, defaulting to 0 and false, respectively) to start or \'{0}count stop\' to stop any counting operation.'.format(prefix))
	
	@_count.command(pass_context=True, name='start')
	async def _start(self, context, startnum: int=None, endnum: int=0, mention: str='false'):
		if self.counting == False:
			if startnum:
				chance = random.randint(1, 10)
				if (startnum >= 0 and endnum < startnum):
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
				elif (startnum >= 0 and endnum > startnum):
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
