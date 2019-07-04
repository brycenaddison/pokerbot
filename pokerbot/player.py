from pokerbot import messages
from database import Database
from pokerbot.member import Member
from pokerbot.channel import Channel


class Player:

    def __init__(self, ctx):
        """
        Initializes a class for player-related functions
        :param ctx: The context object of the message
        """
        self.ctx = ctx
        self.server_id = self.ctx.message.guild.id
        self.player_id = self.ctx.message.author.id
        self.channel_id = self.ctx.message.channel.id

    def get_balance(self, player_id=None):
        """
        Returns the balance of a given player
        :param player_id: The owner of the balance to return
        :return: The balance of the given player
        """
        if player_id is None:
            player_id = self.player_id
        return Database("Members", self.server_id).get_value("userId", player_id, "balance")

    def set_balance(self, balance, player_id=None):
        """
        Sets the balance of a given player
        :param balance: The number to set the player's balance to
        :param player_id: The target player for the balance change
        """
        if player_id is None:
            player_id = self.player_id
        Database("Members", self.server_id).set_value("userId", player_id, {"balance": balance})

    async def dm(self, message, player_id=None):
        """
        Directly message the given player
        :param message: The message to send the player
        :param player_id: The player to send the message to
        """
        if player_id is None:
            player_id = self.player_id
        player = self.ctx.guild.get_member(player_id)
        if player.dm_channel is not None:
            await player.dm_channel.send(message)
        else:
            await player.create_dm()
            await player.dm_channel.send(message)

    def is_playing(self, player_id=None):
        """
        Returns whether a given player is active in a game
        :rtype: bool
        :param player_id: The target player
        :return: Returns the boolean of whether the target player is active in a game
        """
        if player_id is None:
            player_id = self.player_id
        for player in Database("Tables", self.server_id).get_value("channelId", self.channel_id, "players"):
            if player["userId"] == player_id:
                return True
        return False

    def is_in_waiting_line(self, player_id=None):
        """
        Returns whether a given player is in a waiting line
        :rtype: bool
        :param player_id: The target player
        :return: Returns the boolean of whether the target player is in a waiting line
        """
        if player_id is None:
            player_id = self.player_id
        for pid in Database("Tables", self.server_id).get_value("channelId", self.channel_id, "waitingLine"):
            if pid == player_id:
                return True
        return False

    def is_in_leaving_line(self, player_id=None):
        """
        Returns whether a given player is in a leaving line
        :rtype: bool
        :param player_id: The target player
        :return: Returns the boolean of whether the target player is in a leaving line
        """
        if player_id is None:
            player_id = self.player_id
        for pid in Database("Tables", self.server_id).get_value("channelId", self.channel_id, "leavingLine"):
            if pid == player_id:
                return True
        return False

    async def join(self, player_id=None):
        """
        Attempts to add a player to a waiting line or remove a player from a leaving line
        :param player_id: The target player
        """
        if player_id is None:
            player_id = self.player_id

        # adds player to waiting line if player is not already in waiting line or currently playing
        if not self.is_in_waiting_line(
            player_id=player_id
        ) and not self.is_playing(
            player_id=player_id
        ) and not self.is_in_leaving_line(
            player_id=player_id
        ):
            Member(self.ctx, player_id).new()
            table = Channel(self.ctx)
            await table.update(messages.player.join(self.ctx))
            await table.add_to_waiting_line(player_id=player_id)

        # removes player from leaving line if they are in leaving line
        elif self.is_in_leaving_line(player_id=player_id) and self.is_playing(player_id=player_id):
            table = Channel(self.ctx)
            await table.update(messages.player.cancelLeave(self.ctx))
            await table.remove_from_leaving_line(player_id=player_id)

    async def leave(self, player_id=None):
        """
        Attempts to remove a player from a waiting line or add a player to a leaving line
        :param player_id: The target player
        """
        if player_id is None:
            player_id = self.player_id

        # removes player from waiting line if they are in it
        if self.is_in_waiting_line(player_id=player_id):
            table = Channel(self.ctx)
            await table.update(messages.player.leave2(self.ctx))
            await table.remove_from_waiting_line(player_id=player_id)

        # adds player to leaving line if they aren't in leaving line and are in game
        elif not self.is_in_leaving_line(player_id=player_id) and self.is_playing(player_id=player_id):
            table = Channel(self.ctx)
            await table.update(messages.player.leave(self.ctx))
            await table.add_to_leaving_line(player_id=player_id)


