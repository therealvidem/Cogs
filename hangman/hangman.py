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
		self.guessword = ''
        
	@commands.command(pass_context=True)
	async def hangman(self, context, message):
		msg = message
		if msg == 'start' and not self.insession:
			self.insession = True
			self.word = random.choice(WORDS)
			for x in range(1, len(self.word)):
				self.guessword = self.guessword + '-'
			await self.bot.say('The word is ' + self.guessword)
		elif msg == 'end' and self.insession:
			self.insession = False
			await self.bot.say('Ended session')
			await self.bot.say('The word was ' + self.word)
		elif msg == 'guesses' and self.insession:
			await self.bot.say('[%s]' % ', '.join(map(str, self.guesses)))
		elif len(msg) == 1 and self.insession:
			if msg in self.guesses:
				await self.bot.say('You already guessed that.')
			elif self.word.find(msg) != -1:
				await self.bot.say('There is a(n) ' + msg)
				index = 0
				for letter in self.word:
					index = index + 1
					if letter == msg:
						self.guessword = self.guessword[0:index - 1] + msg + self.guessword[index:len(self.guessword)]
				self.guesses.append(msg)
				if self.guessword.find('-') == -1:
					await self.bot.say('You won!')
					self.insession = False
			else:
				await self.bot.say('There is no ' + msg)
				self.guesses.append(msg)
			await self.bot.say('The word is ' + self.guessword)
		elif msg == self.word and self.insession:
			await self.bot.say('You won!')
			self.insession = False

					   
def setup(bot):
	n = hangman(bot)
	bot.add_cog(n)
