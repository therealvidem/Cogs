from .lastfm import LastFM

async def setup(bot):
    await bot.add_cog(LastFM())