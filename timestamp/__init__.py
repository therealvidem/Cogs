from .timestamp import TimestampCog

async def setup(bot):
	await bot.add_cog(TimestampCog(bot))