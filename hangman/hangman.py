import discord
import os
import random
from discord.ext import commands
from .utils import checks
import asyncio

WORD_LIST = open('data/hangman/words2.txt', 'r')
WORDS = WORD_LIST.readlines()

class hangman:
	def __init__(self, bot):
		self.bot = bot
		self.insession = False
		self.guesses = list()
		self.word = ''
		self.numguesses = 0
		self.guessword = ''
        
	@commands.command(pass_context=True)
	@commands.cooldown(2, 2, commands.BucketType.user)
	async def hangman(self, context, message):
		if message.isalpha():
			msg = message.lower()
			if msg == 'start' and not self.insession:
				self.insession = True
				self.word = random.choice(WORDS).lower()
				self.guessword = ''
				self.numguesses = 0
				self.guesses = []
				self.guessword = '-' * (len(self.word) - 1)
				await self.bot.say('The word is ' + self.guessword)
			elif self.insession:
				if len(msg) == 1:
					if msg in self.guesses:
						msg_reply = 'You already guessed a(n) "{}".'.format(msg)
						await self.bot.say(msg_reply)
					elif self.word.find(msg) != -1:
						msg_reply = 'The word does contain a(n) "{}\n".'.format(msg)
						for i, letter in enumerate(self.word, start = 1):
							if letter == msg:
								self.guessword = self.guessword[0:i - 1] + msg + self.guessword[i:len(self.guessword)]
						self.guesses.append(msg)
						self.guesses.sort()
						self.numguesses = self.numguesses + 1
						msg_reply += 'Guesses: [%s]\n' % ', '.join(map(str, self.guesses))
						if self.guessword.find('-') == -1:
							msg_reply += 'You won with {} guess(es)!\n'.format(self.numguesses)
							msg_reply += 'The word was {}.'.format(self.word)
							self.insession = False
						else:
							msg_reply += 'The word is {}'.format(self.guessword) 
						await self.bot.say(msg_reply)
					else:
						msg_reply = 'There are no {}\'s\n'.format(msg)
						self.guesses.append(msg)
						self.guesses.sort()
						msg_reply += 'Guesses: [%s]\n' % ', '.join(map(str, self.guesses))
						msg_reply += 'The word is {}.\n'.format(self.guessword)
						await self.bot.say(msg_reply)
				elif msg == 'end':
					msg_reply = 'Ended session.'
					self.insession = False
					msg_reply += 'The word was {}.'.format(self.word)
					await self.bot.say(msg_reply)
				elif msg == self.word:
					await self.bot.say('You won with ' + str(self.numguesses) + ' guess(es)!')
					self.insession = False
				elif msg != self.word:
					self.numguesses = self.numguesses + 1
					await self.bot.say('It\'s not ' + msg)

					   
def setup(bot):
	n = hangman(bot)
	bot.add_cog(n)
