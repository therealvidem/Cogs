from .cleverbot import CleverbotCog

def setup(bot):
    cog = CleverbotCog(bot)
    bot.add_listener(cog.on_message, 'on_message')
    bot.add_cog(cog)