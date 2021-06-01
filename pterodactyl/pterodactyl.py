from typing import Dict

import discord
from discord.channel import DMChannel
from discord.member import Member
from discord.message import Message
from pydactyl.client import Client
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.commands.context import Context


class Pterodactyl(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=5846885500913601604)
        default_guild = {
            'panel_url': None,
            'api_key': None,
            'registered': False,
            'aliases': {},
            'whitelist': [],
        }
        self.config.register_guild(**default_guild)
        self.clients: Dict[str, Client] = {}
    
    async def server_permissions_pred(self, ctx: Context):
        return ctx.author.guild_permissions.administrator \
            or ctx.author.id in await self.config.guild(ctx.guild).whitelist()
    
    async def check_guild(self, ctx: Context):
        guild_group = self.config.guild(ctx.guild)
        if ctx.guild.id not in self.clients:
            if await guild_group.registered():
                panel_url = await guild_group.panel_url()
                api_key = await guild_group.api_key()
                self.clients[ctx.guild.id] = Client(url=panel_url, api_key=api_key)
            else:
                await ctx.send(f'This guild is not currently registered. Use `{self.bot.command_prefix}pt register` to register.')
                return False
        return True
    
    @commands.group(name='pt')
    async def _pt(self, _: Context):
        pass
    
    @_pt.command(name='register')
    @commands.admin()
    @commands.guild_only()
    async def _pt_register(self, ctx: Context, panel_url: str):
        if ctx.guild.id in self.clients or await self.config.guild(ctx.guild).registered():
            await ctx.send('This server has already been registered')
            return
        member: Member = ctx.author

        await member.send('Enter your API key here (Note: You have 60 seconds to enter it)')

        def check(m):
            return m.channel.type == discord.ChannelType.private and m.channel.recipient.id == member.id
        
        msg: Message = await self.bot.wait_for('message', check=check, timeout=60)
        api_key = str(msg.content)
        client = Client(url=panel_url, api_key=api_key)
        try:
            client.list_servers()
        except:
            await member.send('Error: That is an invalid API key and panel URL combination')
        else:
            guild_group = self.config.guild(ctx.guild)
            await guild_group.registered.set(True)
            await guild_group.panel_url.set(panel_url)
            await guild_group.api_key.set(api_key)
            self.clients[ctx.guild.id] = client
            await member.send('Successfully entered that API key')
    
    @_pt.group(name='whitelist')
    @commands.admin()
    @commands.guild_only()
    async def _whitelist(self, _: Context):
        pass

    @_whitelist.command(name='add')
    @commands.admin()
    @commands.guild_only()
    async def _whitelist_add(self, ctx: Context, member: Member):
        async with self.config.guild(ctx.guild).whitelist() as whitelist:
            if member.id in whitelist:
                await ctx.send(f'{member.display_name} is already whitelisted')
                return
            whitelist.append(member.id)
    
    @_whitelist.command(name='remove')
    @commands.admin()
    @commands.guild_only()
    async def _whitelist_remove(self, ctx: Context, member: Member):
        async with self.config.guild(ctx.guild).whitelist() as whitelist:
            if member.id not in whitelist:
                await ctx.send(f'{member.display_name} is not whitelisted')
                return
            whitelist.remove(member.id)
    
    @_whitelist.command(name='list')
    @commands.admin()
    @commands.guild_only()
    async def _whitelist_list(self, ctx: Context):
        whitelist = await self.config.guild(ctx.guild).whitelist()
        if len(whitelist) == 0:
            await ctx.send('The whitelist is empty')
        else:
            response = '```\n'
            for user_id in whitelist:
                name = '(name not found)'
                try:
                    user = await self.bot.fetch_user(user_id)
                    name = user.name
                except:
                    pass
                response += f'{name} (id: {user_id})\n'
            response += '```'
            await ctx.send(response)
    
    @_pt.group(name='alias')
    @commands.admin()
    @commands.guild_only()
    async def _alias(self, _: Context):
        pass

    @_alias.command(name='set')
    @commands.admin()
    @commands.guild_only()
    async def _alias_set(self, ctx: Context, server_id: str, alias: str=None):
        async with self.config.guild(ctx.guild).aliases() as aliases:
            if server_id in aliases:
                if alias is None:
                    aliases.pop(alias)
                    await ctx.send(f'Successfully removed the alias for {server_id}')
                else:
                    aliases[alias] = server_id
                    await ctx.send(f'Successfully set {server_id} to the alias {alias}')
            else:
                aliases[alias] = server_id
                await ctx.send(f'Successfully set {server_id} to the alias {alias}')
    
    @_alias.command(name='list')
    @commands.admin()
    @commands.guild_only()
    async def _alias_list(self, ctx: Context):
        aliases = await self.config.guild(ctx.guild).aliases()
        if len(aliases) == 0:
            await ctx.send('There are no aliases')
        else:
            response = '```\n'
            for alias in aliases:
                response += f'{alias} -> {aliases[alias]}\n'
            response += '```'
            await ctx.send(response)
    
    @_pt.command(name='listservers')
    @commands.admin()
    @commands.guild_only()
    async def _pt_listservers(self, ctx: Context):
        if not await self.check_guild(ctx): return
        
        client = self.clients[ctx.guild.id]
        response = '```\n'
        for page in client.list_servers():
            for data in page.data:
                server = data['attributes']
                response += f'{server["name"]} (id: {server["identifier"]})\n'
        response += '```'
        await ctx.send(response)
    
    async def send_power_action(self, ctx: Context, server_id_or_alias: str, action: str):
        if not await self.server_permissions_pred(ctx):
            await ctx.send('You do not have permission to run that command')
            return
        if not await self.check_guild(ctx): return

        aliases = await self.config.guild(ctx.guild).aliases()
        if server_id_or_alias in aliases:
            server_id_or_alias = aliases[server_id_or_alias]

        client = self.clients[ctx.guild.id]
        try:
            client.send_power_action(server_id_or_alias, action)
        except Exception as e:
            await ctx.send('An error has occurred')
            print(e)
        else:
            await ctx.send('Server has successfully been started')

    @_pt.command(name='start')
    @commands.admin()
    @commands.guild_only()
    async def _pt_start(self, ctx: Context, server_id_or_alias: str):
        await self.send_power_action(ctx, server_id_or_alias, 'start')
        
    @_pt.command(name='stop')
    @commands.admin()
    @commands.guild_only()
    async def _pt_stop(self, ctx: Context, server_id_or_alias: str):
        await self.send_power_action(ctx, server_id_or_alias, 'stop')
        
    @_pt.command(name='restart')
    @commands.admin()
    @commands.guild_only()
    async def _pt_restart(self, ctx: Context, server_id_or_alias: str):
        await self.send_power_action(ctx, server_id_or_alias, 'restart')
        
    @_pt.command(name='kill')
    @commands.admin()
    @commands.guild_only()
    async def _pt_kill(self, ctx: Context, server_id_or_alias: str):
        await self.send_power_action(ctx, server_id_or_alias, 'kill')
