import re
from discord import Embed
from wiktionaryparser import WiktionaryParser

from redbot.core import commands
from redbot.core.commands import Context
from redbot.core.utils import menus

class Wiktionary(commands.Cog):
	def __init__(self, bot):
		self.parser = WiktionaryParser()
		self.parser.set_default_language('english')

	@commands.command(name='define')
	async def define(self, ctx: Context, *, word: str):
		"""Defines a word"""
		if len(word) > 128:
			await ctx.send('Word is too long.')
			return
		results = self.parser.fetch(word)
		if len(results) == 0:
			await ctx.send('No results found.')
			return
		print(results)
		embeds = []
		for word_data in results:
			em = Embed(
				title=f'**{word}**',
				description='\n'.join(word_data['pronunciations']['text']) if 'pronunciations' in word_data and len(word_data['pronunciations']['text']) > 0 else '',
				url=f'https://en.wiktionary.org/wiki/{word}'
			)
			if 'etymology' in word_data and len(word_data['etymology']) > 0:
				em.add_field(name='Etymology', value=word_data['etymology'], inline=False)	
			for i in range(min(3, len(word_data['definitions']))):
				definition_data = word_data['definitions'][i]
				for j in range(min(5, len(definition_data['text']))):
					text: str = definition_data['text'][j]	
					em.add_field(name=f'Definition {i * 3 + j + 1} ({definition_data["partOfSpeech"]})', value=text)
			embeds.append(em)
		await menus.menu(
			ctx,
			pages=embeds,
			controls=menus.DEFAULT_CONTROLS,
		)
