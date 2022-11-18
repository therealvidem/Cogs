
from .wiktionary import Wiktionary

def setup(bot):
    bot.add_cog(Wiktionary(bot))