from .leaver import Leaver


async def setup(bot):
    await bot.add_cog(Leaver(bot))