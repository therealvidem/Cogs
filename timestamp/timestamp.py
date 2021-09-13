import random

from datetime import datetime
from dateutil import parser
from dateutil.tz import gettz
from redbot.core import commands
from redbot.core.commands import Context, Converter

class Datetime(Converter):
	async def convert(self, _, argument: str):
		return parser.parse(argument, fuzzy=True, tzinfos={
			'PT': gettz('America/Los_Angeles'),
			'CT': gettz('America/Chicago'),
			'ET': gettz('America/Detroit'),
		})

class TimestampCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='timestamp')
	async def timestamp(self, ctx: Context, *, datetime: Datetime):
		"""Gets the Discord timestamp style of the given datetime"""
		await ctx.send(f'<t:{int(datetime.timestamp())}>')
	
	@commands.command(name='timestampraw')
	async def timestampraw(self, ctx: Context, *, datetime: Datetime):
		"""Gets the (raw) Discord timestamp style of the given datetime"""
		await ctx.send(f'\\<t:{int(datetime.timestamp())}\\>')
