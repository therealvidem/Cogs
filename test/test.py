import random
import discord
from discord.ext import commands
from .utils import checks
import asyncio
import time

class test:
	def __init__(self, bot):
		self.bot = bot
		self.base = 'data/test/images/'
		self.base2 = 'data/test/imagesj/'
		
	async def listener(self, message):
		if message.author.id != self.bot.user.id:
			if message.author.id == '81026656365453312':
				time.sleep(1)
				quotes = ["Abby!","So… um…","How was it back there in your visit to Hawaii?","That’s nice…","I’m just a little tired, that’s all.","Well... I kind of…","Shh…!","Quiet! Not so loud…","Well, not just her- I mean, darnit, why would I-","Look, this secret had to have gone out one way or the other.","W... why should we have kept it a secret? If I did, Kitten would’ve hated me even more!","It’s… me.","Yes, I want to apologize for the things I’ve done, to you and to Kitten. I shouldn’t have kept thesecret and I should have kept the secret at the same time. I’m sorry for trying to kill you, and I’m sorry for being so irresponsible of my father and boyfriend status.","Would you like to, you know, dance with me?","Abby! What is it?","Dr. Marv is fine on his own, didn’t you see him beat up that fashion guy?","Let’s do this.","Ah, yes! I’ve been meaning to tell you that Kitten is well and alive!","I’m not sure, she should be here any-","Huh? Oh, right! Sure.","So…","Well… he seems to just not care about me after Isabelle came along.","Abby… I want to confess.","Before you came along, I… kind of… well…","I know, but-","Before you came, I had feelings for Catalina…","But, of course I did.","There’s just some sort of magnetic force between Catalin-","We’re still friends.... right?","Um… hi...","Yes, well… remember the time I gave you that heart crystal… well, I just wanted to say… I have feelings for you…","So, what do you want to do first?","Oh my god, yes! We should!","Same.","I don’t think we should run into the forest!","Well- it’s that- I, uh…","Spicy and I were walking in the forest-","It’s not- that! Spicy and I saw this strange woman with magical spells named Cherrie!- No wait, was it Cherrie or Chara? I can’t remember. Anyway, we met this woman-","and she claimed she knew us, and that she tried to kill me in the bathroom!","Crazy. I know, right?","I think we should be safe here. If we see him coming, we should run…","If they come, we’ll hear them. If we come, they’ll hear us louder, and if we run, they’ll be there.","I just- wanted some time to rest and think.","Uh…","Well… what?","You know, sometimes, I think to myself, does a star ever die?","That’s not what I mean. What I meantersay is; do stars ever fully dissipate itself from the universe? Science says its atoms merely convert into something else- even in black holes- but, perhaps, there is something that can cause anything to disappear forever, not leaving any trail of it behind. Boom. It’s gone and done for. Would it not be known or remembered, as its existence was only merely an illusion?","Did you hear that?","Run, Abby! Go, hurry!","Of course, I had to keep it a secret! I also lied about the vacation…","I-I… it’s a long story…","No.","You deserve to hate me, for what I did- I feel guilty…","Abby, just look at the situation right now! I lied to you and this entire group the whole time, I put you into a trap that killed my stupid roommate, and I- I didn’t love you, and I regret it.","No. Nothing can clean up the mess I’ve created, and now the world’s in danger because of me…","Our story. The origin of the group… I was going to give it to you guys earlier, but…","Y-yes, indeed we are."]
				await self.bot.send_message(message.channel, '!chat ' + random.choice(quotes))
			elif message.content.lower().startswith('hayy') or message.content.lower().startswith('haayy'):
				await self.bot.send_message(message.channel, '¡Harambe!')
			elif message.content.lower().startswith('japanese'):
				await self.bot.send_message(message.channel, 'I\'m sorry, I don\'t speak Japanese.')
	
	@commands.command(pass_context=True, invoke_without_command=True)
	async def pearl(self, context, message):
		try:
			message = int(message)
			s = '{}meme_(' + str(message) + ').png'
			s2 = '{}meme_(' + str(message) + ').PNG'
		except:
			n = random.randint(1,136)
			s = '{}meme_(' + str(n) + ').png'
			s2 = '{}meme_(' + str(n) + ').PNG'
		try:
			await self.bot.send_file(context.message.channel, s.format(self.base))
		except:
			await self.bot.send_file(context.message.channel, s2.format(self.base))
			
	@commands.command(pass_context=True, invoke_without_command=True)
	async def bar(self, context, message):
		try:
			message = int(message)
			s = '{}meme (' + str(message) + ').png'
			s2 = '{}meme (' + str(message) + ').PNG'
		except:
			n = random.randint(1,17)
			s = '{}meme (' + str(n) + ').png'
			s2 = '{}meme (' + str(n) + ').PNG'
		try:
			await self.bot.send_file(context.message.channel, s.format(self.base2))
		except:
			await self.bot.send_file(context.message.channel, s2.format(self.base2))
			
	@commands.command(pass_context=True)
	async def talktoabby(self, context):
		quotes = ["Abby!","So… um…","How was it back there in your visit to Hawaii?","That’s nice…","I’m just a little tired, that’s all.","Well... I kind of…","Shh…!","Quiet! Not so loud…","Well, not just her- I mean, darnit, why would I-","Look, this secret had to have gone out one way or the other.","W... why should we have kept it a secret? If I did, Kitten would’ve hated me even more!","It’s… me.","Yes, I want to apologize for the things I’ve done, to you and to Kitten. I shouldn’t have kept thesecret and I should have kept the secret at the same time. I’m sorry for trying to kill you, and I’m sorry for being so irresponsible of my father and boyfriend status.","Would you like to, you know, dance with me?","Abby! What is it?","Dr. Marv is fine on his own, didn’t you see him beat up that fashion guy?","Let’s do this.","Ah, yes! I’ve been meaning to tell you that Kitten is well and alive!","I’m not sure, she should be here any-","Huh? Oh, right! Sure.","So…","Well… he seems to just not care about me after Isabelle came along.","Abby… I want to confess.","Before you came along, I… kind of… well…","I know, but-","Before you came, I had feelings for Catalina…","But, of course I did.","There’s just some sort of magnetic force between Catalin-","We’re still friends.... right?","Um… hi...","Yes, well… remember the time I gave you that heart crystal… well, I just wanted to say… I have feelings for you…","So, what do you want to do first?","Oh my god, yes! We should!","Same.","I don’t think we should run into the forest!","Well- it’s that- I, uh…","Spicy and I were walking in the forest-","It’s not- that! Spicy and I saw this strange woman with magical spells named Cherrie!- No wait, was it Cherrie or Chara? I can’t remember. Anyway, we met this woman-","and she claimed she knew us, and that she tried to kill me in the bathroom!","Crazy. I know, right?","I think we should be safe here. If we see him coming, we should run…","If they come, we’ll hear them. If we come, they’ll hear us louder, and if we run, they’ll be there.","I just- wanted some time to rest and think.","Uh…","Well… what?","You know, sometimes, I think to myself, does a star ever die?","That’s not what I mean. What I meantersay is; do stars ever fully dissipate itself from the universe? Science says its atoms merely convert into something else- even in black holes- but, perhaps, there is something that can cause anything to disappear forever, not leaving any trail of it behind. Boom. It’s gone and done for. Would it not be known or remembered, as its existence was only merely an illusion?","Did you hear that?","Run, Abby! Go, hurry!","Of course, I had to keep it a secret! I also lied about the vacation…","I-I… it’s a long story…","No.","You deserve to hate me, for what I did- I feel guilty…","Abby, just look at the situation right now! I lied to you and this entire group the whole time, I put you into a trap that killed my stupid roommate, and I- I didn’t love you, and I regret it.","No. Nothing can clean up the mess I’ve created, and now the world’s in danger because of me…","Our story. The origin of the group… I was going to give it to you guys earlier, but…","Y-yes, indeed we are."]
		await self.bot.say('!chat ' + random.choice(quotes))
			
	@commands.command(pass_context=True)
	@checks.admin_or_permissions(move_members=True)
	async def movevidem(self, context, message, to_channel: discord.Channel):
		type_to = str(to_channel.type)
		if type_to == 'text':
			await self.bot.say('{} is not a valid voice channel'.format(to_channel.name))
		else:
			try:
				if message.author.id == 1556:
					await self.bot.move_member(message.author, to_channel)
			except discord.Forbidden:
				await self.bot.say('I have no permission to move members.')
			except discord.HTTPException:
				await self.bot.say('A error occured. Please try again')
				
	@commands.command(pass_context=True)
	async def rateship(self, context, message, message2):
		stringthing = 'qwertyuiopasdfghjklzxcvbnm'
		

def setup(bot):
	n = test(bot)
	bot.add_listener(n.listener, "on_message")
	bot.add_cog(n)
