from .timestamp import TimestampCog

def setup(bot):
	bot.add_cog(TimestampCog(bot))