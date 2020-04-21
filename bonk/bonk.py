from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.data_manager import bundled_data_path
import discord
from discord import Message
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

        self.filesize_limit = 8388608
        self.last_author = None
        self.second_last_author = None
        self.third_last_author = None
    
    def generate_image(self, name: str):
        img = Image.open(self.img_path).convert('RGBA')

        # Draw the rotated text of the name of the person and
        # pastes it into the image
        text_w, text_h = self.font.getsize(name, stroke_width=self.text_outline_size)
        text = Image.new('RGBA', (text_w, text_h), (255, 255, 255, 0))
        draw_text = ImageDraw.Draw(text)
        draw_text.text((0, 0), name, 
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
    
    def can_upload(self, img: BytesIO):
        file_size = img.tell()
        img.seek(0)
        return file_size <= self.filesize_limit

    @commands.command(name='bonk')
    @cooldown(1, 10)
    async def bonk(self, context: Context, *, person_name: str=None):
        name = ''
        if person_name is None:
            if self.second_last_author:
                try:
                    person = self.second_last_author
                    name = person.display_name
                except:
                    pass
        else:
            try:
                person = await BetterMemberConverter().convert(context, person_name)
                name = person.display_name
            except:
                name = person_name
        
        async with context.typing():
            img = self.generate_image(name)
            if self.can_upload(img):
                img_name_ext = f'_{name}.png' if name else '.png'
                f = discord.File(img, f'{self.img_name}{img_name_ext}')
                await context.send(file=f)
    
    async def on_message(self, message: Message):
        self.third_last_author = self.second_last_author
        self.second_last_author = self.last_author
        self.last_author = message.author