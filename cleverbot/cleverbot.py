from redbot.core import commands
from redbot.core.bot import Red
import discord
from discord.ext.commands import BadArgument
from discord.ext.commands import cooldown
import asyncio
import random
import cleverbotfree.cbfree

class Cleverbot(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.cb = cleverbotfree.cbfree.Cleverbot()
        self.loaded = False
    
    @commands.command(name='cleverbot')
    @cooldown(1, 5)
    async def cleverbot(self, context: discord.ext.commands.Context, *, msg: str):
        channel: discord.channel.TextChannel = context.channel
        async with channel.typing():
            if not self.loaded:
                try:
                    self.cb.browser.get(self.cb.url)
                    self.loaded = True
                except Exception as e:
                    self.cb.browser.close()
                    await context.send('Could not load cleverbot')
                    print(e)
            if self.loaded:
                try:
                    self.cb.get_form()
                except Exception as e:
                    await context.send('An error occured')
                    print(e)
                self.cb.send_input(msg)
                await context.send(self.cb.get_response())
    
    def cog_unload(self):
        if self.loaded:
            self.cb.browser.close()