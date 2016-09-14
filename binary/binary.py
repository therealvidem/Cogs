import binascii
import discord
from discord.ext import commands

class binary:
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(pass_context=True)
	async def binarytoascii(self, *, message):
		try:
			await self.bot.say(bin(int(binascii.hexlify(message), 16)))
		except:
			await self.bot.say("Either you entered something invalid, or I fucked up.")
			
	@commands.command(pass_context=True)
	async def asciitobinary(self, context, message):
		try:
			n = int(message, 2)
			await self.bot.say(str(binascii.unhexlify('%x' % n)))
		except:
			await self.bot.say("Either you entered something invalid, or I fucked up.")

def setup(bot):
	n = binary(bot)
	bot.add_cog(n)
