from discord.ext import commands
from cogs.utils import checks
from .utils.dataIO import dataIO
import os
import requests
import json

API_URL = "https://cleverbot.io/1.0/"

class Cleverbot:
    def __init__(self, user, key, nick=None):
        self.user = user
        self.key = key
        self.nick = nick

        body = {
            'user': user,
            'key': key,
            'nick': nick
        }

        requests.post('https://cleverbot.io/1.0/create', json=body)

    def query(self, text):
        body = {
            'user': self.user,
            'key': self.key,
            'nick': self.nick,
            'text': text
        }

        r = requests.post('https://cleverbot.io/1.0/ask', json=body)
        r = json.loads(r.text)

        if r['status'] == 'success':
            return r['response']
        else:
            return False

class CleverbotError(Exception):
    pass

class NoCredentials(CleverbotError):
    pass


class CleverbotCog:
    """Cleverbot"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json("data/cleverbot/settings.json")
        self.instances = {}

    @commands.group(no_pm=True, invoke_without_command=True, pass_context=True)
    async def cleverbot(self, ctx, *, message):
        """Talk with cleverbot"""
        author = ctx.message.author
        channel = ctx.message.channel
        try:
            result = await self.get_response(author, message)
        except NoCredentials:
            await self.bot.send_message(channel, "The owner needs to set the credentials first.\n"
                                                 "See: `[p]cleverbot apikey`")
        else:
            await self.bot.say(result)

    @cleverbot.command()
    @checks.is_owner()
    async def toggle(self):
        """Toggles reply on mention"""
        self.settings["TOGGLE"] = not self.settings["TOGGLE"]
        if self.settings["TOGGLE"]:
            await self.bot.say("I will reply on mention.")
        else:
            await self.bot.say("I won't reply on mention anymore.")
        dataIO.save_json("data/cleverbot/settings.json", self.settings)

    @cleverbot.command()
    @checks.is_owner()
    async def apikey(self, user: str, key: str):
        self.settings["cleverbot_user"] = user
        self.settings["cleverbot_key"] = key
        self.settings.pop("key", None)
        self.settings.pop("user", None)
        dataIO.save_json("data/cleverbot/settings.json", self.settings)
        await self.bot.say("Credentials set.")

    async def get_response(self, author, text):
        user, key = self.get_credentials()
        if author.id not in self.instances:
            self.instances[author.id] = Cleverbot(user, key, self.bot.user.id + author.id)
        return self.instances[author.id].query(text)

    def get_credentials(self):
        try:
            return (self.settings["cleverbot_user"], self.settings["cleverbot_key"])
        except KeyError:
            raise NoCredentials()

    async def on_message(self, message):
        if not self.settings["TOGGLE"] or message.server is None:
            return

        if not self.bot.user_allowed(message):
            return

        author = message.author
        channel = message.channel

        if message.author.id == self.bot.user.id:
            return

        content = message.content

        # I can't just .replace the .mention for a dumb mobile-only bug
        # related to nicknames
        name_mention = "<@{}>".format(self.bot.user.id)
        nick_mention = "<@!{}>".format(self.bot.user.id)

        if content.startswith(name_mention):
            text = message.content.replace(name_mention, "", 1).strip()
        elif content.startswith(nick_mention):
            text = message.content.replace(nick_mention, "", 1).strip()
        else:
            return

        await self.bot.send_typing(channel)
        
        try:
            response = await self.get_response(author, text)
        except NoCredentials:
            await self.bot.send_message(channel, "The owner needs to set the credentials first.\n"
                                                 "See: `[p]cleverbot apikey`")
        else:
            await self.bot.send_message(channel, response)


def check_folders():
    if not os.path.exists("data/cleverbot"):
        print("Creating data/cleverbot folder...")
        os.makedirs("data/cleverbot")


def check_files():
    f = "data/cleverbot/settings.json"
    data = {"TOGGLE" : True}
    if not dataIO.is_valid_json(f):
        dataIO.save_json(f, data)


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(CleverbotCog(bot))
