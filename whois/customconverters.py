from discord.ext.commands import MemberConverter
import re

async def get_member_named(bot, guild, name):
    result = None
    if len(name) > 5 and name[-5] == '#':
        member_names = {m.name.lower(): m for m in bot.members}
        # The 5 length is checking to see if #0000 is in the string,
        # as a#0000 has a length of 6, the minimum for a potential
        # discriminator lookup.
        potential_discriminator = name[-4:]

        # do the actual lookup and return if found
        # if it isn't found then we'll do a full name lookup below.
        actual_name = name[:-5]
        if actual_name in member_names and member_names[actual_name].discriminator == potential_discriminator:
           result = member_names[actual_name]
        if result is not None:
            return result

    # def pred(m):
    #     return m.name.lower().find(name.lower()) == 0 or (m.nick is not None and m.nick.lower().find(name.lower()) == 0)

    found_members = await guild.query_members(name, limit=1)
    if len(found_members) > 0:
        return found_members[0]
    else:
        return None

class BetterMemberConverter(MemberConverter):
    async def convert(self, ctx, argument):
        message = ctx.message
        match = self._get_id_match(argument) or re.match(r'<@!?([0-9]+)>$', argument)
        guild = message.guild
        result = None
        if match is None:
            # not a mention...
            if guild:
                result = await get_member_named(ctx.bot, guild, argument)
        else:
            user_id = int(match.group(1))
            if guild:
                result = guild.get_member(user_id)
        
        return result