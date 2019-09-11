from redbot.core import commands
from redbot.core import Config
from redbot.core import checks
from redbot.core.data_manager import cog_data_path
from redbot.core.utils.predicates import MessagePredicate
from discord import utils
from discord.ext.commands import cooldown
from discord.role import Role
from discord.file import File
from discord.embeds import Embed
import os
from datetime import datetime
import asyncio
import random
import requests
import shutil

class Emotes(commands.Cog):
    # Note: I *would* use custom groups if I knew how to, but right now the docs are VERY vague on
    # how to actually use custom groups. So, if you see any set_raws, don't blame me :(

    def __init__(self):
        self.path = cog_data_path(self)
        self.config = Config.get_conf(self, identifier=2294513315121518)
        default_global = {
            'categories': {}
        }
        default_guild = {
            'categories': {}
        }
        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)
    
    async def check_folder(self, ctx, is_global: bool, category_name: str):
        if is_global:
            server_path = os.path.join(self.path, 'global')
        else:
            server_path = os.path.join(self.path, str(ctx.guild.id))
        if not os.path.exists(server_path):
            os.mkdir(server_path)
        category_path = os.path.join(server_path, category_name)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
    
    async def remove_folder(self, ctx, is_global: bool, category_name: str):
        if is_global:
            server_path = os.path.join(self.path, 'global')
        else:
            server_path = os.path.join(self.path, str(ctx.guild.id))
        if os.path.exists(server_path):
            category_path = os.path.join(server_path, category_name)
            if os.path.exists(category_path):
                shutil.rmtree(category_path)
    
    async def get_category(self, ctx, is_global: bool, category_name: str):
        if is_global:
            return self.config.categories.get_attr(category_name)
        else:
            return self.config.guild(ctx.guild).categories.get_attr(category_name)

    async def add_category(self, ctx, is_global: bool, category_name: str):
        category_value = await self.get_category(ctx, is_global, category_name)
        category = await category_value()
        if category is None:
            await self.check_folder(ctx, True, category_name)
            if is_global:
                await self.config.categories.set_raw(category_name, value={'emotes': {}})
            else:
                await self.config.guild(ctx.guild).categories.set_raw(category_name, value={'emotes': {}})
            await ctx.send('I foresee your command to add this category!')
        else:
            await ctx.send('I foresee that this category already exists!')
    
    async def list_categories(self, ctx, is_global: bool):
        if is_global:
            categories = await self.config.categories.all()
        else:
            categories = await self.config.guild(ctx.guild).categories.all()
        title_str = 'Global Categories' if is_global else 'Categories in {}'.format(ctx.guild.name)
        new_embed = Embed(title=title_str)
        for category_name in categories:
            new_embed.add_field(name=category_name, value=len(categories[category_name]['emotes']), inline=False)
        await ctx.send(embed=new_embed)
    
    async def remove_category(self, ctx, is_global: bool, category_name: str):
        category_value = await self.get_category(ctx, is_global, category_name)
        category = await category_value()
        if category is not None:
            await ctx.send('Are you sure you want to remove category {}? (yes/no)'.format(category_name))
            pred = MessagePredicate.yes_or_no(ctx)
            await ctx.bot.wait_for('message', check=pred)
            if pred.result is True:
                await self.remove_folder(ctx, is_global, category_name)
                await category_value.clear()
                await ctx.send('I foresee your command to remove this category!')
            else:
                await ctx.send('You will say no!')
        else:
            await ctx.send('I cannot find that category with my future vision!')

    async def get_image_from_url(self, ctx, guild_id: str, category_name: str, link: str, latest_id: int):
        category_path = os.path.join(self.path, guild_id, category_name)
        try:
            r = requests.get(link, stream=True)
            if r.status_code == 200:
                with open(os.path.join(category_path, str(latest_id) + '.png'), 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    return True
        except:
            await ctx.send('Oh no! I cannot foresee into that link! May I suggest using a different one?')
            return False

    async def get_latest_id(self, ctx, category):
        for i in range(len(category['emotes'])):
            try:
                category['emotes'][str(i)]
            except:
                return i
        return 0
    
    async def get_available_ids(self, ctx, category):
        return [i for i in category['emotes']]

    async def post_emote(self, ctx, is_global: bool, category_name: str, str_id: str=None):
        category_value = await self.get_category(ctx, is_global, category_name.lower())
        category = await category_value()
        if category is not None:
            if ('allow_servers_with_role' in category and not utils.get(ctx.guild.roles, name=category['allow_servers_with_role'])):
                await ctx.send('I cannot find that category with my future vision!')
                return
            try:
                str_id = str(int(str_id) - 1)
            except:
                pass
            available_ids = await self.get_available_ids(ctx, category)
            if str_id not in available_ids:
                try:
                    emote = category['emotes'][random.choice(available_ids)]
                except:
                    await ctx.send('Either there are no emotes in that category, or something has interfered with my future vision!')
                    return
            else:
                emote = category['emotes'][str_id] if str_id in category['emotes'] else None
            if emote:
                await ctx.send(file=File(emote['dir']))
            else:
                await ctx.send('Either there are no emotes in that category, or something has interfered with my future vision!')
        else:
            await ctx.send('I cannot find that category with my future vision!')

    async def post_count(self, ctx, is_global: bool, category_name: str):
        category_value = await self.get_category(ctx, is_global, category_name.lower())
        category = await category_value()
        if category is not None:
            category = await category_value()
            if 'allow_servers_with_role' in category and not utils.get(ctx.guild.roles, name=category['allow_servers_with_role']):
                await ctx.send('I cannot find that category with my future vision!')
                return
            count = len(category['emotes'])
            emote_word = 'emotes' if count != 1 else 'emote'
            await ctx.send('I foresee that {} has {} {}!'.format(category_name, count, emote_word))
        else:
            await ctx.send('I cannot find that category with my future vision!')

    async def add_emote(self, ctx, is_global: bool, category_name: str, link: str=None):
        category_name = category_name.lower()
        category_value = await self.get_category(ctx, is_global, category_name)
        async with category_value() as category:
            if category is not None:
                latest_id = await self.get_latest_id(ctx, category)
                guild_id = 'global' if is_global else str(ctx.guild.id)
                success = await self.get_image_from_url(ctx, guild_id, category_name, link, latest_id)
                if success:
                    emote_data = {
                        'id': latest_id,
                        'date_added': str(datetime.now()),
                        'creator': ctx.author.id,
                        'link': link,
                        'dir': os.path.join(self.path, guild_id, category_name, str(latest_id) + '.png'),
                        'category': category_name
                    }
                    category['emotes'][str(latest_id)] = emote_data
                    as_command = '{}emotes getserver {} {}' if is_global else '{}emotes getglobal {} {}'
                    as_command = as_command.format(ctx.prefix, category_name, latest_id + 1)
                    await ctx.send('I predict you want to add this emote as {}!'.format(as_command))
            else:
                await ctx.send('I cannot find that category with my future vision!')

    async def remove_emote(self, ctx, is_global: bool, category_name: str, id: int):
        category_value = await self.get_category(ctx, is_global, category_name.lower())
        async with category_value() as category:
            if category is not None and len(category['emotes']) > 0:
                str_id = str(id - 1)
                if str_id in category['emotes']:
                    await ctx.send('Are you sure you want to remove emote {}? (yes/no)'.format(id))
                    pred = MessagePredicate.yes_or_no(ctx)
                    await ctx.bot.wait_for('message', check=pred)
                    if pred.result is True:
                        try:
                            os.remove(category['emotes'][str_id]['dir'])
                        except:
                            pass
                        del category['emotes'][str_id]
                        await ctx.send('I foresee your command to remove this emote!')
                    else:
                        await ctx.send('You will say no!')
                else:
                    await ctx.send('A terrible forecast has struck upon me; that emote does not exist, or something went wrong!')
            else:
                await ctx.send('I cannot find that category with my future vision!')

    @commands.group(name='emotes')
    @cooldown(3, 5)
    async def _emotes(self, ctx):
        pass
    
    @_emotes.group(name='global')
    async def _global(self, ctx):
        pass
    
    @_emotes.group(name='server')
    async def _server(self, ctx):
        pass

    @_server.command(name='add')
    @cooldown(3, 5)
    async def _addserver(self, ctx, category_name: str, link: str=None):
        attachments = ctx.message.attachments
        if attachments:
            link = attachments[0].url
        await self.add_emote(ctx, False, category_name, link)

    @_global.command(name='add')
    @cooldown(3, 5)
    async def _addglobal(self, ctx, category_name: str, link: str=None):
        attachments = ctx.message.attachments
        if attachments:
            link = attachments[0].url
        await self.add_emote(ctx, True, category_name, link)

    @_server.command(name='remove')
    @checks.admin()
    async def _removeserver(self, ctx, category_name: str, id: int):
        await self.remove_emote(ctx, False, category_name, id)

    @_global.command(name='remove')
    @checks.admin()
    async def _removeglobal(self, ctx, category_name: str, id: int):
        await self.remove_emote(ctx, True, category_name, id)

    @_server.command(name='get')
    @cooldown(3, 5)
    async def _getserver(self, ctx, category_name: str, id: str=None, *args):
        await self.post_emote(ctx, False, category_name, id)

    @_global.command(name='get')
    @cooldown(3, 5)
    async def _getglobal(self, ctx, category_name: str, id: str=None, *args):
        await self.post_emote(ctx, True, category_name, id)
    

    @_server.command(name='getcount')
    @cooldown(3, 5)
    async def _getservercount(self, ctx, category_name: str):
        await self.post_count(ctx, False, category_name)

    @_global.command(name='getcount')
    @cooldown(3, 5)
    async def _getglobalcount(self, ctx, category_name: str):
        await self.post_count(ctx, True, category_name)

    @_server.group(name='category')
    async def _servercategory(self, ctx):
        pass
    
    @_global.group(name='category')
    async def _globalcategory(self, ctx):
        pass
    
    @_servercategory.command(name='list')
    async def _serverlist(self, ctx):
        await self.list_categories(ctx, False)
    
    @_globalcategory.command(name='list')
    async def _globallist(self, ctx):
        await self.list_categories(ctx, True)
    
    @_servercategory.command(name='add')
    @checks.admin()
    async def _addservercategory(self, ctx, category_name: str):
        await self.add_category(ctx, False, category_name)

    @_globalcategory.command(name='add')
    @checks.is_owner()
    async def _addglobalcategory(self, ctx, category_name: str):
        await self.add_category(ctx, True, category_name)
    
    @_servercategory.command(name='remove')
    @checks.admin()
    async def _removeservercategory(self, ctx, category_name: str):
        await self.remove_category(ctx, False, category_name)
    
    @_globalcategory.command(name='remove')
    @checks.is_owner()
    async def _removeglobalcategory(self, ctx, category_name: str):
        await self.remove_category(ctx, True, category_name)
    
    @_global.command(name='setserverrole')
    @checks.is_owner()
    async def _setserverrole(self, ctx, category_name: str, role: Role):
        category_value = await self.get_category(ctx, True, category_name)
        async with category_value() as category:
            if category is not None:
                category['allow_servers_with_role'] = role.name
                await ctx.send('I foresee that you want to set that category\'s server role to {}!'.format(role.name))
            else:
                await ctx.send('I cannot find that category with my future vision!')