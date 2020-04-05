from redbot.core import commands
from redbot.core.bot import Red
import discord
from discord.ext.commands import BadArgument
from discord.ext.commands import cooldown
from discord.ext.commands import Context
from discord.message import Message
from discord.utils import escape_markdown
import asyncio
import random
import time
from typing import Dict
from cleverbotfree.cbfree import Cleverbot

class CleverbotCog(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.instances: Dict[int, Cleverbot] = {}
        self.cooldowns = {}
        self.bot.cbcooldowns = self.cooldowns
    
    async def get_cleverbot_response(self, content: str, author_id: int) -> str:
        if author_id not in self.instances:
            self.instances[author_id] = Cleverbot()
            cb = self.instances[author_id]
            try:
                cb.browser.get(cb.url)
            except Exception as e:
                cb.browser.close()
                self.instances[author_id] = None
                print(e)
                return 'Could not load cleverbot'
        
        if author_id in self.instances:
            cb = self.instances[author_id]
            try:
                cb.get_form()
            except Exception as e:
                print(e)
                return 'An error occured'
            cb.send_input(content)
            return cb.get_response()
    
    @commands.command(name='cleverbot')
    @cooldown(1, 5)
    async def cleverbot(self, context: Context):
        clean_content: str = context.message.clean_content
        if len(clean_content) > len(context.prefix + " "):
            clean_content = clean_content[len(context.prefix) + 1:]
            
            async with context.typing():
                response = await self.get_cleverbot_response(clean_content, context.author.id)
                if response:
                    await context.send(response)
    
    async def on_message(self, message: Message):
        author_id: int = message.author.id
        bot_id: int = self.bot.user.id
        if author_id != bot_id:
            content: str = message.content
            text: str = ''
            
            name_mention = f'<@{bot_id}>'
            nick_mention = f'<@!{bot_id}>'
            if content.startswith(name_mention):
                text = message.content.replace(name_mention, '', 1).strip()
            elif content.startswith(nick_mention):
                text = message.content.replace(nick_mention, '', 1).strip()
            else:
                return
            
            now = time.time()

            if author_id not in self.cooldowns:
                self.cooldowns[author_id] = {
                    'cooldown_off_time': now,
                    'responding': False
                }

            author_cooldown = self.cooldowns[author_id]
            if author_cooldown['responding'] or author_cooldown['cooldown_off_time'] > now:
                await message.channel.send('You must wait before talking with me again')
            else:
                author_cooldown['responding'] = True
                author_cooldown['cooldown_off_time'] = now + 5

                async with message.channel.typing():
                    response = await self.get_cleverbot_response(text, message.author.id)
                    if response:
                        author_cooldown['responding'] = False
                        await message.channel.send(response)
    
    def cog_unload(self):
        for member_id in self.instances:
            self.instances[member_id].browser.close()
        self.instances.clear()