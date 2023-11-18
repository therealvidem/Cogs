from .rate import Rate

async def setup(bot):
    await bot.add_cog(Rate(bot))