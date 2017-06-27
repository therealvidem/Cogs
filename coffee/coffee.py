import discord
from discord.ext import commands
from discord.utils import find
from .utils import checks
from .utils.dataIO import dataIO

class Coffee:
    def __init__(self, bot):
        self.bot = bot
        self.coffeedata = dataIO.load_json('data/coffee/coffee.json')
    
    @commands.group(pass_context=True)
    async def coffee(self, context):
        if context.invoked_subcommand is None:
            if context.message.server.id not in self.coffeedata:
                self.coffeedata[context.message.server.id] = {}
            await self.bot.say('Do {}help coffee.'.format(context.prefix)) 

    @coffee.command()
    @checks.admin()
    async def plus(self, member: discord.Member=None):
        if member:
            if member.id not in self.coffee[context.message.server.id]:
                self.coffeedata[context.message.server.id][member.id] = 0
            numcoffee = self.coffeedata[context.message.server.id][member.id] + 1
            self.coffeedata[context.message.server.id][member.id] = numcoffee
            dataIO.save_json('data/coffee/coffee.json', self.coffeedata)
            await self.bot.say('Gave 1 coffee to ' + member.mention + '!')
	
    @coffee.command()
    @checks.admin()
    async def subtract(self, member: discord.Member=None):
        if member:
            if member.id not in self.coffeedata[context.message.server.id]:
                self.coffeedata[context.message.server.id][member.id] = 0
            numcoffee = max(0, self.coffeedata[context.message.server.id][member.id] - 1)
            self.coffeedata[context.message.server.id][member.id] = numcoffee
            dataIO.save_json('data/coffee/coffee.json', self.coffeedata)
            await self.bot.say('Took 1 coffee from ' + member.mention + '!')
			
    @coffee.command()
    @checks.admin()
    async def give(self, member: discord.Member=None, n: int=1):
        if member:
            if member.id not in self.coffeedata[context.message.server.id]:
                self.coffeedata[context.message.server.id][member.id] = 0
            numcoffee = self.coffeedata[context.message.server.id][member.id] + n
            self.coffeedata[context.message.server.id][member.id] = numcoffee
            dataIO.save_json('data/coffee/coffee.json', self.coffeedata)
            await self.bot.say('Gave ' + str(n) + ' coffee to ' + member.mention + '!')
			
    @coffee.command()
    @checks.admin()
    async def set(self, member: discord.Member=None, numcoffee: int=1):
        if member:
            self.coffeedata[context.message.server.id][member.id] = numcoffee
            dataIO.save_json('data/coffee/coffee.json', self.coffeedata)
            await self.bot.say('Set ' + member.mention + '\'s number of coffee to ' + str(numcoffee) + '!')
			
    @coffee.command()
    @checks.admin()
    async def reset(self, member: discord.Member=None):
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
    
    async def reaction_listener(self, reaction, user):
        print(reaction.emoji.name)
        print(user.name)
        if reaction.message.server.id == '310510876514058241' and reaction.emoji == ':ophiuchus:':
            if user == self.bot.user:
                return
            message = reaction.message
            author = message.author
            emoji = reaction.emoji
            if message.id == '329141418444455937':
                if next(r for r in author.roles if r.name == 'Audience') is None:
                    await self.bot.add_roles(author, next(r for r in message.server.roles if r.name == 'Audience'))
                await self.bot.remove_reaction(message, emoji, user)
    
    async def join_listener(self, member):
        await self.bot.send_message(member.server.default_channel, "Welcome {0} to {1}!".format(member.mention, member.server.name))
            
def check_files():
    f = "data/coffee/coffee.json"
    data = {}
    if not dataIO.is_valid_json(f):
        dataIO.save_json(f, data)

def setup(bot):
    check_files()
    n = Coffee(bot)
    bot.add_cog(n)
    bot.add_listener(n.reaction_listener, "on_reaction_add")
    bot.add_listener(n.join_listener, "on_member_join")
