from .reaction import Reaction

async def setup(bot):
	n = Reaction()
	bot.add_listener(n.listener, 'on_message')
	'''bot.add_listener(n.voicelistener, "on_voice_state_update")'''
	await bot.add_cog(n)