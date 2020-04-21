from .bonk import Bonk

def setup(bot):
    cog = Bonk(bot)
    bot.add_listener(cog.on_message, 'on_message')
    bot.add_cog(cog)