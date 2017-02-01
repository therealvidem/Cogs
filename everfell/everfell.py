import discord
from discord.ext import commands
import asyncio
import datetime

class everfell:
	def __init__(self, bot):
		self.bot = bot
		
	
				
def setup(bot):
	n = everfell(bot)
	bot.add_listener(n.listener, "on_message")
	bot.add_cog(n)
