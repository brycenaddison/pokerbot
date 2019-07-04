from pokerbot.channel import Channel
from pokerbot.ErrorHandler import Errors
from discord.ext import commands


class PmCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # verifies for private message
    def cog_check(self, ctx):
        if ctx.message.guild is None:
            return True
        else:
            if Channel(ctx).is_table():
                raise Errors.Ignore()
            else:
                raise Errors.PmCommandError()


def setup(bot):
    bot.add_cog(PmCommands(bot))
