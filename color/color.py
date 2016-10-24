import urllib.request
import xmltodict

class color:
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(pass_context=True)
	async def hexcolor(self, context, colr):
        	file = urllib2.urlopen('https://www.goodreads.com/review/list/20990068.xml?key=nGvCqaQ6tn9w4HNpW8kquw&v=2&shelf=toread')
        	data = file.read()
        	file.close()
        	data = xmltodict.parse(data)
        	table = render_to_response('my_template.html', {'data': data})
        	img = table['colors']['color']['imageUrl']
        	await self.bot.say(img)

def setup(bot):
	n = color(bot)
	bot.add_cog(n)
