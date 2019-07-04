# General Messages
info = "Version inDev\n*Coded by Brycen Addison and Austin Xie*"
no_permission = "You don't have permission to perform this command!"
missing_args = "Not enough parameters were given. See the help menu for proper use of this command."
invalid_command = "That command is invalid! See the help menu for a list of commands."
not_at_table = "You can only use this command at a table channel!"
pm_command = "That command cannot be used in private messages!"
server_command = "That command can only be used in private messages!"
invalid_args = "The arguments you specified are invalid!"


# Command Messages
class newtable:
    brief = "Converts a text channel into a poker table."
    help = "Converts a text channel into a poker table. It is highly advised that this channel is not used for anything else for playability of the game. All messages sent into this channel are deleted."
    error = "The channel you selected is already a poker table!"
    invalidtable = "That is not a valid channel! Make sure you use the `#text-channel` form of the channel."

    def success(channelname):
        return "Successfully converted " + channelname + " to a poker table!"

    intable = "This channel is now a poker table! The game will automatically start when two or more players join. Use the `join` command to join the table."


class closetable:
    brief = "Converts a text channel from a poker table and closes the poker table."
    help = "After this command is used, any ongoing rounds of poker will first be finished. Afterwards, a new game will not start, and then messages in the channel will no longer be deleted."
    nottable = "The channel you selected is not a poker table!"
    closed = "This table is now closed and another round will not be played. Messages can now be sent in this channel again."

    def success(channelname):
        return f"Poker table {channelname} will be closed at the end of the ongoing round."


class balance:
    brief = "Shows a user's balance of money."
    help = "Will display the amount of money in a user's possession. This money is gained and lost through the game of poker. All users are initially given a default balance that can be set_value by a server administrator."


class baltop:
    brief = "Shows richest users on the server."
    help = "Displays a list of users and their balances in descending order based on balance."


class player:
    def join(ctx):
        return f"{ctx.message.author.mention} has joined the table and will be put in next round."

    def leave(ctx):
        return f"{ctx.message.author.mention} has left the table and will be taken out at the end of the round."

    def leave2(ctx):
        return f"{ctx.message.author.mention} has left the waiting queue and will not be put in next round."

    def cancelLeave(ctx):
        return f"{ctx.message.author.mention} will no longer be leaving at the end of the round."


class game:
    newhand = "New hand, everyone chipped 5$ into the pot to play in."

    def turn(ctx, uid):
        return f"{ctx.message.guild.get_member(uid).mention}'s turn to bet."
