import discord
from discord.ext import commands
from discord.utils import find
from .utils import checks
from .utils.dataIO import dataIO
import os
from datetime import datetime
import asyncio
import random
import requests
import shutil

class Emotes:
    def __init__(self, bot):
        self.bot = bot
        self.path = 'data/emotes'
        self.json = os.path.join(self.path, 'data.json')
        self.data = dataIO.load_json(self.json)

    async def check_server(self, context, category):
        server = context.message.server
        server_path = os.path.join(self.path, server_id)
        category_path = os.path.join(server_path, category)
        if not os.path.exists(server_path):
            os.makedirs(server_path)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
        if server.id not in self.data:
            self.data[server.id] = {}
            dataIO.save_json(self.json, self.data)
        if category and category not in self.data[server.id]:
            self.data[server.id][category] = {'count': 0, 'emotes': []}
            dataIO.save_json(self.json, self.data)

    async def get_image_from_url(self, server_id, category, link, latest_id):
        category_path = os.path.join(self.path, server_id, category)
        try:
            r = requests.get(link, stream=True)
            if r.status_code == 200:
                with open(os.path.join(category_path, latest_id + '.png'), 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    return True
        except:
            await self.bot.say('Oh no! I could not foresee into that link! May I suggest using a different one?')
        return False
        # try:
        #     urllib.request.urlretrieve(link, category_path + '/' + filename)
        #     return filename
        # except:
        #     await self.bot.say('Could not get image.')
        # with urllib.request.urlopen(link) as url:
            
        #     if os.path.basename(file_name):
        #         await self.bot.say('That file name already exists inside the category.')
        #         return
        #     with open(file_name, 'wb') as file:
        #         file.write(url.read())
        #         return f

    async def get_emote(self, server_id, category, id):
        category_data = self.data[server_id][category]
        try:
            emote = category_data['emotes'][str(id)]
        except:
            emote = None
        return emote
        # return [e for e in category_data['emotes'] if e['id'] == id][0]

    async def get_latest_id(self, server_id, category):
        for i in range(len(self.data[server_id][category]['emotes']) + 1):
            try:
                category_data['emotes'][i]
            except:
                return i
        # count = 1
        # for emote in category_data['emotes']:
        #     if emote['id'] != count:
        #         return count
        #     count += 1
        # return count

    async def post_emote(self, channel, server_id, category: str, id: str=None):
        category_data = self.data[server_id][category]
        try:
            id = int(id)
        except:
            pass
        available_ids = await self.get_available_ids(server_id, category)
        if id not in available_ids:
            try:
                emote = random.choice(list(category_data['emotes'].values()))
            except:
                await self.bot.say('Either there are no emotes in that category, or something has subverted my prediction skills!')
                return
        else:
            emote = await self.get_emote(server_id, category, id)
        if emote:
            try:
                await self.bot.send_file(channel, emote['dir'])
            except:
                await self.bot.say(emote['link'])
        else:
            await self.bot.say('Either there are no emotes in that category, or something has subverted my prediction skills!')

    async def get_available_ids(self, server_id, category):
        return [e['id'] for e in self.data[server_id][category]['emotes'].values()]

    async def add_emote(self, server_id, member_id, category: str, link: str=None):
        category_data = self.data[server_id][category]
        latest_id = await self.get_latest_id(server_id, category)
        success = await self.get_image_from_url(server_id, category, link, latest_id)
        if success:
            emote_data = {
                'id': latest_id,
                'date_added': str(datetime.now()),
                'creator': member_id,
                'link': link,
                'dir': os.path.join(self.path, server_id, category, latest_id + '.png'),
                'category': category
            }
            category_data['emotes'][latest_id] = emote_data
            category_data['count'] += 1
            dataIO.save_json(self.json, self.data)
            as_command = '{}emotes getserver {} {}!' if server_id != 'global' else '{}emotes getglobal {} {}!'
            as_command.format(context.prefix, category, str(latest_id))
            await self.bot.say('I predict you want to add this emote as {}!'.format(as_command))

    async def remove_emote(self, server_id, category, id):
        emote = await self.get_emote(server_id, category, id)
        if emote:
            category_data = self.data[server_id][category]
            os.remove(emote['dir'])
            del category_data['emotes'][id]
            category_data['count'] -= 1
            dataIO.save_json(self.json, self.data)
            await self.bot.say('I foresaw your command to remove this emote!')
        else:
            await self.bot.say('A terrible forecast has struck upon me; there was an error!')

    @commands.group(pass_context=True, name='emotes')
    @commands.cooldown(3, 5)
    async def _emotes(self, context):
        pass

    @_emotes.command(pass_context=True, name='addserver')
    @commands.cooldown(3, 5)
    async def _addserver(self, context, category: str, link: str=None):
        await self.check_server(context, category)
        attachments = context.message.attachments
        if attachments:
            link = attachments[0]['url']
        await self.add_emote(context.message.server.id, context.message.author.id, category, link)

    @_emotes.command(pass_context=True, name='addglobal')
    @commands.cooldown(3, 5)
    async def _addglobal(self, context, category: str, link: str=None):
        if category not in self.data['global']:
            await self.bot.say('I could not find that category with my future vision!')
            return
        attachments = context.message.attachments
        if attachments:
            link = attachments[0]['url']
        await self.add_emote('global', context.message.author.id, category, link)

    @_emotes.command(pass_context=True, name='removeserver')
    @checks.admin()
    async def _removeserver(self, context, category: str, id: int):
        await self.check_server(context, category)
        await self.remove_emote(context.message.server.id, category, id)

    @_emotes.command(pass_context=True, name='removeglobal')
    async def _removeglobal(self, context, category: str, id: int):
        if context.message.author.id == '138838298742226944':
            await self.remove_emote('global', category, id)

    @_emotes.command(pass_context=True, name='getserver')
    @commands.cooldown(3, 5)
    async def _getserver(self, context, category: str, id: str=None, *args):
        await self.check_server(context)
        await self.post_emote(context.message.channel, context.message.server.id, category, id)

    @_emotes.command(pass_context=True, name='getglobal')
    @commands.cooldown(3, 5)
    async def _getglobal(self, context, category: str, id: str=None, *args):
        if category not in self.data['global']:
            await self.bot.say('I could not find that category with my future vision!')
            return
        await self.post_emote(context.message.channel, 'global', category, id)

def check_folder():
    f = 'data/emotes'
    if not os.path.exists(f):
        os.makedirs(f)
        os.makedirs(os.path.join(f, 'global'))

def check_files():
    f = 'data/emotes/data.json'
    if not dataIO.is_valid_json(f):
        dataIO.save_json(f, {})

def setup(bot):
    check_folder()
    check_files()
    bot.add_cog(Emotes(bot))