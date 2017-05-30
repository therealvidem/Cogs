import discord
from discord.ext import commands
import asyncio

class reaction:
	def __init__(self, bot):
		self.bot = bot
		self.listenstart = {
			'sara': 'Ew!',
			'omg': '0 milligrams?',
			'0mg': 'Oh my god?',
			'syrz': 'It\'s called a dress.',
			'darnit': 'Amethyst, and Pearl, and Steven!',
			'bob': 'http://66.media.tumblr.com/5756bdebeb6a5e675ee45d68b6c09096/tumblr_ntt4qzMvQW1rz6w0do1_500.gif',
			'I': ''
		}
		self.listensub = {
			'kys': 'Kind your self?',
			'secret code': 'mewmewmew',
			'woah': 'whoa*,  you uneducated swine.',
			'thx': '***m̧̰̟̫̣̳̱̫̼̻̾ͦ͂̈́ͣ̽͆̄̾̄̾̚͞͠m̥̜͍͎̜̘̦̝͉͇͇ͪ̏ͬ̔̿̅͘͟͟͝͞ͅm̴̙̗̼͍͍̿͒̒̃̽̇͊͑̒̇̿̽̚͘͢͝͝m̶̵̲̖̬̦̀̄̓ͥ́͌ͭ̀̿̔͂̌̿m̡̘̻̞̘͕̭̗͖̭̺̦̞̥̹ͤͦ̆͑̅͛̂ͯ̒̃ͬ͂͛̈͜͜͠͞m͔̥͇͚̞͌̊͒ͫͩͫ̀M̌̆ͧ̃͒̃̂̍̐ͣͫ͏͙̥͕̟͖̜̰͍͎̩̫̥̺̭M͕̠̲̜̗͈̠͈̝͕̥̳͉͕͆̋̎̉ͭ̀̋ͬͬͯ͐͌͐ͯ̀́͟M̴͔̰̩̳̤̪̫͚͆̏ͮ̃ͥ̑́̄͑̉ͩ͑̉͐ͨ̑̀̓ͣ͠M̵̹̬̩͖̟͔̞ͨͨ̈ͨ͛̀M̧̢̝̘̲̮͈̰̻̮̰̩͉̜͋ͬͮ̐͑ͯ̽͢͟͝ͅM͊̃̎͒̔̾̎͋͗͂̈ͯͨ̽ͤ̅ͦ́͊͏̲͕͓͉̼̜͎̕͢ͅṂ̴̢̱͍͈͙̥̫̞̫̻͈̩͇͔̰̣̳ͨ̑̅̊ͭͪ̌̿̚M̵͔͍͔̺̤̪̲̣͔̠͖̝̳̠͎̥̼̒̏ͩ̄̑ͭ͠M̶̨̢̫͎̠̣͙͕̻ͫ͋̑̍͗ͣͩ͌̐ͤ͐̃̊ͬ̎̌ͫ̊͞͠ͅM̈̒̉͛ͩ̇ͭ̎̃ͬͦͭͩ̊҉̸̫͕͉̲̱͙̤͙͢ͅM͋ͪͯ͐ͯͫ͐̍͆̉͒̂̌͆ͥ͐͌̂͂͏̡҉̞͙̲̲̘͍̫̼̝̦̼͓Ḿ̷̭̮̦͎̞̙̣͙̟̼̲͎̘̼̲̙͊̅ͧͫ̚͜͠͞M̛̭̟͎̠̣̫̦̥̼̼̗͈ͫ̑̈̐ͭͭ͐ͥ̔̈́͡M̵̨̛̤̙̗͖͒ͯ̃͑̿̒ͦ̃ͨ̎́ͤ͆ͦ͒̍͛Ṁ̙̩̖̱̰͈͕̖͔̗̲͕͇̜͊̋ͫͪ̊ͫ̃̓ͫͨ̔̈ͦ̕͢͢ͅM̵̴̻̗̤̭͔͍̲̗̯͉̝͇̽͐ͫͮ͞M̸̝̤̲̠̬̝̰̣̼͓̍̏ͮ̽ͥͮ̄̏̊ͮ̌̋͌͊͡͝M̴̩̰̰̲̮̞͇͔̼̝͉̺̞̫͛̉ͥ̂̀́̋ͦ̊̽ͧ̄̀̔̍̎̈́̍M̎̋ͮ͏̘͉̙͖̜͞ͅM̜̮̰͈͎̺̟̬̲ͨ̆͗̾͒͊ͩͧ̆͘͟W̶̨̩̙̲̜̻̏͋ͫͤͥͮ̌ͩ͒ͩ̃́̏ͨA̶̷͖͉̲̗̫̰̰̭̿̍ͯͥ̍͌͋ͫ͂ͬ̐ͨÂ͌͒̋́̈̐̓̓̓ͩ̊ͫͨͩ͋̇͑̀͏͉͙͔̹̤̣̻̲͕A̸͙̺̼͍͎͇̯̬̓̏̅ͨͮ̄ͣͤ͐ͣ̚̕ͅA̵̸̡̛͙̹͔̱̩̺̬̺͇̩̺̞̳̫̹͕̖̮͆́̂ͬ͒̍̈́̎̾́A̡̨͍̟͓̥̤͊ͣͪ̉͛̓ͫ̌͐͘Ä̬̖̬̦̲̦̙ͩ͋͛̕͟͜A̵̻̝̖̲̹͎̫̱̬͍̣̠̺̲͙̬̣ͩ̆̾̅̆͌͟ͅͅA̶̡̤̼̙̭̩̲̼̼̝͍̋̒̒͑͊ͧͥ̕͡ͅA̷̧̠̝̣̟͉ͩͪ̃ͤ͆͑ͮͨ̊ͫ́̓ͦͮ͗̀͢͞ͅA̔̽͒̉̎ͬͦ̄͛̃̈́̚͞҉̷̺̬̘̭͘A̳͔̭͍̯̞͇̬̳͇͔͈̝̯͕̅ͨ͆ͣ̓̎ͥ̉̔̉̕͝Â͚͔̜͕̙̮̳̘͉̾̾̒́̎͆̑ͬ͜͢͞͠͝A̴̙̘͓̻̜̱̻̫̜͉͚̪͂ͯ͊͋̌ͬ̐̎̐̊͋̐̒͟͢͟A̧͖̻͍̥̠̟͖͙̠ͧ̃̓̓ͬ̀̃ͯͥͥ̎̒ͫ̀͢A̡̡̙̞̱̥̯̗̦͎͈̩͎ͯ̈́ͧ͊͑͊̑̎ͬ͛̓ͬͨ́ͫ͌̐̏͡A̴̢͈̲̗̬͙̤̙̞̭ͭ̔̀̄̍ͪ̀̑ͅĄ̵̳̰̲̥̝͖̈ͪ̒́͊ͣ̇ͥͫ͛ͤ̂ͧͮ̔A̡̡̰̲̥͉̙̞̬͈̫ͧͤͯ̋ͣͯ̀ͭ̃ͭ̔͆ͬ̎́͢A̵ͫͣ̿͊̀̌͏̸̫̜͔͕͉̕A̵͒̿ͦ́̉͘͏҉̶͇̹̼̟̯̝̰͈͈̣͇̯̩A͉̜͍͍̟̫͓̳̠͉̼̗̗ͦ̽ͩ̆́ͨ̐ͯͨ̇͒͐͐̈́̾̔̿̀Á̷̴̫̬̰̳͙͓̮̦͖̱̼͎̺͇̠̦ͥ̽͂͂̓̃͂̑͌͐̃͜ͅĂ̶̴̝̝͔̂ͧ͒̆̐͐̐͜͠ͅAͮ̔͗͋̌̽̈ͯͯͮ̿͗ͥ͡͠͏̱̠̙̩̣͈̝͙̬̯̪̟̭̜͇A̶̢̧͔̪͔̱͙͖̫̥̘̹̹͙̺̗̝̣͇ͪ͂ͫ́̿ͬ̀̽̉ͫ̽̈́̉ͫͪ̀Ą̶͇̗͎͕͉̪̟̅̈̿ͬͬ̅ͫͮͤ͆̽̾̀͠A̡̘̩̖̎ͬ̎ͧ̿̚͜͠Ȁ̍͂͌ͧ͑ͬ͒̋̌҉҉̛̤̖̬̤̗͉̮̝̦̠̼͚͔͝A̸̋̾ͤ͐̍ͥ͛̎̍̈̚͘͏̺̞͔̩̪̩̖̱̖̣̟̮̫A̧͚̼̟͔͈̜̝̹̳͖̞̻̗̞̯̩̘͖̖͋̉͆̊͗́ͫͤ̉̀͊̇͌ͩ͑ͩ̃̐̚͠͡A̴̡͚̻͙̪̩̹̲̮̺̭̳̺͖̜̤̗̯̓͂̒ͦͬ̊̔ͪ̍̿̏̏̎̑ͤ͑̒̊̅͟͞ͅ***',
			'pearl': '***W̙̮͔̞ͭ̂̉̈͑̈͗ͦ͆͟Hͧ̒̂͏̺̱̗̭̞͈̖A̞͎̳̖̙̫̤͇̽̒̈ͩ̔͒ͮ̚͢͞Ţ̘̳͕͓͉̫̩ͬ̍ͅ ̲̥̗̖̰̮ͨͩW̃ͪ̏̌̅̑ͩͫ̐҉͓͚̰̀͠Ě̢͉̥͙̜̩̈́ ̮͈̬͉̻̼͇̰͂ͥͨ̒ͯͯ͗̀R̨͉͍͒ͩ̽̀ͮ̊ͥ͡È̹̯̖̙͇̺̮̀̏ͬ̚Aͤͨ̈́ͪ͋ͣ̇ͭ͏̢̤̰̲L̡̻̪͕͔̘͉̩͈̇ͥ̎̅̓̋ͫ̉͡ͅL̢̪̙͈̟̦̣̝͂̾̃ͬ̀͐ͤͥỸ̡̛͈͇̥̲̱ͮ̿̋̂̍ͣ ̲͕̯͉ͧ͛́A̶̅͏̜̤͙͍̺̰R̢̘͍͇̮͈̾͟͠E̡͈̝̐̍͛̄͢***'
		}
		
	async def listener(self, message):
		if message.author.id != self.bot.user.id:
			if self.bot.user.id == '224328344769003520':
				container = ''
				for k, v in self.listenstart.items():
					if message.content[:len(k)].lower() == k:
						if k == 'ppap':
							container = message.author.name + '*'
						elif k == 'I':
							container = 'I predict ' + message.author.name + ' will say, "' + message.content + '"'
						await self.bot.send_message(message.channel, v + container)
				for k, v in self.listensub.items():
					if message.content.lower().find(k) != -1:
						await self.bot.send_message(message.channel, v)
			"""if message.content == 'vcnor FORM THE WEIRD QUARTET!' and self.bot.user.id == '224328344769003520':
				await asyncio.sleep(0.5)
				await self.bot.send_message(message.channel, 'VIDEM!')
			elif message.content == 'VIDEM!' and message.author.id == '224328344769003520' and self.bot.user.id == '276425303276912640':
				await asyncio.sleep(0.5)
				await self.bot.send_message(message.channel, 'CATALINA!')
			elif message.content == 'CATALINA!' and message.author.id == '276425303276912640' and self.bot.user.id == '283325760851410944':
				await asyncio.sleep(0.5)
				await self.bot.send_message(message.channel, 'MADISON!')
			elif message.content == 'MADISON!' and message.author.id == '283325760851410944' and self.bot.user.id == '283327246150926336':
				await asyncio.sleep(0.5)
				await self.bot.send_message(message.channel, 'AND RACHEL!')
			elif message.content == 'AND RACHEL!' and message.author.id == '283327246150926336' and (self.bot.user.id == '224328344769003520' or self.bot.user.id == '276425303276912640' or self.bot.user.id == '283325760851410944'):
				await asyncio.sleep(0.5)
				await self.bot.send_message(message.channel, 'AND WE ARE THE WEIRD QUARTET!')
			elif message.content == 'AND WE ARE THE WEIRD QUARTET!' and message.author.id == '283325760851410944' and self.bot.user.id == '283327246150926336':
				await self.bot.send_message(message.channel, 'AND WE ARE TEH WEIRD QUARTET!')"""
			
	async def voicelistener(self, before, after):
		if before.voice.voice_channel is None and after.voice.voice_channel:
			channel = [c for c in after.sever.channels if c.name == 'chat']
			await self.bot.send_message(channel, 'I predict that ' + after.nick + ' will join the voice channel.')
		elif before.voice.voice_channel and after.voice.voice_channel is None:
			channel = [c for c in after.sever.channels if c.name == 'chat']
			await self.bot.send_message(channel, 'I foresee that ' + after.nick + ' will leave the voice channel.')
				
def setup(bot):
	n = reaction(bot)
	bot.add_listener(n.listener, "on_message")
	bot.add_listener(n.voicelistener, "on_voice_state_update")
	bot.add_cog(n)
