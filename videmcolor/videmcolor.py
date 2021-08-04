import random
from colour import Color as col

from .customconverters import BetterMemberConverter
from redbot.core import checks, commands
from redbot.core.commands import Context

class VidemColor(commands.Cog):
	def __init__(self, bot):
		self.color_cog = color_cog = bot.get_cog('Color')

		if not color_cog:
			raise Exception('Could not load the color cog')

	@checks.bot_has_permissions(embed_links=True)
	@commands.command(name='randomcolor')
	async def randomcolor(self, ctx: Context):
		"""Gets a random color"""
		c = col(rgb=(random.randint(0, 255) / 255, random.randint(0, 255) / 255, random.randint(0, 255) / 255))
		embed, f = await self.color_cog.build_embed(c)
		await ctx.send(file=f, embed=embed)

	@checks.bot_has_permissions(embed_links=True)
	@commands.command(name='mycolor')
	async def mycolor(self, ctx: Context):
		"""Gets the display color of the invoker"""
		c = col(rgb=tuple(v / 255 for v in ctx.author.color.to_rgb()))
		embed, f = await self.color_cog.build_embed(c)
		await ctx.send(file=f, embed=embed)
	
	@checks.bot_has_permissions(embed_links=True)
	@commands.command(name='membercolor')
	async def membercolor(self, ctx: Context, member: BetterMemberConverter):
		"""Gets the display color of the invoker"""
		c = col(rgb=tuple(v / 255 for v in member.color.to_rgb()))
		embed, f = await self.color_cog.build_embed(c)
		await ctx.send(file=f, embed=embed)
	