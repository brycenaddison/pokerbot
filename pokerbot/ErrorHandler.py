import sys
import traceback
from pokerbot import messages
from pokerbot.channel import Channel
from discord.ext import commands
from log import log


# custom instances of errors
class Errors:
    class ServerCommandError(commands.CommandError):
        def __init__(self):
            pass

    class TableCommandError(commands.CommandError):
        def __init__(self):
            pass

    class PmCommandError(commands.CommandError):
        def __init__(self):
            pass

    class Ignore(commands.CommandError):
        def __init__(self):
            pass


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):

        # Prevent errors from being sent in table channel
        if Channel(ctx).is_table():
            return

        # MissingRequiredArgument
        if isinstance(e, commands.MissingRequiredArgument):
            return await ctx.send(messages.missing_args)

        # CommandNotFound
        elif isinstance(e, commands.CommandNotFound):
            return await ctx.send(messages.invalid_command)

        # DisabledCommand
        elif isinstance(e, commands.DisabledCommand):
            return await ctx.send(f'{ctx.command} has been disabled.')

        # NoPrivateMessage
        elif isinstance(e, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(messages.pm_command)
            except Exception as e:
                print(type(e))
                pass

        # BadArgument
        elif isinstance(e, commands.BadArgument):
            return await ctx.send(messages.invalid_args)

        # TableCommandError
        elif isinstance(e, Errors.TableCommandError):
            return await ctx.send(messages.not_at_table)

        # ServerCommandError
        elif isinstance(e, Errors.ServerCommandError):
            return

        # PmCommandError
        elif isinstance(e, Errors.PmCommandError):
            return await ctx.send(messages.server_command)

        # Ignore
        elif isinstance(e, Errors.Ignore):
            return

        # unrecognized error
        else:
            log("[ERROR] Unrecognized command error encountered:")
            log(e)
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
