import zlib
from datetime import datetime, timezone

import discord
import requests
from redbot.core import checks, commands
from redbot.core.commands.context import Context
from redbot.core.config import Config
from redbot.core.utils import menus

API_URL = 'http://ws.audioscrobbler.com/2.0/'

INVALID_API_KEY_ERROR_CODE = 10
EMBED_COLOR = 0x01f30a
DEFAULT_MAX_RECENT = 15

ordinals = {
    '1': 'st',
    '2': 'nd',
    '3': 'rd',
}
def num_to_ordinal(n):
    global ordinals
    n_str = str(n)
    return f'{n_str}{ordinals[n_str[-1]] if n_str[-1] in ordinals else "th"}'

class LastFM(commands.Cog):
    def __init__(self):
        self.config = Config.get_conf(self, identifier=zlib.crc32(b'videmlastfm'))
        self.config.register_global(
            api_key=None,
            max_recent=DEFAULT_MAX_RECENT,
        )
    
    async def fetch_lastfm(self, ctx: Context, method: str, **kwargs):
        api_key = await self.config.api_key() if 'api_key' not in kwargs else kwargs['api_key']
    
        if not api_key:
            await ctx.send('The API key has not been set.')
            return None

        payload = {
            'api_key': api_key,
            'method': method,
            'format': 'json',
            **kwargs,
        }

        result = requests.get(API_URL, params=payload).json()
        
        if 'error' in result:
            await ctx.send('An error occurred')
            await ctx.bot.on_command_error(ctx, f'{ctx.command.qualified_name} returned error code: {result["error"]}')
            return None
        else:
            return result
    
    @commands.group(name='lastfm')
    async def _lastfm(self, ctx: Context):
        pass

    @_lastfm.command(name='setapikey')
    @commands.cooldown(1, 3)
    @checks.is_owner()
    async def _setapikey(self, ctx: Context, api_key: str):
        '''
        Sets the API key to use for interfacing with LastFM.
        API keys can be created by getting an API account at: https://www.last.fm/api/account/create.
        '''
        if await self.fetch_lastfm(ctx, 'chart.gettopartists', api_key=api_key):
            await self.config.api_key.set(api_key)
            await ctx.send('Successfully set API key')
        else:
            await ctx.send('That API key is invalid.')
    
    @_lastfm.group(name='set')
    async def _set(self, ctx: Context):
        pass

    @_set.command(name='maxrecent')
    async def _set_maxrecent(self, ctx: Context, new_max_recent: int):
        if new_max_recent > 0:
            await ctx.send('The max should be greater than 0.')
            return
        
        await self.config.max_recent.set(new_max_recent)
    
    @_lastfm.command(name='recent')
    @commands.cooldown(1, 3)
    async def _recent(self, ctx: Context, user: str, amount: int=5):
        '''
        Gets the most recent scrobbles of the specified user.
        '''
        max_recent = await self.config.max_recent()
        if amount <= 0 or amount > max_recent:
            await ctx.send(f'That amount is not within the range 1-{max_recent}.')
            return

        if result := await self.fetch_lastfm(ctx, 'user.getrecenttracks', user=user):
            embeds = []

            for i, track in enumerate(result['recenttracks']['track'][:amount]):
                em = discord.Embed(
                    title=track["name"],
                    colour=EMBED_COLOR,
                    url=track["url"],
                )
                em.set_author(name=f'Artist: {track["artist"]["#text"]}')
                em.set_footer(text=f'{num_to_ordinal(i + 1)} of {amount} most recently played tracks for {user}')

                user_lastfm_name = result["recenttracks"]["@attr"]["user"]

                timestamp_string = None
                if 'date' in track:
                    timestamp_string = f'Listened: {discord.utils.format_dt(datetime.fromtimestamp(int(track["date"]["uts"])), "R")}'
                if '@attr' in track and 'nowplaying' in track['@attr']:
                    timestamp_string = 'Now playing'

                em.description = f'Viewing scrobbles for [{user_lastfm_name}](https://www.last.fm/user/{user_lastfm_name})\n{timestamp_string}'
                
                if 'image' in track:
                    # Get the "large" image, which is 3rd in the list of images
                    em.set_image(url=track['image'][2]['#text'])
                
                embeds.append(em)
            
            if len(embeds) > 0:
                await menus.menu(
                    ctx,
                    pages=embeds,
                    controls=menus.DEFAULT_CONTROLS,
                )
            else:
                await ctx.send('That user does not have any recent tracks.')
