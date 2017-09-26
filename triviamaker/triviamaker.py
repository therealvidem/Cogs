import discord
import os
import asyncio
from .utils import chat_formatting as chatformat
from discord.ext import commands

class triviamaker:
    def __init__(self, bot, trivia_cog):
        self.bot = bot
        self.trivias = {}
        self.trivia_cog = trivia_cog
        
    @commands.group(pass_context=True)
    async def tm(self, ctx):
        pass
        
    @tm.command(pass_context=True)
    async def new(self, ctx):
        self.trivias[ctx.message.author.id] = {}
        await self.bot.say('Successfully reset the trivia.')
        
    @tm.command(pass_context=True)
    async def set(self, ctx, question, *answers):
        authorid = ctx.message.author.id
        try:
            if question not in self.trivias[authorid]:
                self.trivias[authorid][question] = []
            if len(answers) > 0:
                for answer in answers:
                    answer = answer.replace('`', '')
                    self.trivias[authorid][question].append(answer)
                await self.bot.say('Successfully set that question to that answer.')
            else:
                del self.trivias[authorid][question]
                await self.bot.say('Successfully removed question.')
        except KeyError:
            await self.bot.say('Do "{}tm new" to create a new trivia.'.format(ctx.prefix))
        
    @tm.command(pass_context=True)
    async def save(self, ctx, name):
        authorid = ctx.message.author.id
        if authorid not in self.trivias:
            await self.bot.say('Do "{}tm new" to create a new trivia.'.format(ctx.prefix))
            return
        with open('data/trivia/{}.txt'.format(name), 'w+') as f:
            for question,answer_list in self.trivias[authorid].items():
                f.write(question)
                for answer in answer_list:
                    f.write('`{}'.format(question, answer))
                f.write('\n')
        await self.bot.say('Successfully uploaded {} for trivia'.format(name))
        
    @tm.command(pass_context=True)
    async def load(self, ctx, name):
        authorid = ctx.message.author.id
        trivia_list = self.trivia_cog.parse_trivia_list(name)
        if trivia_list is None:
            await self.bot.say('That trivia doesn\'t exist.')
            return
        self.trivias[authorid] = {}
        for trivia_line in trivia_list:
            self.trivias[authorid][trivia_line.question] = trivia_line.answers
        await self.bot.say('Successfully loaded trivia "{}"'.format(name))
        
    @tm.command(pass_context=True)
    async def print(self, ctx, name):
        authorid = ctx.message.author.id
        try:
            trivia_list = self.trivia_cog.parse_trivia_list(name)
        except FileNotFoundError:
            await self.bot.say('That trivia doesn\'t exist.')
            return
        print_str = ''
        for trivia_line in trivia_list:
            print_str += '{}: {}\n'.format(trivia_line.question, trivia_line.answers)
        for page in chatformat.pagify(print_str):
            await self.bot.say(chatformat.box(page))
            await asyncio.sleep(2)
    
def check_folders():
    if not os.path.exists('data/triviamaker'):
        os.makedirs('data/triviamaker')
    
def setup(bot):
    trivia_cog = bot.get_cog('Trivia')
    if trivia_cog is None:
        print('Error: Trivia cog is not loaded')
    else:
        check_folders()
        bot.add_cog(triviamaker(bot, trivia_cog))
