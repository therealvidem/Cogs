import discord
from discord.ext import commands

class sumDigits:
	def __init__(self, bot):
		self.bot = bot
		
	def sD(n):
    		newnum = 0
    		i = n
    		while i > 0:
      			i /= 10
      			newnum += i % 10
    		return newnum;
			
	@commands.command(name="sumDigits")
	async def _sumDigits(self, *, message):
		try:
			await self.bot.say("Your answer: " + sD(int(message)))
		except:
			await self.bot.say("Either you entered something invalid, or I fucked up.")

def setup(bot):
	n = sumDigits(bot)
	bot.add_cog(n)
