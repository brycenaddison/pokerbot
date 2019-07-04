import joker
from pokerbot import messages
from pokerbot.member import Member
from pokerbot.channel import Channel
from pokerbot.player import Player


async def start_round(ctx):
    table = Channel(ctx)
    table.set({
        "waitingForPlayers": False,
        "pot": 0,
        "currentBet": 0,
        "phase": 0,
        "cards": [],
        "deck": joker.new_deck()
    })

    position = 0

    for player in table.get("players"):
        table.remove("players", player)

        player_id = player["userId"]

        hand = []

        card1, deck = joker.draw(table.get_deck())
        card2, deck = joker.draw(deck)
        table.set_deck(deck)
        hand.append(card1)
        hand.append(card2)

        table.add_player(player_id, position, hand)
        position = position + 1

    for player_id in table.get("waitingLine"):
        hand = []

        card1, deck = joker.draw(table.get_deck())
        card2, deck = joker.draw(deck)
        table.set_deck(deck)
        hand.append(card1)
        hand.append(card2)

        table.add_player(player_id, position, hand)

        position = position + 1

        table.remove("waitingLine", player_id)

    table.set({
        "positionTurn": -1,
    })

    await table.update(messages.game.newhand)

    await next_turn(ctx)


async def next_turn(ctx):
    table = Channel(ctx)

    # Grabs list of players
    players = table.get("players")

    # Checks if round needs to be advanced
    '''advanceRound = True
    for player in players:
      if not player["takenTurn"]:
        advanceRound = False
      if not player["inPot"] == (table.functions.get_value(ctx, "pot")/players.len):
        advanceRound = False
    if advanceRound:
      table.functions.set_value(ctx, {"phase": table.functions.get_value(ctx, "phase")+1})
    '''
    # Grabs which player's turn
    positionTurn = table.functions.get(ctx, "positionTurn") + 1

    if positionTurn > len(players):
        positionTurn = 0

    # Grabs community cards
    cards = ""
    for card in table.functions.get(ctx, "cards"):
        cards = cards + card + " "
    cards = cards.rstrip()
    if cards == "":
        cards = "None"

    # Searches for player whose turn it is
    for player in players:
        if positionTurn == player["position"]:

            # Grabs user id
            userId = player["userId"]

            # Sends message in table regarding whose turn it is
            await table.update(ctx, messages.game.turn(ctx, userId))

            # Sets player as taking turn
            player["takingTurn"] = True

            # Grabs table values
            pot = table.functions.get(ctx, "pot")
            currentBet = table.functions.get(ctx, "pot")
            inPot = player["inPot"]
            amountToRaise = currentBet - inPot
            balance = member.functions.get(ctx, userId, "balance")

            # Formats player's hand
            hand = "%s %s" % (player["hand"][0], player["hand"][1])

            # Formats message to send to player
            interface = f"Pot: **${pot}**\nCurrent Bet: **${currentBet}**\nYou've bet: **${inPot}**\nYou need to bet: **${amountToRaise}**\nYour balance: **${balance}**\nHand: **{hand}**\nCommunity Cards: **{cards}**\n"

            if table.functions.get(ctx, "currentBet") == 0:
                interface = interface + "Type `!check` to check the bet.\n"
            else:
                interface = interface + f"Type `!call` to call the bet and add {amountToRaise} to the pot.\n"
            interface = interface + "Or, type `!raise [amount] to raise the bet by a specific amount."

            # Sends player the DM.
            await pl.dm(ctx, userId, interface)

    # Updates values in database
    table.functions.set(ctx, {"players": players})
    table.functions.set(ctx, {"positionTurn": positionTurn})


async def end_round(ctx):
    table = Channel(ctx)
    highest_score = 0
    winning_position = [-1]

    for player in table.get("players"):
        in_pot = player["inPot"]
        member = Member(ctx, player["userId"])
        # Adds 1 to total hands played
        member.set("handsPlayed", member.get("handsPlayed") + 1)

        # Adds amount in pot to total losses
        member.set("totalLosses", member.get("totalLosses") + in_pot)

        # Detracts amount bet from users hand
        member.set("balance", member.get("balance") - in_pot)

        # Finds the position[s] with the winning hand
        hand = player["hand"]
        position = player["position"]
        score = joker.Score(hand, table.get("cards")).get()

        if score > highest_score:
            highest_score = score
            winning_position = [position]
        elif score == highest_score:
            winning_position.append[position]

    # Splits up pot among winners
    winning_amount = table.get("pot") / len(winning_position)

    for player in table.get("players"):
        if player["position"] in winning_position:
            member = Member(ctx, player["userId"])
            # Adds winnings to balance
            member.set("balance", member.get("balance") + winning_amount)
            # Adds winnings to total winnings
            member.set("totalWinnings", member.get("totalWinnings") + winning_amount)
            # Adds 1 to hands won
            member.set("handsWon", member.get("handsWon") + 1)

    # Removes players in leaving queue from table
    for player_id in table.get("leavingLine"):

        if table.get_database().is_there("players", {"userId": player_id}):
            table.remove("players", {"userId": player_id})
            table.remove("leavingLine", player_id)
            await table.update(f"{ctx.message.guild.get_member(player_id).mention} has left the table.")

    # Set waiting for players to true if less than 2 players
    if len(table.get("players")) < 2:
        table.set({
            "waitingForPlayers": True
        })

    # Deletes table if waiting to delete
    if table.get("waitingToClose"):
        await table.update(messages.closetable.closed)
        table.get_database().delete_entry("channelId", ctx.message.channel.id)
