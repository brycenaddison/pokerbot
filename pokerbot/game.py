import joker
from database import Database
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

        hand = []

        card1, deck = joker.draw(table.get_deck())
        card2, deck = joker.draw(deck)
        table.set_deck(deck)
        hand.append(card1)
        hand.append(card2)

        table.functions.refresh(ctx, playerid, position, hand)
        table.functions.set(ctx, {"pot": table.functions.get(ctx, "pot") + ante})
        position = position + 1

    for playerid in table.functions.get(ctx, "waitingLine"):
        hand = []

        card1, Deck = deck.draw(table.functions.getDeck(ctx))
        card2, Deck = deck.draw(Deck)
        table.functions.setDeck(ctx, Deck)
        hand.append(card1)
        hand.append(card2)

        table.functions.refresh(ctx, playerid, position, hand)

        position = position + 1

        table.functions.remove(ctx, "waitingLine", playerid)

    table.functions.set(ctx, {
        "positionTurn": -1,
    })

    await table.update(ctx, messages.game.newhand)

    await nextTurn(ctx)


async def nextTurn(ctx):
    # Grabs list of players
    players = table.functions.get(ctx, "players")

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


async def endRound(ctx):
    highestScore = 0
    for player in table.functions.get(ctx, "players"):
        playerid = player["userId"]
        inPot = player["inPot"]

        # Adds 1 to total hands played
        member.functions.set(ctx, playerid, "handsPlayed", (member.functions.get(ctx, playerid, "handsPlayed") + 1))

        # Adds amount in pot to total losses
        member.functions.set(ctx, playerid, "totalLosses", (member.functions.get(ctx, playerid, "totalLosses") + inPot))

        # Detracts amount bet from users hand
        member.functions.set(ctx, playerid, "balance", (member.functions.get(ctx, playerid, "balance") - inPot))

        # Finds the position[s] with the winning hand
        hand = player["hand"]
        position = player["position"]
        score = scoring.handEval(hand, table.functions.get(ctx, "cards"))
        if score > highestScore:
            highestScore = score
            winningPosition = [position]
        elif score == highestScore:
            winningPosition.append[position]

        # Splits up pot among winners
        winningAmount = table.functions.get(ctx, "pot") / len(winningPosition)

        for player in table.functions.get(ctx, "players"):
            if player["position"] == position:
                # Adds winnings to balance
                member.functions.set(ctx, playerid, "balance",
                                     (member.functions.get(ctx, playerid, "balance") + winningAmount))
                # Adds winnings to total winnings
                member.functions.set(ctx, playerid, "totalWinnings",
                                     (member.functions.get(ctx, playerid, "totalWinnings") + winningAmount))
                # Adds 1 to hands won
                member.functions.set(ctx, playerid, "handsWon", (member.functions.get(ctx, playerid, "handsWon") + 1))

    # Removes players in leaving queue from table
    for playerid in table.functions.get(ctx, "leavingLine"):

        if Database("Tables", ctx.message.guild.id).is_there("players", {"userId": playerid}):
            table.functions.remove(ctx, "players", {"userId": playerid})
            table.functions.remove(ctx, "leavingLine", playerid)
            table.update(ctx, f"{ctx.message.guild.get_member(playerid).mention} has left the table.")

    # Set waiting for players to true if less than 2 players
    if len(table.functions.get(ctx, "players")) < 2:
        table.functions.set(ctx, {
            "waitingForPlayers": True
        })

    # Deletes table if waiting to delete
    if table.functions.get(ctx, "waitingToClose"):
        table.update(ctx, messages.closetable.closed)
        Database("Tables", ctx.message.guild.id).delete_entry("channelId", ctx.message.channel.id)
