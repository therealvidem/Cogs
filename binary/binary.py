import discord
from discord.ext import commands

class binary:
	def __init__(self, bot):
		self.bot = bot
		
	def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    		bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    		return bits.zfill(8 * ((len(bits) + 7) // 8))

	def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    		n = int(bits, 2)
    		return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'
	
	@commands.command(name="binarytoascii")
	async def _binarytoascii(self, *, message):
		try:
			await self.bot.say(str(text_from_bits(message)))
		except:
			await self.bot.say("Either you entered something invalid, or I fucked up.")
			
	@commands.command(name="asciitobinary")
	async def _asciitobinary(self, *, message):
		try:
			await self.bot.say(str(text_to_bits(message)))
		except:
			await self.bot.say("Either you entered something invalid, or I fucked up.")

def setup(bot):
	n = binary(bot)
	bot.add_cog(n)
