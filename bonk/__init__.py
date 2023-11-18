from .bonk import Bonk

async def setup(bot):
    await bot.add_cog(Bonk(bot))