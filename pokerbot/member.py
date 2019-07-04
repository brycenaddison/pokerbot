from database import Database


class Member:

    def __init__(self, ctx, player_id):
        """
        Initializes a member class for adding a new member and checking a members balance
        :param ctx: The context of the message
        :param player_id: The target player id
        """
        self.server_id = ctx.message.guild.id
        self.player_id = player_id
        self.client = ctx.bot
        self.ctx = ctx

    def set(self, key, value):
        Database("Members", self.server_id).set_value("userId", self.player_id, {key: value})

    def get(self, key):
        return Database("Members", self.server_id).get_value("userId", self.player_id, key)

    def new(self):
        """
        Adds a new entry for a player
        """
        entry = {
            "userId": self.player_id,
            "balance": 1000,
            "handsWon": 0,
            "totalWinnings": 0,
            "totalLosses": 0,
            "handsPlayed": 0,
        }

        members = Database("Members", self.server_id)
        if not members.is_there("userId", self.player_id):
            members.new_entry(entry)

    def balance(self):
        """
        Returns a string containing the member's balance
        :rtype: str
        :return: A string containing the member's balance
        """
        name = self.client.get_guild(self.server_id).get_member(self.player_id).display_name

        balance = Database("Members", self.server_id).get_value("userId", self.player_id, "balance")

        return "**" + name + "**'s balance is **$" + str(balance) + "**"



