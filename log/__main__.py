from time import gmtime, strftime

import discord


def time():
    return strftime("[%m/%d/%y][%H:%M:%S]", gmtime())


def log(obj):
    if isinstance(obj, Exception):
        print(f'{time()}[ERROR] {type(obj).__name__}: {obj}')

    elif isinstance(obj, discord.Message):

        if obj.guild == None:
            location = "[Direct Message]"
        else:
            location = f"[{obj.guild.name}][{obj.channel.name}]"
        print(f"{time()}{location} {obj.author}: {obj.content}")

    elif isinstance(obj, str):
        print(f"{time()}{obj}")

    else:
        print(f'{time()}[ERROR] Attempted to log unrecognized object type: {type(obj).__name__}')


def t():
    return strftime("[%H:%M]", gmtime())
