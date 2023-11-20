import random
from colour import Color as col

from .customconverters import BetterMemberConverter
from redbot.core import checks, commands
from redbot.core.commands import Context

class VidemColor(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.color_cog = color_cog = bot.get_cog('Color')

		if not color_cog:
			raise Exception('Could not load the color cog')
		
	def have_fun_with_pillow_custom(self, rgb, file_name='picture.png'):
        im = Image.new("RGB", (200, 200), rgb)
        f = io.BytesIO()
        im.save(f, format="png")
        f.seek(0)
        file = discord.File(f, filename=file_name)
        return file
	
	async def build_embed_custom(self, co, file_name='picture.png'):
        if isinstance(co, int):
            rgb = self.color_cog.decimal_to_rgb(co)
            r, g, b = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255
            co = col(rgb=(r, g, b))
        else:
            rgb = tuple([int(c * 255) for c in co.rgb])
        file = await self.bot.loop.run_in_executor(None, self.have_fun_with_pillow_custom, rgb, file_name)
        hexa = rgb2hex(co.rgb, force_long=True)
        decimal = self.color_cog.rgb_to_decimal(rgb)
        embed = discord.Embed(
            title=f"Color Embed for: {hexa}", color=int(hexa.replace("#", "0x"), 0)
        )
        embed.add_field(name="Hexadecimal Value:", value=hexa)
        embed.add_field(name="Decimal Value:", value=decimal)
        normal = ", ".join([f"{part:.2f}" for part in co.rgb])
        extended = ", ".join([f"{(part*255):.2f}" for part in co.rgb])
        embed.add_field(name="Red, Green, Blue (RGB) Value: ", value=f"{normal}\n{extended}")
        embed.add_field(name="Hue, Saturation, Luminance (HSL) Value:", value=str(co.hsl))
        embed.set_thumbnail(url=f'attachment://{file_name}')
        return embed, file

	@checks.bot_has_permissions(embed_links=True)
	@commands.command(name='randomcolor')
	async def randomcolor(self, ctx: Context):
		"""Gets a random color"""
		c = col(rgb=(random.randint(0, 255) / 255, random.randint(0, 255) / 255, random.randint(0, 255) / 255))
		embed, f = await self.color_cog.build_embed(c)
		await ctx.send(file=f, embed=embed)

	@checks.bot_has_permissions(embed_links=True)
	@commands.command(name='mycolor')
	async def mycolor(self, ctx: Context):
		"""Gets the display color of the invoker"""
		c = col(rgb=tuple(v / 255 for v in ctx.author.color.to_rgb()))
		embed, f = await self.color_cog.build_embed(c)
		await ctx.send(file=f, embed=embed)
	
	@checks.bot_has_permissions(embed_links=True)
	@commands.command(name='membercolor')
	async def membercolor(self, ctx: Context, member: BetterMemberConverter):
		"""Gets the display color of the invoker"""
		c = col(rgb=tuple(v / 255 for v in member.color.to_rgb()))
		embed, f = await self.color_cog.build_embed(c)
		await ctx.send(file=f, embed=embed)
	
	@checks.bot_has_permissions(embed_links=True)
	@commands.command(name='barcolors')
	async def barcolors(self, ctx: Context):
		"""Gets The BAR colors"""
		colors = {
			'neon_blue': col(rgb=(77 / 255, 77 / 255, 255 / 255)),
			'the_bar_hat_brim': col(rgb=(55 / 255, 55 / 255, 181 / 255)),
			'the_bar_bucket_grip': col(rgb=(128 / 255, 128 / 255, 255 / 255)),
			'white': col(rgb=(255 / 255, 255 / 255, 255 / 255)),
			'roblox': col(rgb=(225 / 255, 34 / 255, 26 / 255)),
			'skype': col(rgb=(0 / 255, 175 / 255, 240 / 255)),
		}
		embeds = []
		files = []
		for color_name, color in colors.items():
			embed, f = await self.build_embed_custom(color, f'{color_name}.png')
			embeds.append(embed)
			files.append(f)
		await ctx.send(files=files, embeds=embeds)
	