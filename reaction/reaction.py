from redbot.core import commands, Config
import asyncio

class Reaction(commands.Cog):
    def __init__(self):
        self.config = Config.get_conf(self, identifier=2294513185132091514)
        default_global = {
            'start': {},
            'sub': {}
        }
        self.config.register_global(**default_global)
        # self.foreseelist = [
        # 	'foresee',
        # 	'predict',
        # 	'think',
        # 	'anticipate',
        # 	'foretell',
        # 	'prophesy'
        # ]
    
    async def set_function(self, ctx, reaction_type, listen: str, reaction: str=None):
        listeners = self.config.__getattr__(reaction_type)
        if listeners:
            if reaction is not None and len(reaction) > 0:
                listeners[listen] = reaction
                await ctx.send('Successfully set that as a reaction')
            else:
                del listeners[listen]
                await ctx.send('Successfully deleted that reaction')
        else:
            await ctx.send('An error occured')
    
    @commands.group(name='reaction')
    async def reaction(self, ctx):
        pass
    
    @reaction.group(name='sub')
    async def sub(self, ctx):
        pass

    @reaction.group(name='start')
    async def start(self, ctx):
        pass
    
    @sub.command(name='set')
    async def sub_set(self, ctx, listen: str, reaction: str=None):
        await self.set_function(ctx, 'set', listen, reaction)
    
    @start.command(name='set')
    async def start_set(self, ctx, listen: str, reaction: str=None):
        await self.set_function(ctx, 'start', listen, reaction)

    async def listener(self, message):
        if not message.author.bot:
            container = ''
            for k, v in await self.config.start().items():
                if message.content[:len(k)].lower() == k:
                    ok = False
                    if len(message.content) > len(k):
                        if message.content[len(k):len(k) + 1] == ' ':
                            ok = True
                    else:
                        ok = True
                    if ok:
                        # if k == 'i' or k == "i'm" or k == "i've":
                        # 	container = 'I ' + random.choice(self.foreseelist) + ' ' + message.author.name + ' will say, "' + message.content + '"'
                        # 	await asyncio.sleep(random.randint(1, 10))
                        await message.channel.send(v + container)
            for k, v in await self.config.sub().items():
                if message.content.lower().find(k) != -1:
                    await message.channel.send(v)


            """if message.content == 'vcnor FORM THE WEIRD QUARTET!' and self.bot.user.id == '224328344769003520':
                await asyncio.sleep(0.5)
                await self.bot.send_message(message.channel, 'VIDEM!')
            elif message.content == 'VIDEM!' and message.author.id == '224328344769003520' and self.bot.user.id == '276425303276912640':
                await asyncio.sleep(0.5)
                await self.bot.send_message(message.channel, 'CATALINA!')
            elif message.content == 'CATALINA!' and message.author.id == '276425303276912640' and self.bot.user.id == '283325760851410944':
                await asyncio.sleep(0.5)
                await self.bot.send_message(message.channel, 'MADISON!')
            elif message.content == 'MADISON!' and message.author.id == '283325760851410944' and self.bot.user.id == '283327246150926336':
                await asyncio.sleep(0.5)
                await self.bot.send_message(message.channel, 'AND RACHEL!')
            elif message.content == 'AND RACHEL!' and message.author.id == '283327246150926336' and (self.bot.user.id == '224328344769003520' or self.bot.user.id == '276425303276912640' or self.bot.user.id == '283325760851410944'):
                await asyncio.sleep(0.5)
                await self.bot.send_message(message.channel, 'AND WE ARE THE WEIRD QUARTET!')
            elif message.content == 'AND WE ARE THE WEIRD QUARTET!' and message.author.id == '283325760851410944' and self.bot.user.id == '283327246150926336':
                await self.bot.send_message(message.channel, 'AND WE ARE TEH WEIRD QUARTET!')"""
            
    '''async def voicelistener(self, before, after):
        if not message.author.bot:
            if before.voice.voice_channel is None and after.voice.voice_channel:
                channel = [c for c in after.server.channels if c.id == '132586673383931904']
                await asyncio.sleep(random.randint(1, 10))
                await self.bot.send_message(channel[0], 'I ' + random.choice(self.foreseelist) + ' that ' + after.name + ' will join the voice channel.')
            elif before.voice.voice_channel and after.voice.voice_channel is None:
                channel = [c for c in after.server.channels if c.id == '132586673383931904']
                await asyncio.sleep(random.randint(1, 10))
                await self.bot.send_message(channel[0], 'I ' + random.choice(self.foreseelist) + ' that ' + after.name + ' will leave the voice channel.')'''
