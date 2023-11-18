
from .wiktionary import Wiktionary

async def setup(bot):
    await bot.add_cog(Wiktionary(bot))