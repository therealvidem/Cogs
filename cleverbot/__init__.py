from .cleverbot import Cleverbot

def setup(bot):
    bot.add_cog(Cleverbot(bot))