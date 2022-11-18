from discord import Embed
from wiktionaryparser import WiktionaryParser

from redbot.core import commands
from redbot.core.commands import Context

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
		word_data = results[0]
		em = Embed(
			title=f'**{word}**',
			description=', '.join(word_data['pronunciation']['text']) if 'pronunciation' in word_data else '',
			url=f'https://en.wiktionary.org/wiki/${word}'
		)
		for i in range(len(word_data['definitions'])):
			em.add_field(name=f'Definition {i}', value=word_data['definitions'][i])
		if 'etymology' in word_data:
			em.add_field(name='Etymology', value=word_data['etymology'])
		await ctx.send(embed=em)
