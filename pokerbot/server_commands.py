from pokerbot.member import Member
from pokerbot import messages
from pokerbot.request import Request
from pokerbot.ErrorHandler import Errors
from discord.ext import commands


class ServerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # verifies for non-poker guild channel
    def cog_check(self, ctx):
        if ctx.message.guild is None:
            raise commands.NoPrivateMessage
        else:
            if not Channel(ctx).is_table():
                return True
            else:
                raise Errors.ServerCommandError()

    # USER COMMANDS #

    # info command
    @commands.command()
    async def info(self, ctx):
        await ctx.send(messages.info)

    # balance command
    @commands.command(help=messages.balance.help, brief=messages.balance.brief)
    async def bal(self, ctx):
        await ctx.send(Member(ctx, ctx.message.author.id).balance())

    # baltop command
    @commands.command(pass_context=True, help=messages.baltop.help, brief=messages.baltop.brief)
    async def baltop(self, ctx):
        await ctx.send(Request(ctx).baltop())

    # ADMIN COMMANDS #

    # newtable command
    @commands.command(help=messages.newtable.help, brief=messages.newtable.brief)
    async def newtable(self, ctx, channel):
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send(messages.no_permission)
        else:
            r = await Request(ctx, channel).create_table()
            await ctx.send(r)

    # closetable command
    @commands.command(help=messages.closetable.help, brief=messages.closetable.brief)
    async def closetable(self, ctx, channel):
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send(messages.no_permission)
        else:
            r = Request(ctx, channel).delete_table()
            await ctx.send(r)


def setup(bot):
    bot.add_cog(ServerCommands(bot))
