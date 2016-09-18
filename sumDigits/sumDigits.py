import discord
from discord.ext import commands

class sumDigits:
	def __init__(self, bot):
		self.bot = bot
		
	def sumD(n):
    		newnum = 0
    		i = int(n)
    		while i > 0:
      			i /= 10
      			newnum += i % 10
    		return newnum;
			
	@commands.command(name="sumDigits")
	async def _sumDigits(self, *, message):
		try:
			await self.bot.say("Your answer: " + str(sumD(message)))
		except:
			await self.bot.say("Either you entered something invalid, or I fucked up.")

def setup(bot):
	n = sumDigits(bot)
	bot.add_cog(n)
