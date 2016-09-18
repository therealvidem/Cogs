import discord
from discord.ext import commands

class sumDigits:
	def __init__(self, bot):
	  self.bot = bot
		
	def sumDigits(int n):
    newnum = 0
    while n > 0:
      n /= 10
      newnum += n % 10
    return newnum
			
	@commands.command(name="sumDigits")
	async def _sumDigits(self, *, message):
		try:
			await self.bot.say(str(sumDigits(int(message))))
		except:
			await self.bot.say("Either you entered something invalid, or I fucked up.")

def setup(bot):
	n = sumDigits(bot)
  bot.add_cog(n)
