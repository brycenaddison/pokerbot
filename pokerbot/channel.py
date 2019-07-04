from pokerbot.database import Database
from pokerbot import game


class Channel:

    def __init__(self, *args):
        """
        Creates an object representing a channel
        :param args: Pass one context object or the server id and the channel id in that order.
        """
        if len(args) == 2:
            self.ctx = None
            self.server_id = args[0]
            self.channel_id = args[1]
        elif len(args) == 1:
            self.ctx = args[0]
            self.server_id = self.ctx.message.guild.id
            self.channel_id = self.ctx.message.channel.id
        else:
            raise TypeError("Improper number of arguments passed. Pass one context object or the server id and the "
                            "channel id in that order.")

    def set(self, data):
        """
        Sets a value for the channel
        :param data: The dict object including the key to be set and the value to set it to
        """
        Database("Tables", self.server_id).set_value("channelId", self.channel_id, data)

    def get(self, key):
        """
        Returns the object at the given key in the database
        :param key: The key of the object to be returned
        :return: The object represented by the key
        """
        return Database("Tables", self.server_id).get_value("channelId", self.channel_id, key)

    def add(self, key, value):
        """
        Adds an entry in the database for the given key and value
        :param key: The key of the entry
        :param value: The value of the entry
        """
        Database("Tables", self.server_id).add_value("channelId", self.channel_id, key, value)

    def remove(self, key, value):
        """
        Removes an entry matching the query from the database
        :param key: The query key
        :param value: The query value
        """
        Database("Tables", self.server_id).remove_value("channelId", self.channel_id, key, value)

    def get_deck(self):
        """
        Returns the current deck order for the table
        :return: The current deck order for the table
        """
        return Database("Tables", self.server_id).get_value("channelId", self.channel_id, "deck")

    def set_deck(self, deck):
        """
        Sets the deck for the table
        :param deck: The deck to set to the table
        """
        Database("Tables", self.server_id).set_value("channelId", self.channel_id, {"deck": deck})

    def add_player(self, player_id, position, hand):
        """
        Adds a player to the table with default values
        :param player_id: The player id of the player to add
        :param position: The position in the betting order for the player
        :param hand: The hand of the player
        """
        self.add("players", {
            "userId": player_id,
            "position": position,
            "hand": hand,
            "folded": False,
            "inPot": 0,
            "takingTurn": False,
            "takenTurn": False
        })

    def is_table(self):
        """
        Returns whether this channel is a table
        :return: A boolean value representing whether the channel is a table
        """
        if Database("Tables", self.server_id).is_there("channelId", self.channel_id):
            return True
        else:
            return False

    async def update(self, message):
        """
        Sends a message in the channel with a timestamp
        :param message: The message to send
        :return: The message sent
        """
        return await self.ctx.send(f"{t()} {message}")

    async def players_left(self):
        """
        Sends a message with the numbers of players left to start the game
        """
        if self.get("waitingForPlayers"):
            n = 2 - len(self.get("waitingLine")) - len(self.get("players"))
            s = ""
            if n != 1:
                s = "s"
            await self.update(f"Waiting for {n} more player{s}...")

    async def check(self):
        """
        Checks if enough players have joined the table, starts game if so
        """
        if self.get("waitingForPlayers") and len(self.get("waitingLine")) >= 2:
            await self.update("2 players have joined the table! Starting a game...")
            await game.startRound(self.ctx)
        else:
            await self.players_left()

    async def add_to_waiting_line(self, player_id=None):
        """
        Adds a player to the waiting line, subsequently checks if enough players are in the waiting line to start game
        :param player_id: The id of the player to add to the waiting line, by default is the one who sent the message
        """
        if player_id is None:
            player_id = self.ctx.message.author.id
        Database("Tables", self.server_id).add_value("channelId", self.channel_id, "waitingLine", player_id)
        await self.check()

    async def add_to_leaving_line(self, player_id=None):
        """
        Adds a player to the leaving line, subsequently sends a message if more players are needed
        :param player_id: The id of the player to add to the leaving line, by default is the one who sent the message
        """
        if player_id is None:
            player_id = self.ctx.message.author.id
        Database("Tables", self.server_id).add_value("channelId", self.channel_id, "leavingLine", player_id)
        await self.players_left()

    async def remove_from_waiting_line(self, player_id=None):
        """
        Removes a player from the waiting line, subsequently sends a message if more players are needed
        :param player_id: The id of the player to remove from the waiting line, by default is the one who sent the
                          message
        """
        if player_id is None:
            player_id = self.ctx.message.author.id
        Database("Tables", self.server_id).remove_value("channelId", self.channel_id, "waitingLine", player_id)
        await self.players_left()

    async def remove_from_leaving_line(self, player_id=None):
        """
        Removes a player from the leaving line, subsequently sends a message if more players are needed
        :param player_id: The id of the player to remove from the leaving line, by default is the one who sent the
                          message
        """
        if player_id is None:
            player_id = self.ctx.message.author.id
        Database("Tables", self.server_id).remove_value("channelId", self.channel_id, "leavingLine", player_id)
        await self.players_left()


