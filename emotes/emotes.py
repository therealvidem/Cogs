import discord
from discord.ext import commands
from discord.utils import find
from .utils import checks
from .utils.dataIO import dataIO
from enum import Enum
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
        self.json = self.path + '/data.json'
        self.data = dataIO.load_json(self.json)

    async def check_server(self, context, category):
        server = context.message.server
        server_path = '{}/{}'.format(self.path, server.id)
        category_path = '{}/{}'.format(server_path, category)
        if not os.path.exists(server_path):
            os.makedirs(server_path)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
        if server.id not in self.data:
            self.data[server.id] = {}
            dataIO.save_json(self.json, self.data)
        if category not in self.data[server.id]:
            self.data[server.id][category] = {'count': 0, 'emotes': []}
            dataIO.save_json(self.json, self.data)

    async def get_image_from_url(self, server_id, category, link, latest_id):
        category_path = '{}/{}/{}'.format(self.path, server_id, category)
        try:
            r = requests.get(link, stream=True)
            if r.status_code == 200:
                with open('{}/{}.png'.format(category_path, latest_id), 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    return True
        except:
            await self.bot.say('An error occured while trying to fetch the image. Try using a different link?')
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
        return [e for e in category_data['emotes'] if e['id'] == id]

    async def get_latest_id(self, server_id, category):
        category_data = self.data[server_id][category]
        count = 1
        for emote in category_data['emotes']:
            if emote['id'] != count:
                return count
            count = count + 1
        return count

    async def get_available_ids(self, server_id, category):
        category_data = self.data[server_id][category]
        return [e['id'] for e in category_data['emotes']]

    @commands.group(pass_context=True, name='emotes')
    @commands.cooldown(3, 5)
    async def _emotes(self, context):
        pass

    @_emotes.command(pass_context=True, name='add')
    @commands.cooldown(3, 5)
    async def _add(self, context, category: str, link: str=None):
        await self.check_server(context, category)
        attachments = context.message.attachments
        if attachments:
            link = attachments[0]['url']
        server = context.message.server
        member = context.message.author
        category_data = self.data[server.id][category]
        latest_id = await self.get_latest_id(server.id, category)
        success = await self.get_image_from_url(server.id, category, link, latest_id)
        if success:
            emote_data = {
                'id': latest_id,
                'date_added': str(datetime.now()),
                'creator': member.id,
                'link': link,
                'dir': '{}/{}/{}/{}.png'.format(self.path, server.id, category, latest_id),
                'category': category
            }
            category_data['emotes'].append(emote_data)
            category_data['count'] += 1
            dataIO.save_json(self.json, self.data)
            await self.bot.say('Successfully added emote as {}emotes get {} {}.'.format(context.prefix, category, str(latest_id)))

    @_emotes.command(pass_context=True, name='remove')
    @checks.admin()
    async def _remove(self, context, category: str, id: int):
        await self.check_server(context, category)
        server = context.message.server
        member = context.message.author
        emote = await self.get_emote(server.id, category, id)
        if emote:
            emote = emote[0]
            category_data = self.data[server.id][category]
            os.remove(emote['dir'])
            category_data['emotes'].remove(emote)
            category_data['count'] -= 1
            dataIO.save_json(self.json, self.data)
            await self.bot.say('Successfully removed emote.')
        else:
            await self.bot.say('That emote doesn\'t exist in this category.')

    @_emotes.command(pass_context=True, name='get')
    @commands.cooldown(3, 5)
    async def _get(self, context, category: str, id, *args):
        await self.check_server(context, category)
        server = context.message.server
        channel = context.message.channel
        category_data = self.data[server.id][category]
        try:
            id = int(id)
        except ValueError:
            id = random.randint(1, category_data['count'] + 1)
        available_ids = await self.get_available_ids(server.id, category)
        if id not in available_ids:
            try:
                id = random.choice(available_ids)
            except:
                await self.bot.say('Either I could not find that emote, or there are no emotes in that category.')
                return
        emote = await self.get_emote(server.id, category, id)
        if emote:
            emote = emote[0]
            try:
                await self.bot.send_file(channel, emote['dir'])
            except:
                await self.bot.say(emote['link'])
            except:
                await self.bot.say('An error occured while trying to send image.')
        else:
            await self.bot.say('Either I could not find that emote, or there are no emotes in that category.')

def check_folder():
    f = 'data/emotes'
    if not os.path.exists(f):
        os.makedirs(f)

def check_files():
    f = 'data/emotes/data.json'
    if not dataIO.is_valid_json(f):
        dataIO.save_json(f, {})

def setup(bot):
    check_folder()
    check_files()
    bot.add_cog(Emotes(bot))