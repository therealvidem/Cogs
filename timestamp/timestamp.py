from dateutil import parser
from dateutil.tz import gettz
from randomtimestamp import randomtimestamp
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
	async def _timestamp(self, ctx: Context, *, dt: Datetime):
		"""Gets the Discord timestamp style of the given datetime"""
		await ctx.send(f'<t:{int(dt.timestamp())}>')
	
	@commands.command(name='timestampraw')
	async def _timestampraw(self, ctx: Context, *, dt: Datetime):
		"""Gets the (raw) Discord timestamp style of the given datetime"""
		await ctx.send(f'\\<t:{int(dt.timestamp())}\\>')
	
	@commands.command(name='timestamprandom')
	async def _timestamprandom(self, ctx: Context):
		"""Returns a random datetime in Discord timestamp style"""
		dt = randomtimestamp(end_year=292277026596)
		await ctx.send(f'<t:{int(dt.timestamp())}>')
	
	@commands.command(name='timestamprandomraw')
	async def _timestamprandomraw(self, ctx: Context):
		"""Returns a random datetime in (raw) Discord timestamp style"""
		dt = randomtimestamp(end_year=292277026596)
		await ctx.send(f'\\<t:{int(dt.timestamp())}\\>')
