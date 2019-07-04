from pokerbot import messages
from database import Database
from pokerbot.channel import Channel
import pymongo
import sys


class Request:

    def __init__(self, ctx, *argv):
        """
        Initializes a request
        :param ctx: The context object from the command
        :param argv: Any extra arguments for use in methods
        """
        self.ctx = ctx
        self.args = argv
        self.server_id = self.ctx.message.guild.id

    async def create_table(self):
        """
        Turns the given channel into a poker table
        :rtype: str
        :return: A message regarding the success of the operation
        """
        # Attempts to grab the target channel id from the command parameter, returns an error if failed
        try:
            channel_id = int(self.args[0].strip("<@!#>"))
        except Exception as e:
            print(type(e))
            return messages.newtable.invalidtable

        # Returns an error if the channel id is invalid
        if self.ctx.bot.get_channel(channel_id) is None:
            return messages.newtable.invalidtable

        # Returns an error if the target channel is already a poker table
        if Database("Tables", self.server_id).is_there("channelId", channel_id):
            return messages.newtable.error

        # The default database entry for a new table
        entry = {
            "channelId": channel_id,
            "waitingForPlayers": True,
            "waitingToClose": False,
            "players": {},
            "waitingLine": [],
            "leavingLine": []
        }

        # Adds the new entry to the database
        Database("Tables", self.server_id).new_entry(entry)

        # Sends a success message in the target channel
        await Channel(self.ctx.bot.get_channel(channel_id)).update(messages.newtable.intable)

        # Returns a success message for use in the command channel
        return messages.newtable.success(self.args[0])

    def delete_table(self):
        """
        Flags the given channel as waiting to close
        :rtype: str
        :return: A message regarding the success of the operation
        """
        # Attempts to grab the target channel id from the command parameter, returns an error if failed
        try:
            channel_id = int(self.args[0].strip("<@!#>"))
        except Exception as e:
            print(type(e))
            return messages.newtable.invalidtable

        # Returns an error if the channel id is invalid
        if self.ctx.bot.get_channel(channel_id) is None:
            return messages.newtable.invalidtable

        # Returns an error if the target channel is not a poker table
        if not Database("Tables", self.server_id).is_there("channelId", channel_id):
            return messages.closetable.nottable

        # Flags the table as waiting to close in the database
        Database("Tables", self.server_id).set_value("channelId", channel_id, {"waitingToClose": True})

        # Returns a success message for use in the command channel
        return messages.closetable.success(self.args[0])

    def baltop(self):
        """
        Returns a string with the table featuring the highest balances on the server
        :return: A string with the table featuring the highest balances on the server
        """
        # Connects to Mongo Client and sets the collection to be operated on
        client = pymongo.MongoClient(sys.argv[2], connect=False)
        database = client["Members"]
        collection = database[self.server_id]

        # Creates a list of dicts with balance in descending order
        members = []

        for entry in collection.find().sort("balance", -1):
            members.append(entry)

        # Closes Mongo Client
        client.close()

        # Initializes variables
        max_name_length = 0
        max_rank = 0

        # Finds the number of digits in the number of players and length of longest name
        for member in members:

            max_rank = max_rank + 1
            player_id = member["userId"]
            username = self.ctx.bot.get_guild(self.server_id).get_member(player_id).display_name
            if len(username) >= max_name_length:
                max_name_length = len(username)

        max_rank_length = len(str(max_rank))

        # Formats a heading for return strings
        r = '```Rank  ' + (max_rank_length - 4) * ' ' + 'Display Name  ' + ((max_name_length - 12) * ' ') + 'Balance\n'

        # Adds an entry in the string for each player
        rank = 0

        for member in members:
            balance = member["balance"]
            player_id = member["userId"]
            rank = rank + 1
            username = client.get_guild(self.server_id).get_member(player_id).display_name
            p = str(rank)
            b = str(balance)
            r = r + p + (4 - max_rank_length) * ' ' + (2 + max_rank_length - len(p)) * ' ' + username + (
                        2 + max_name_length - len(username)) * ' ' + (12 - max_name_length) * ' ' + b + '\n'

        return r + '```'
