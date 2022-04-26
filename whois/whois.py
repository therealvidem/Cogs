from datetime import timezone
import discord
from .customconverters import BetterMemberConverter
from redbot.core import commands

EMBED_COLOR = 0x01f30a

def get_user_profile(member: discord.Member):
    user: discord.User = member._user
    username = str(user)
    color = member.color
    nickname: str = member.nick if member.nick else member.display_name
    creation_date = f'<t:{int(user.created_at.replace(tzinfo=timezone.utc).timestamp())}>'
    joined_date = f'<t:{int(member.joined_at.replace(tzinfo=timezone.utc).timestamp())}>'
    roles = member.roles
    roles_string = ' '.join(reversed(list(role.mention for role in roles if role.id != member.guild.id))) if len(roles) > 0 else 'None'

    embed = discord.Embed()
    embed.title = username
    embed.set_thumbnail(url=user.avatar_url)
    embed.color = color
    embed.add_field(
        name='ID', value=user.id, inline=False
    ).add_field(
        name='Nickname', value=nickname
    ).add_field(
        name='Display Color', value=str(color)
    ).add_field(
        name='Creation Date', value=creation_date, inline=False
    ).add_field(
        name='Joined Date', value=joined_date
    ).add_field(
        name='Roles', value=roles_string, inline=False
    )
    return embed

class WhoIs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='member', aliases=['whois'])
    @commands.cooldown(rate=2, per=5)
    async def _member(self, ctx: commands.Context, member: BetterMemberConverter=None):
        if member:
            await ctx.send(embed=get_user_profile(member))
        else:
            await ctx.send(embed=get_user_profile(ctx.author))
        