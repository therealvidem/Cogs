from .videmcolor import VidemColor

async def setup(bot):
	await bot.add_cog(VidemColor(bot))