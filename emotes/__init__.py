from .emotes import Emotes

async def setup(bot):
    await bot.add_cog(Emotes())