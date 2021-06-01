from .pterodactyl import Pterodactyl

def setup(bot):
    bot.add_cog(Pterodactyl(bot))