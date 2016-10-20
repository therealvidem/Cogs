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
from .utils.dataIO import dataIO


class test:
	def __init__(self, bot):
		self.bot = bot
		self.base = 'data/test/images/'
		self.base2 = 'data/test/imagesj/'
		self.baselen = len([name for name in os.listdir('Red-DiscordBot/' + self.base) if os.path.isfile(name)])
		self.base2len = len([name for name in os.listdir('Red-DiscordBot/' + self.base2) if os.path.isfile(name)])
		self.clv = Clv()
		self.shiplist = dataIO.load_json("data/shiplist.json")
		self.shiplistsay = {
			'1': {
				'I think you should try harder'
			},
			'2': {
				'they\'ll last a week'
			},
			'3': {
				'it could be better... not really..'
			},
			'4': {
				'not that good but pretty decent'
			},
			'5': {
				'maybe it\'ll be work'	
			},
			'6': {
				'a little more interactiong would be great'
			},
			'7': {
				'the lucky number 7 is in favor of this ship'
			},
			'8': {
				'what a great ship'	
			},
			'9': {
				'HOT DAMN THAT\'S A NICE SHIP'	
			},
			'10': {
				'*bows down to the ship*'
			}
		}
		
	async def listener(self, message):
		if message.author.id != self.bot.user.id:
			if message.content.lower().startswith('hayy') or message.content.lower().startswith('haayy'):
				await self.bot.send_message(message.channel, '¡Harambe!')
			elif message.content.lower().startswith('japanese'):
				await self.bot.send_message(message.channel, 'I\'m sorry, I don\'t speak Japanese.')
			elif message.content.lower().startswith('woah'):
				await self.bot.send_message(message.channel, 'whoa*')
	
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
		if self.shiplist[message.content + " x " + message2.content]:
			ship = self.shiplist[message.content + " x " + message2.content]
			await.self.bot.say('I give the %q x %w ship a %e/10. %y.' % (message.content, message2.content, ship.rate, self.shiplistsay[ship.rate]))
		else:
			ship = {
				'p1': {message.content},
				'p2': {message2.content},
				'rate': {random.randInt(1, 10)}
			}
			self.shiplist[ship['p1'] + " x " + ship['p2']] = ship
			dataIO.save_json(JSON_PATH, self.shiplist)

def check_files():
    if not dataIO.is_valid_json('shiplist.json'):
        print("Creating duelist.json...")
        dataIO.save_json('shiplist.json', {})

def setup(bot):
	n = test(bot)
	check_files()
	bot.add_listener(n.listener, "on_message")
	bot.add_cog(n)
