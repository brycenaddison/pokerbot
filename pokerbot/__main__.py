from discord.ext import commands
from log import log
from pokerbot.channel import Channel
import sys


if __name__ == "__main__":

    # check arguments
    if len(sys.argv) != 3:
        raise Exception("Improper number of arguments passed. Proper usage: pokerbot [discord bot key] [mongo key]")

    # specify startup cogs
    startup = ["table_commands", "server_commands", "pm_commands"]

    # grab token
    token = sys.argv[1]

    # initialize bot
    log(f"Starting discord bot...")
    bot = commands.Bot(command_prefix='!')

    @bot.event
    async def on_ready():
        log(f"Logged in as: {bot.user} ({bot.user.id})")

    # master message handler
    @bot.event
    async def on_message(msg):
        # logs message in console
        log(msg)

        # processes commands
        await bot.process_commands(msg)

        # delete message if in poker channel
        try:
            server_id = msg.guild.id
            channel = msg.channel.id
            if Channel(server_id, channel).is_table():
                if msg.author != bot.user:
                    await msg.delete()
        except Exception as error:
            log(f"{type(error)}: {error}")

    # load extensions
    for group in startup:
        try:
            bot.load_extension(group)
            log("Loaded group {}".format(group))
        except Exception as e:
            log(f'[ERROR] Failed to load command group {group}:')
            log(e)

    # connects to discord bot
    try:
        bot.run(token)
    except Exception as e:
        log("Error: " + str(e))
