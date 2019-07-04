from pokerbot.player import Player
from pokerbot.channel import Channel
from pokerbot.ErrorHandler import Errors
from discord.ext import commands


class TableCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # verifies for poker channel
    def cog_check(self, ctx):
        if ctx.message.guild is None:
            raise commands.NoPrivateMessage
        else:
            if Channel(ctx).is_table():
                return True
            else:
                raise Errors.TableCommandError()

    @commands.command()
    async def join(self, ctx):
        await Player(ctx).join()

    @commands.command()
    async def refresh(self, ctx):
        await Channel(ctx).check()

    @commands.command()
    async def leave(self, ctx):
        await Player(ctx).leave()


def setup(bot):
    bot.add_cog(TableCommands(bot))
