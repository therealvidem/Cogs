import discord
from discord.ext import commands
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

    async def check_server(self, server_id, category):
        server_path = os.path.join(self.path, server_id)
        category_path = os.path.join(server_path, category)
        if not os.path.exists(server_path):
            os.makedirs(server_path)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
        if server_id not in self.data:
            self.data[server_id] = {}
            dataIO.save_json(self.json, self.data)
        if category and category not in self.data[server_id]:
            self.data[server_id][category] = {'emotes': []}
            dataIO.save_json(self.json, self.data)

    async def get_image_from_url(self, server_id, category, link, latest_id):
        category_path = os.path.join(self.path, server_id, category)
        try:
            r = requests.get(link, stream=True)
            if r.status_code == 200:
                with open(os.path.join(category_path, str(latest_id) + '.png'), 'wb') as f:
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
        category_data = self.data[server_id][category]
        for i in range(len(category_data['emotes']) + 1):
            try:
                category_data['emotes'][str(i)]
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
            id = int(id) - 1
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

    async def post_count(self, context, server_id, category):
        original_str = category
        category = category.lower()
        await self.check_server('global', category)
        count = await self.get_count(server_id, category)
        category_data = self.data[server_id][category]
        if (not category_data) or ('allow_servers_with_role' in category_data and not discord.utils.get(context.message.server.roles, name=category_data['allow_servers_with_role'])):
            await self.bot.say('I could not find that category with my future vision!')
            return
        article = 'emotes' if count > 1 else 'emote'
        await self.bot.say('I foresee that {} has {} {}!'.format(original_str, count, article))

    async def get_available_ids(self, server_id, category):
        return [e['id'] for e in self.data[server_id][category]['emotes'].values()]

    async def get_count(self, server_id, category):
        return len(self.data[server_id][category]['emotes'])

    async def add_emote(self, prefix, server_id, member_id, category: str, link: str=None):
        category_data = self.data[server_id][category]
        latest_id = await self.get_latest_id(server_id, category)
        success = await self.get_image_from_url(server_id, category, link, latest_id)
        if success:
            emote_data = {
                'id': latest_id,
                'date_added': str(datetime.now()),
                'creator': member_id,
                'link': link,
                'dir': os.path.join(self.path, server_id, category, str(latest_id) + '.png'),
                'category': category
            }
            category_data['emotes'][str(latest_id)] = emote_data
            dataIO.save_json(self.json, self.data)
            as_command = '{}emotes getserver {} {}' if server_id != 'global' else '{}emotes getglobal {} {}'
            as_command = as_command.format(prefix, category, str(latest_id + 1))
            await self.bot.say('I predict you want to add this emote as {}!'.format(as_command))

    async def remove_emote(self, author, server_id, category, id):
        emote = await self.get_emote(server_id, category, id - 1)
        if emote:
            await self.bot.say("Are you sure you want to remove emote {}? (yes/no)".format(id))
            answer = await self.bot.wait_for_message(timeout=15, author=author)
            if answer is None:
                await self.bot.say('You will say no!')
            elif answer.content.lower().strip() == 'yes':
                category_data = self.data[server_id][category]
                try:
                    os.remove(emote['dir'])
                except:
                    pass
                del category_data['emotes'][str(id - 1)]
                dataIO.save_json(self.json, self.data)
                await self.bot.say('I foresaw your command to remove this emote!')
            else:
                await self.bot.say('You will say no!')
        else:
            await self.bot.say('A terrible forecast has struck upon me; that emote doesn\'t exist, or something went wrong!')

    @commands.group(pass_context=True, name='emotes')
    @commands.cooldown(3, 5)
    async def _emotes(self, context):
        pass

    @_emotes.command(pass_context=True, name='addserver')
    @commands.cooldown(3, 5)
    async def _addserver(self, context, category: str, link: str=None):
        category = category.lower()
        await self.check_server(context.message.server.id, category)
        attachments = context.message.attachments
        if attachments:
            link = attachments[0]['url']
        await self.add_emote(context.prefix, context.message.server.id, context.message.author.id, category, link)

    @_emotes.command(pass_context=True, name='addglobal')
    @commands.cooldown(3, 5)
    async def _addglobal(self, context, category: str, link: str=None):
        category = category.lower()
        await self.check_server('global', category)
        if category not in self.data['global']:
            await self.bot.say('I could not find that category with my future vision!')
            return
        attachments = context.message.attachments
        if attachments:
            link = attachments[0]['url']
        await self.add_emote(context.prefix, 'global', context.message.author.id, category, link)

    @_emotes.command(pass_context=True, name='removeserver')
    @checks.admin()
    async def _removeserver(self, context, category: str, id: int):
        category = category.lower()
        await self.check_server(context.message.server.id, category)
        await self.remove_emote(context.message.author, context.message.server.id, category, id)

    @_emotes.command(pass_context=True, name='removeglobal')
    @checks.is_owner()
    async def _removeglobal(self, context, category: str, id: int):
        category = category.lower()
        await self.check_server('global', category)
        await self.remove_emote(context.message.author, 'global', category, id)

    @_emotes.command(pass_context=True, name='getserver')
    @commands.cooldown(3, 5)
    async def _getserver(self, context, category: str, id: str=None, *args):
        category = category.lower()
        await self.check_server(context.message.server.id, category)
        await self.post_emote(context.message.channel, context.message.server.id, category, id)

    @_emotes.command(pass_context=True, name='getglobal')
    @commands.cooldown(3, 5)
    async def _getglobal(self, context, category: str, id: str=None, *args):
        category = category.lower()
        await self.check_server('global', category)
        category_data = self.data['global'][category]
        if 'allow_servers_with_role' in category_data and not discord.utils.get(context.message.server.roles, name=category_data['allow_servers_with_role']):
            await self.bot.say('I could not find that category with my future vision!')
            return
        await self.post_emote(context.message.channel, 'global', category, id)

    @_emotes.command(pass_context=True, name='getservercount')
    @commands.cooldown(3, 5)
    async def _getservercount(self, context, category: str):
        await self.post_count(context, context.message.server.id, category)

    @_emotes.command(pass_context=True, name='getglobalcount')
    @commands.cooldown(3, 5)
    async def _getglobalcount(self, context, category: str):
        await self.post_count(context, 'global', category)

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