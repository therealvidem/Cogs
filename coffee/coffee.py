import discord
from discord.ext import commands
from discord.utils import find
from .utils import checks
from .utils.dataIO import dataIO

class Coffee:
    def __init__(self, bot):
        self.bot = bot
        self.coffeedata = dataIO.load_json('data/coffee/coffee.json')
        self.read_me_channel = discord.utils.get(self.bot.get_all_channels(), id='310620886476783616')
        self.read_me_message = self.bot.get_message(self.read_me_channel, '329141418444455937')
        self.reaction_task = bot.loop.create_task(self.check_reaction())

    @commands.group(pass_context=True)
    async def coffee(self, context):
        if context.invoked_subcommand is None:
            if context.message.server.id not in self.coffeedata:
                self.coffeedata[context.message.server.id] = {}
            await self.bot.say('Do {}help coffee.'.format(context.prefix)) 

    @coffee.command(pass_context=True)
    @checks.admin()
    async def plus(self, context, member: discord.Member=None):
        if member:
            if member.id not in self.coffeedata[context.message.server.id]:
                self.coffeedata[context.message.server.id][member.id] = 0
            numcoffee = self.coffeedata[context.message.server.id][member.id] + 1
            self.coffeedata[context.message.server.id][member.id] = numcoffee
            dataIO.save_json('data/coffee/coffee.json', self.coffeedata)
            await self.bot.say('Gave 1 coffee to ' + member.mention + '!')
	
    @coffee.command(pass_context=True)
    @checks.admin()
    async def subtract(self, context, member: discord.Member=None):
        if member:
            if member.id not in self.coffeedata[context.message.server.id]:
                self.coffeedata[context.message.server.id][member.id] = 0
            numcoffee = max(0, self.coffeedata[context.message.server.id][member.id] - 1)
            self.coffeedata[context.message.server.id][member.id] = numcoffee
            dataIO.save_json('data/coffee/coffee.json', self.coffeedata)
            await self.bot.say('Took 1 coffee from ' + member.mention + '!')
			
    @coffee.command(pass_context=True)
    @checks.admin()
    async def give(self, context, member: discord.Member=None, n: int=1):
        if member:
            if member.id not in self.coffeedata[context.message.server.id]:
                self.coffeedata[context.message.server.id][member.id] = 0
            numcoffee = self.coffeedata[context.message.server.id][member.id] + n
            self.coffeedata[context.message.server.id][member.id] = numcoffee
            dataIO.save_json('data/coffee/coffee.json', self.coffeedata)
            await self.bot.say('Gave ' + str(n) + ' coffee to ' + member.mention + '!')
			
    @coffee.command(pass_context=True)
    @checks.admin()
    async def set(self, context, member: discord.Member=None, numcoffee: int=1):
        if member:
            self.coffeedata[context.message.server.id][member.id] = numcoffee
            dataIO.save_json('data/coffee/coffee.json', self.coffeedata)
            await self.bot.say('Set ' + member.mention + '\'s number of coffee to ' + str(numcoffee) + '!')
			
    @coffee.command(pass_context=True)
    @checks.admin()
    async def reset(self, context, member: discord.Member=None):
        if member:
            try:
                self.coffeedata[context.message.server.id].pop(member.id, None)
            except KeyError:
                await self.bot.say('Person doesn\'t exist.')
			
    @coffee.command(pass_context=True)
    async def list(self, context):
        em = discord.Embed(title='Coffee Leaderboard', color=discord.Color.red())
        i = 0
        server = self.coffeedata[context.message.server.id]
        for person in sorted(server, key=server.__getitem__, reverse=True):
            i += 1
            member = find(lambda p: p.id == person, context.message.server.members)
            if member:
                discriminator = member.discriminator
                personname = member.name
                score = server[person]
                coffeetext = 'coffees' if score > 1 else 'coffee'
                em.add_field(name=str(i) + '. ' + personname + '#' + discriminator, value=str(score) + ' ' + coffeetext, inline=False)
        await self.bot.say(embed=em)

    async def wait_for_reaction(self, reaction=None, member=None):
        if self.read_me_channel and self.read_me_message:
            if reaction and user and reaction.message.server.id == '310510876514058241':
                # if member == self.bot.user or member.id == '138838298742226944':
                    # return
                audiencerole = discord.utils.get(message.server.roles, name='Audience')
                message = reaction.message
                emoji = reacton.emoji
                if audiencerole not in member.roles and emoji == '⛎':
                    await self.bot.add_roles(member, audiencerole)
                    await self.bot.send_message(message.server.default_channel, "Welcome {} to {}!".format(member.mention, message.server.name))
                await self.bot.remove_reaction(message, emoji, member)
        else:
            print('Something went wrong when trying to find the channel and message!')

    async def check_reaction(self):
        res = await self.bot.wait_for_reaction('⛎', message=self.read_me_message, check=self.wait_for_reaction)
    
    async def join_listener(self, member):
        channel = discord.utils.get(member.server.channels, id='329153340044738560')
        await self.bot.send_message(channel, '<@138838298742226944>, {} joined the server.'.format(member.name))

    def __unload(self):
        self.wait_for_reaction.cancel()
            
def check_files():
    f = "data/coffee/coffee.json"
    data = {}
    if not dataIO.is_valid_json(f):
        dataIO.save_json(f, data)

def setup(bot):
    check_files()
    n = Coffee(bot)
    bot.add_cog(n)
    bot.add_listener(n.join_listener, "on_member_join")