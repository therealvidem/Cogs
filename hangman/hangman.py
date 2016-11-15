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
						await self.bot.say('You already guessed that.')
						await self.bot.say('The word is ' + self.guessword)
					elif self.word.find(msg) != -1:
						await self.bot.say('The word does contain ' + msg)
						for i, letter in enumerate(self.word, start = 1):
							if letter == msg:
								self.guessword = self.guessword[0:i - 1] + msg + self.guessword[i:len(self.guessword)]
						self.guesses.append(msg)
						self.guesses.sort()
						self.numguesses = self.numguesses + 1
						await self.bot.say('Guesses: [%s]' % ', '.join(map(str, self.guesses)))
						if self.guessword.find('-') == -1:
							await self.bot.say('You won with ' + str(self.numguesses) + ' guess(es)!')
							await self.bot.say('The word was ' + self.word)
							self.insession = False
						else:
							await self.bot.say('The word is ' + self.guessword) 
					else:
						self.guesses.append(msg)
						self.guesses.sort()
						await self.bot.say('There are no ' + msg + '\'s')
						await self.bot.say('Guesses: [%s]' % ', '.join(map(str, self.guesses)))
						await self.bot.say('The word is ' + self.guessword)
				elif msg == 'end':
					self.insession = False
					await self.bot.say('Ended session')
					await self.bot.say('The word was ' + self.word)
				elif msg[0:] == self.word[0:]:
					await self.bot.say('You won with ' + str(self.numguesses) + ' guess(es)!')
					self.insession = False
				elif msg != self.word:
					await self.bot.say('msg: ' + msg)
					await self.bot.say('self.word: ' + self.word)
					self.numguesses = self.numguesses + 1
					await self.bot.say('It\'s not ' + msg)

					   
def setup(bot):
	n = hangman(bot)
	bot.add_cog(n)
