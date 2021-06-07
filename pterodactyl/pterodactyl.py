from enum import Enum, auto
from http import HTTPStatus
from typing import Dict, Union

import discord
from discord.channel import TextChannel
from discord.ext.commands.converter import ColorConverter
from discord.member import Member
from discord.message import Message
from pydactyl.client import PterodactylClient
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.commands.context import Context
from requests.models import HTTPError, Response


class LoggingType(Enum):
    LOG_POWER_ACTION = auto()

status_emojis = {
    'running': '🟢',
    'starting': '🔃',
    'stopping': '🔃',
    'offline': '🔴',
}

def is_status_ok(response: Union[Response, Dict]):
    return isinstance(response, dict) or response.ok or response.status_code == HTTPStatus.NO_CONTENT

def has_server_permissions():
    async def predicate(ctx):
        return ctx.channel.type == discord.ChannelType.text and \
            (ctx.author.guild_permissions.administrator \
            or ctx.author.id in await ctx.cog.config.guild(ctx.guild).whitelist())
    return commands.check(predicate)

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
            'server_embed_info': {},
            'logging': {},
        }
        self.config.register_guild(**default_guild)
        self.pt_instances: Dict[str, PterodactylClient] = {}
    
    async def check_guild(self, ctx: Context):
        guild_group = self.config.guild(ctx.guild)
        if ctx.guild.id not in self.pt_instances:
            if await guild_group.registered():
                panel_url = await guild_group.panel_url()
                api_key = await guild_group.api_key()
                self.pt_instances[ctx.guild.id] = PterodactylClient(url=panel_url, api_key=api_key)
            else:
                await ctx.send(f'This guild is not currently registered')
                return False
        return True
    
    async def get_server_id(self, ctx: Context, server_id_or_alias: str):
        aliases = await self.config.guild(ctx.guild).aliases()
        if server_id_or_alias in aliases:
            return aliases[server_id_or_alias]
        return server_id_or_alias
    
    async def server_exists(self, client: PterodactylClient, server_id: str):
        try:
            response = client.client.get_server(server_id)
        except:
            return False
        else:
            return is_status_ok(response)
    
    @commands.group(name='pt')
    async def _pt(self, _):
        pass
    
    @_pt.command(name='register')
    @commands.admin()
    @commands.guild_only()
    @commands.cooldown(1, 60)
    async def _pt_register(self, ctx: Context, panel_url: str):
        if ctx.guild.id in self.pt_instances or await self.config.guild(ctx.guild).registered():
            await ctx.send('This server has already been registered')
            return
        
        member: Member = ctx.author
        await member.send('Enter your API key here (Note: You have 60 seconds to enter it)')
        def check(m):
            return m.channel.type == discord.ChannelType.private and m.channel.recipient.id == member.id
        msg: Message = await self.bot.wait_for('message', check=check, timeout=60)

        api_key = str(msg.content)
        pt_instance = PterodactylClient(url=panel_url, api_key=api_key)
        try:
            pt_instance.client.list_servers()
        except:
            await member.send('Error: That is an invalid API key and panel URL combination')
        else:
            guild_group = self.config.guild(ctx.guild)
            await guild_group.registered.set(True)
            await guild_group.panel_url.set(panel_url)
            await guild_group.api_key.set(api_key)
            self.pt_instances[ctx.guild.id] = pt_instance
            await member.send('Successfully entered that API key')
    
    @_pt.command(name='unregister')
    @commands.admin()
    @commands.guild_only()
    async def _pt_unregister(self, ctx: Context):
        guild_group = self.config.guild(ctx.guild)
        registered = await guild_group.registered()
        
        if not registered:
            await ctx.send('This server has not yet been registered')
            return
        
        await guild_group.registered.set(False)
        await guild_group.panel_url.set(None)
        await guild_group.api_key.set(None)
        if ctx.guild.id in self.pt_instances:
            del self.pt_instances[ctx.guild.id]
        await ctx.send('Successfully unregistered this server')
    
    @_pt.group(name='whitelist')
    @commands.admin()
    @commands.guild_only()
    async def _whitelist(self, _):
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
    @has_server_permissions()
    async def _alias(self, _):
        pass

    @_alias.command(name='set')
    @has_server_permissions()
    async def _alias_set(self, ctx: Context, alias: str, server_id: str=None):
        async with self.config.guild(ctx.guild).aliases() as aliases:
            if alias in aliases:
                if server_id is None:
                    del aliases[alias]
                    await ctx.send(f"Successfully unbounded the alias from the server '{server_id}'")
                else:
                    aliases[alias] = server_id
                    await ctx.send(f"Successfully bound the alias '{alias}' to the server '{server_id}'")
            else:
                if server_id is None:
                    await ctx.send("That alias is not bound to any server")
                else:
                    aliases[alias] = server_id
                    await ctx.send(f"Successfully bound the alias '{alias}' to the server '{server_id}'")
    
    @_alias.command(name='list')
    @has_server_permissions()
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
    @has_server_permissions()
    @commands.cooldown(1, 5)
    async def _pt_listservers(self, ctx: Context):
        if not await self.check_guild(ctx): return
        
        pt_instance = self.pt_instances[ctx.guild.id]
        response = '```\n'
        for page in pt_instance.client.list_servers():
            for data in page.data:
                server = data['attributes']
                response += f'{server["name"]} (id: {server["identifier"]})\n'
        response += '```'
        await ctx.send(response)
    
    @_pt.group(name='server')
    @commands.guild_only()
    async def _server(self, _):
        pass
    
    async def send_power_action(self, ctx: Context, server_id_or_alias: str, action: str, action_past_participle: str):
        # if not await self.server_permissions_pred(ctx):
        #     await ctx.send('You do not have permission to run that command')
        #     return
        if not await self.check_guild(ctx): return

        server_id = await self.get_server_id(ctx, server_id_or_alias)

        pt_instance = self.pt_instances[ctx.guild.id]
        
        if not await self.server_exists(pt_instance, server_id):
            await ctx.send(f"The server '{server_id_or_alias}' does not exist")
            return
        
        async with self.config.guild(ctx.guild).logging() as logging:
            if LoggingType.LOG_POWER_ACTION in logging and logging[LoggingType.LOG_POWER_ACTION]['server_id'] == server_id:
                destination: TextChannel = logging[LoggingType.LOG_POWER_ACTION]['destination']
                destination.send(f"{ctx.author} has sent the power action '{action}' to the server '{server_id}'")

        try:
            response = pt_instance.client.send_power_action(server_id, action)
        except HTTPError as e:
            if e.response.status_code == HTTPStatus.NOT_FOUND:
                await ctx.send(f"'{server_id_or_alias}' is not a valid server")
            else:
                await ctx.send('An error has occurred')
                print(e)
        except Exception as e:
            await ctx.send('An error has occurred')
            print(e)
        else:
            if is_status_ok(response):
                await ctx.send(f'Server has successfully been {action_past_participle}')
            else:
                await ctx.send(f'Something went wrong while trying to {action} the server')
    
    # def server_exists(self, ctx: Context, server_id: str):
    #     pt_instance = self.pt_instances[ctx.guild.id]
    #     try:
    #         info_response = pt_instance.client.get_server(server_id)
    #     except:
    #         return False
    #     else:
    #         if is_status_ok(info_response):
    #             return True
    #     return False

    @_server.command(name='start')
    @has_server_permissions()
    @commands.cooldown(1, 60)
    async def _server_start(self, ctx: Context, server_id_or_alias: str):
        await self.send_power_action(ctx, server_id_or_alias, 'start', 'started')
        
    @_server.command(name='stop')
    @has_server_permissions()
    @commands.cooldown(1, 60)
    async def _server_stop(self, ctx: Context, server_id_or_alias: str):
        await self.send_power_action(ctx, server_id_or_alias, 'stop', 'stopped')
        
    @_server.command(name='restart')
    @has_server_permissions()
    @commands.cooldown(1, 60)
    async def _server_restart(self, ctx: Context, server_id_or_alias: str):
        await self.send_power_action(ctx, server_id_or_alias, 'restart', 'restarted')
        
    @_server.command(name='kill')
    @has_server_permissions()
    @commands.cooldown(1, 60)
    async def _server_kill(self, ctx: Context, server_id_or_alias: str):
        await self.send_power_action(ctx, server_id_or_alias, 'kill', 'killed')

    @_server.command(name='status')
    @commands.cooldown(1, 5)
    async def _server_status(self, ctx: Context, server_id_or_alias: str):
        if not await self.check_guild(ctx): return

        server_id = await self.get_server_id(ctx, server_id_or_alias)

        pt_instance = self.pt_instances[ctx.guild.id]
        try:
            info_response = pt_instance.client.get_server(server_id)
            util_response = pt_instance.client.get_server_utilization(server_id)
        except HTTPError as e:
            if e.response.status_code == HTTPStatus.NOT_FOUND:
                await ctx.send(f"'{server_id_or_alias}' is not a valid server")
            else:
                await ctx.send('An error has occurred')
                print(e)
        except Exception as e:
            await ctx.send('An error has occurred')
            print(e)
        else:
            # pprint.pprint(util_response)
            if is_status_ok(info_response) and is_status_ok(util_response):
                embed = discord.Embed()
                embed.title = info_response['name']
                embed.color = await self.bot.get_embed_color(ctx)
                embed_info = (await self.config.guild(ctx.guild).server_embed_info()).get(server_id, None)
                if embed_info:
                    if 'color' in embed_info:
                        embed.color = discord.Color(embed_info['color'])
                    if 'image_url' in embed_info:
                        embed.set_thumbnail(url=embed_info['image_url'])
                embed.add_field(
                    name='ID',
                    value=info_response['identifier'],
                    inline=False,
                )
                current_state = util_response['current_state']
                embed.add_field(
                    name='Current State',
                    value=f'{current_state.capitalize()} {status_emojis[current_state]}',
                    inline=False,
                )
                ram_limit_bytes = info_response['limits']['memory'] * 1024 * 1024
                ram_usage_bytes = util_response['resources']['memory_bytes']
                embed.add_field(
                    name='RAM Usage',
                    value=f'{round((ram_usage_bytes / ram_limit_bytes) * 100, 2)}%',
                    inline=True,
                )
                disk_limit_bytes = info_response['limits']['disk'] * 1024 * 1024
                disk_usage_bytes = util_response['resources']['disk_bytes']
                embed.add_field(
                    name='Disk Usage',
                    value=f'{round((disk_usage_bytes / disk_limit_bytes) * 100, 2)}%',
                    inline=True,
                )
                await ctx.send(embed=embed)
    
    @_server.command(name='setembedcolor')
    @has_server_permissions()
    async def _server_setembedcolor(self, ctx: Context, server_id_or_alias: str, color: ColorConverter=None):
        if not await self.check_guild(ctx): return

        server_id = await self.get_server_id(ctx, server_id_or_alias)

        async with self.config.guild(ctx.guild).server_embed_info() as server_embed_info:
            if server_id in server_embed_info:
                embed_info = server_embed_info[server_id]
                if color is None:
                    if 'color' in embed_info:
                        del embed_info['color']
                        await ctx.send(f"Successfully removed the color for '{server_id}'")
                    else:
                        await ctx.send('That server does not have an color')
                else:
                    embed_info['color'] = color.value
                    await ctx.send(f"Successfully set the embed color of '{server_id}' to '{color}'")
            else:
                server_embed_info[server_id] = {
                    'color': color.value
                }
                await ctx.send(f"Successfully set the embed color of '{server_id}' to the color '{color}'")
    
    @_server.command(name='setimage')
    @has_server_permissions()
    async def _server_setimage(self, ctx: Context, server_id_or_alias: str, image_url: str=None):
        if not await self.check_guild(ctx): return

        server_id = await self.get_server_id(ctx, server_id_or_alias)

        async with self.config.guild(ctx.guild).server_embed_info() as server_embed_info:
            if server_id in server_embed_info:
                embed_info: Dict = server_embed_info[server_id]
                if image_url is None:
                    if 'image_url' in embed_info:
                        del embed_info['image_url']
                        await ctx.send(f"Successfully removed the image for '{server_id}'")
                    else:
                        await ctx.send('That server does not have an image')
                else:
                    embed_info['image_url'] = image_url
                    await ctx.send(f"Successfully set the embed image of '{server_id}' to '{image_url}'")
            else:
                server_embed_info[server_id] = {
                    'image_url': image_url
                }
                await ctx.send(f"Successfully set the embed image of '{server_id}' to '{image_url}'")
    
    @_pt.group(name='log')
    @has_server_permissions()
    async def _log(self, _):
        pass
    
    async def toggle_logging(self, ctx: Context, logging_type: LoggingType, server_id_or_alias: str, destination: TextChannel, **logging_info):
        if not await self.check_guild(ctx): return

        server_id = await self.get_server_id(ctx, server_id_or_alias)

        pt_instance = self.pt_instances[ctx.guild.id]
        if not await self.server_exists(pt_instance, server_id):
            await ctx.send(f"The server '{server_id_or_alias}' does not exist")
            return

        async with self.config.guild(ctx.guild).logging() as logging:
            if logging_type in logging:
                del logging[logging_type]
                await ctx.send(f'Disabled logging {logging_type} for {server_id_or_alias} in {destination}')
            else:
                logging[logging_type] = {
                    'server_id': server_id,
                    'destination': destination,
                    **logging_info,
                }
                await ctx.send(f'Enabled logging {logging_type} for {server_id_or_alias} in {destination}')

    @_log.command(name='poweractions')
    @has_server_permissions()
    async def _log_poweractions(self, ctx: Context, server_id_or_alias: str, destination: TextChannel):
        await self.toggle_logging(ctx, LoggingType.LOG_POWER_ACTION, server_id_or_alias, destination)
