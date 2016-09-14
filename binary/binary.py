import binascii
import discord
from discord.ext import commands

class binary:
	def __init__(self, bot):
		self.bot = bot
		
	def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
		bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
		return bits.zfill(8 * ((len(bits) + 7) // 8))

	def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    		n = int(bits, 2)
    		return int2bytes(n).decode(encoding, errors)
	
	@commands.command()
	async def binarytoascii(self, *, message):
		try:
			await self.bot.say(text_from_bits(message))
		except:
			await self.bot.say("Either you entered something invalid, or I fucked up.")
			
	@commands.command()
	async def asciitobinary(self, *, message):
		try:
			await self.bot.say(text_to_bits(message))
		except:
			await self.bot.say("Either you entered something invalid, or I fucked up.")

def setup(bot):
	n = binary(bot)
	bot.add_cog(n)
