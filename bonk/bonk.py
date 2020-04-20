from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.data_manager import bundled_data_path
import discord
from discord.ext.commands import cooldown
from discord.ext.commands import Context
from .customconverters import BetterMemberConverter
import asyncio
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw

class Bonk(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.path = bundled_data_path(self)
        self.img_name = 'hornyjail'
        self.img_path = self.path / f'{self.img_name}.jpeg'
        self.font_path = self.path / 'simply-rounded.ttf'
        self.font = ImageFont.truetype(str(self.font_path), 32)
        self.text_color = (0, 0, 0)
        self.text_outline_color = 'white'
        self.text_outline_size = 5
        self.text_position = (500, 275)
        self.text_rotate = 45
        self.draw_text_size = (400, 400)
        self.filesize_limit = 8388608
    
    def generate_image(self, name: str):
        img = Image.open(self.img_path).convert('RGBA')
        # Draw the rotated text of the name of the person and
        # pastes it into the image
        text = Image.new('RGBA', self.draw_text_size, (255, 255, 255, 0))
        draw_text = ImageDraw.Draw(text)
        text_w, text_h = draw_text.textsize(name, font=self.font, stroke_width=self.text_outline_size)
        draw_text.text(((self.draw_text_size[0] - text_w) / 2, (self.draw_text_size[1] - text_h) / 2), name, 
            fill='black', 
            font=self.font, 
            align='center', 
            stroke_width=self.text_outline_size,
            stroke_fill=self.text_outline_color
        )
        text_rotated = text.rotate(self.text_rotate, expand=1)
        dest_x = max(0, int(self.text_position[0] - text_rotated.size[0] / 2))
        dest_y = max(0, int(self.text_position[1] - text_rotated.size[1] / 2))
        # img.paste(text_rotated, box=(int(self.text_position[0] - self.draw_text_size[0] / 2), int(self.text_position[1] - self.draw_text_size[1] / 2)))
        img.alpha_composite(text_rotated, dest=(dest_x, dest_y))
        # Used this as reference: https://github.com/Flame442/FlameCogs/blob/master/battleship/game.py
        temp = BytesIO()
        temp.name = f'{self.img_name}_{name}.png'
        img.save(temp, 'PNG')
        temp.seek(0)
        return temp

    @commands.command(name='bonk')
    @cooldown(1, 10)
    async def bonk(self, context: Context, *, person_name: str):
        name = ''
        try:
            person = await BetterMemberConverter().convert(context, person_name)
            name = person.display_name
        except:
            name = person_name
        async with context.typing():
            img = self.generate_image(name)
            file_size = img.tell()
            img.seek(0)
            if file_size <= self.filesize_limit:
                f = discord.File(img, f'{self.img_name}_{name}.png')
                await context.send(file=f)