from .scream import Scream

async def setup(bot):
    await bot.add_cog(Scream(bot))
