from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot, error):
        self.bot = bot



def setup(bot):
    bot.add_cog(ErrorHandler(bot))