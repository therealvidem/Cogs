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
import os

class talktoabby:
	def __init__(self, bot):
		self.bot = bot
		self.clv = Clv()
			
	async def listener(self, message):
		if message.author.id == '81026656365453312' and message.channel.id == '276490574624849920':
			await asyncio.sleep(10)
			response = await self.get_response(message.content)
			await self.bot.send_message(message.channel, '!chat ' + response)
			
	@commands.command(pass_context=True)
	async def talktoabby(self, context):
		await self.bot.say('!chat Hi Abby.')
		
	async def get_response(self, msg):
		question = self.bot.loop.run_in_executor(None, self.clv.ask, msg)
		try:
		    answer = await asyncio.wait_for(question, timeout=10)
		except asyncio.TimeoutError:
		    answer = "We'll talk later..."
		return answer

def setup(bot):
	n = talktoabby(bot)
	bot.add_listener(n.listener, "on_message")
	bot.add_cog(n)
