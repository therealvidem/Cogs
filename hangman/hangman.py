import discord
import os
import random
from discord.ext import commands
from .utils import checks
import asyncio

WORD_LIST = open('#!/usr/share/dict/words', 'r')
WORDS = WORD_LIST.readlines()

class hangman:
	def __init__(self, bot):
		self.bot = bot
		self.insession = false
		self.guesses = list()
		self.word = ''
		self.guessword = ''
        
	@commands.command(pass_context=True)
	async def hangman(self, context, message):
		msg = message.content
		if msg == 'start' and not self.insession:
			self.insession = true
			self.word = random.choice(self.words)
			for x in range(0, len(self.word)):
				self.guessword = self.guessword + '_'
		elif len(msg) == 1 and self.insession:
			if self.guesses.index(msg):
				await self.bot.say('You already guessed that.')
			elif self.word.find(msg):
				await self.bot.say('There is a(n) ' + msg)
				for x in range(0, len(self.word)):
					if self.word[x:x] == msg:
						self.guessword[x:x] == msg
				self.guesses.append(msg)
				if not self.guessword.find('_'):
					await self.bot.say('You won!')
					self.insession = true
			else:
				await self.bot.say('There is no ' + msg)
				self.guesses.append(msg)


def setup(bot):
	n = test(bot)
	bot.add_cog(n)
