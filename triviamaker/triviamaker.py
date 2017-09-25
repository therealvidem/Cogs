import discord
from discord.ext import commands

class triviamaker:
    def __init__(self, bot):
        self.bot = bot
        self.trivias = {}
        
    @commands.group(pass_context=True)
    async def tm(self, ctx):
        pass
        
    @tm.command(pass_context=True)
    async def new(self, ctx):
        self.trivias[ctx.message.author.id] = {}
        await self.bot.say('Successfully reset the trivia.')
        
    @tm.command(pass_context=True)
    async def set(self, ctx, question, answer=None):
        try:
            if answer:
                answer = answer.replace(answer, '`', '')
                self.trivias[ctx.message.author.id][question] = answer
            else:
                del self.trivias[ctx.message.author.id][question]
        except KeyError:
            await self.bot.say('Do "{}tm new" to create a new trivia.'.format(self.bot.prefix))
        
    @tm.command(pass_context=True)
    async def save(self, ctx, name):
        try:
            self.trivias[ctx.message.author.id]
        except KeyError:
            await self.bot.say('Do "{}tm new" to create a new trivia.'.format(self.bot.prefix))
            return
        with open('data/trivia/{}.txt'.format(name), 'w+') as f:
            for question,answer in self.trivias[ctx.message.author.id].items():
                f.write('{} `{}'.format(question, answer))
        await self.bot.say('Successfully uploaded {} for trivia'.format(name))
    
def check_folders():
    if not os.path.exists('data/triviamaker'):
        os.makedirs('data/triviamaker')
    
def setup(bot):
    check_folders()
    bot.add_cog(triviamaker(bot))
