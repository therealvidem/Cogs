from redbot.core import commands
from redbot.core.bot import Red
import discord
from discord.ext.commands import BadArgument
from discord.ext.commands import cooldown
import asyncio
import random
from typing import Dict
import cleverbotfree.cbfree

class Cleverbot(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.instances: Dict[int, cleverbotfree.cbfree.Cleverbot] = {}
    
    @commands.command(name='cleverbot')
    @cooldown(1, 5)
    async def cleverbot(self, context: discord.ext.commands.Context, *, msg: str):
        if len(msg) > 0:
            author_id: int = context.author.id
            
            async with context.typing():
                if author_id not in self.instances:
                    self.instances[author_id] = cleverbotfree.cbfree.Cleverbot()
                    cb = self.instances[author_id]
                    try:
                        cb.browser.get(cb.url)
                    except Exception as e:
                        cb.browser.close()
                        self.instances[author_id] = None
                        await context.send('Could not load cleverbot')
                        print(e)
                        
                if author_id in self.instances:
                    cb = self.instances[author_id]
                    try:
                        cb.get_form()
                    except Exception as e:
                        await context.send('An error occured')
                        print(e)
                    cb.send_input(msg)
                    await context.send(cb.get_response())
    
    def cog_unload(self):
        for member_id in self.instances:
            self.instances[member_id].browser.close()
        self.instances.clear()