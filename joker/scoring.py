class Score:
    def __init__(self, hand, table):
        self.hand = hand
        self.table = table

        self.value = self.__get_score()

    def get(self):
        return self.value

    def __flush(self):
        """
        Checks for a flush, returning either the suit or False
        :return: either the suit of the flush, or False if there is no flush
        """
        suits = [x[0] for x in (self.hand + self.table)]
        if suits.count('♦') >= 5:
            return '♦'
        if suits.count('♥') >= 5:
            return '♥'
        if suits.count('♠') >= 5:
            return '♠'
        if suits.count('♣') >= 5:
            return '♣'
        else:
            return False

    def __runs(self, cards, pos):
        """
        Specifically for use in straight(). Part of the process that checks if a list of cards (:param cards:),
        starting from a certain position(:param pos:), when everything is subtracted by its first number equals
        [0, 1, 2, 3, 4], which indicates that that set of numbers is, indeed, consecutive and therefore a straight. This
        is the part that subtracts everything by the first number.
        :param cards: A list of cards without their suits and in number form (Jack=11, Queen=12, King=13, Ace=14 or 1)
        They are also in numerical order.
        :param pos: The position in the cards the function starts with when checking for 5 consecutive numbers
        :return:
        """
        return [(x - cards[pos]) for x in cards]

    def __straight(self, cards):  # determines if there is a straight, and if so, what its high card is
        cards = list(set(cards))  # removes duplicates and puts in order
        if len(cards) < 5:
            return False
        if cards[-1] == 14:  # puts ace also in the front as a one cuz straights be like that
            cards = [1] + cards
        if len(cards) == 8:  # hand + table + maybe ace being at front and back
            if runs(cards, 3)[3:] == list(range(0,
                                                5)):
                return 4 + cards[3]
        if len(cards) >= 7:
            if runs(cards, 2)[2:7] == list(range(0, 5)):
                return 4 + cards[2]
        if len(cards) >= 6:
            if runs(cards, 1)[1:6] == list(range(0, 5)):
                return 4 + cards[1]
        if runs(cards, 0)[0:5] == list(range(0, 5)):
            return 4 + cards[0]
        else:
            return False

    def __four_check(self, cards):  # all these somethingcheck functions check for their respective match and return either false or part of thne number described in 132
        four = [x for x in cards if cards.count(x) == 4]
        if len(four) != 0:
            return four[-1]
        else:
            return False

    def __house_check(self, cards):
        three = [x for x in cards if cards.count(x) == 3]  # straightforward
        two = [x for x in cards if cards.count(x) == 2]
        if len(three) != 0:
            if three[0] != three[-1]:
                return three[-1] + (three[0] / 100)  # 132 decimal thing
            if len(two) != 0:
                return three[-1] + (two[-1] / 100)
            else:
                return False
        else:
            return False

    def __three_check(self, cards):
        three = [x for x in cards if cards.count(x) == 3]
        if len(three) != 0:
            return three[-1]
        else:
            return False

    def __two_pair_check(self, cards):
        two = [x for x in cards if cards.count(x) == 2]
        if len(two) != 0:
            if len(two) >= 4:
                return two[-1] + (two[-3] / 100)
            else:
                return False
        else:
            return False

    def __pair_check(self, cards):
        two = [x for x in cards if cards.count(x) == 2]
        if len(two) != 0:
            return two[-1]
        else:
            return 0

    def __high_card(self, cards, hand, table, rank):
        hand = sorted(
            [14 if x[-1] == 'e' else 13 if x[-1] == 'g' else 12 if x[-1] == 'n' else 11 if x[-1] == 'k' else int(x[1:]) for
             x in hand])  # same as line 133 but with hand instead of all cards
        if rank == 'house':  # to determine winning hand when ranks are identical; gives the high card value for the very end of score number (see 132)
            house_used = __house_check(self, cards)
            used = [int(house_used),
                    int(house_used * 100) - (int(house_used) * 100)]  # cards u used to make the match cant be ur high card
            hand = [x for x in hand if x not in used]
            if len(hand) == 2:
                return sorted(hand)[-1] + sorted(hand)[0] / 100
            if len(hand) == 1:
                return hand[0]
            else:
                return 0
        if rank == 'straight':
            table = sorted(
                [14 if x[-1] == 'e' else 13 if x[-1] == 'g' else 12 if x[-1] == 'n' else 11 if x[-1] == 'k' else int(x[1:])
                 for x in table])
            straight_cards = __straight(self, cards)
            used = list(range(straight_cards - 4, straight_cards + 1))
            used = [x for x in used if x not in table]
            hand = [x if hand.count(x) > 1 else False if x in used else x for x in hand]
            hand = [x for x in hand if x != False]
            if len(hand) == 2:
                return sorted(hand)[-1] + sorted(hand)[0] / 100
            if len(hand) == 1:
                return hand[0]
            else:
                return 0
        if rank == 'three':
            hand = [x for x in hand if x != __three_check(self, cards)]
            if len(hand) == 2:
                return sorted(hand)[-1] + sorted(hand)[0] / 100
            if len(hand) == 1:
                return hand[0]
            else:
                return 0
        if rank == 'twoPair':
            two_pair_used = __two_pair_check(self, cards)
            used = [int(two_pair_used), int(two_pair_used * 100) - (int(two_pair_used) * 100)]
            hand = [x for x in hand if x not in used]
            if len(hand) == 2:
                return sorted(hand)[-1] + sorted(hand)[0] / 100
            if len(hand) == 1:
                return hand[0]
            else:
                return 0
        if rank == 'pair':
            hand = [x for x in hand if x != __pair_check(self, cards)]
            if len(hand) == 2:
                return sorted(hand)[-1] + sorted(hand)[0] / 100
            if len(hand) == 1:
                return hand[0]
            else:
                return 0
        if rank == 'none':  # stuff where highcard doesnt exist or matter if its in the match: straight flush cant be the same rank by nature of flush unless its all on the table which is just normal high card - high card obv - 4 of a kind same reasons as flush -
            return hand[-1] + hand[0] / 100

    '''
    The actual code that scores hands.
    '''

    def __get_score(self, hand, table):  # Finally the actual function that calculates the hand score- score format is: a.bcdefghi where a represents what match it is (straight flush through high card from 9 to 1, 9.14 specifically being a royal flush) bc is the highest card of the match (highest card of the straight flush, straight, or flush, what you have 4 of in four of a kind, the card for the triple in the full house, etc. pretty straightforwards i hope also in the format of like 10 or 04) now de in the specific case of house and two pair is the card for the secondary match (the pair in full house and the second(smaller) pair in two pair) in every other case it is the highest card in your hand that has not been used already (unless it is specifically denoted as having rank 'none') fg is the same, just secondary high card (or first if its house or two pair) hi is just house or two pair's version of fg
        cards = sorted(
            [14 if x[-1] == 'e' else 13 if x[-1] == 'g' else 12 if x[-1] == 'n' else 11 if x[-1] == 'k' else int(x[1:]) for
             x in (
                         hand + table)])  # Replaces Aces, Kings, Queens, and Jacks with their respective numbers (14,13,12,11) and also places everything in order, as well as removing all of the suit symbols.
        if not __flush(self, hand, table) == False:
            cards2 = [14 if x[-1] == 'e' else 13 if x[-1] == 'g' else 12 if x[-1] == 'n' else 11 if x[-1] == 'k' else int(x)
                      for x in [x[1:] if x[0] == __flush(self, hand, table) else False for x in hand + table] if x != False]
            # The above line just replaces Aces, Kings, Queens, and Jacks with their respective numbers (14,13,12,11) from a version of the cards in the hand and on the table where any card that does not match the "flush" suit is replaced by "False" and the replacing of Aces, Kings, etc. also ignores entries that are "False".
            if not __straight(self, cards2) == False:  # if not false == if true but the 'true' value isnt actually true its a number.
                return (9 + __straight(self, cards2) / 100) + __high_card(self, cards, hand, table, 'none') / 10000  # all the returns just create the number score stated on line 132.
        if not __four_check(self, cards) == False:
            return 8 + __four_check(self, cards) / 100 + __high_card(self, cards, hand, table, 'none') / 10000
        if not __house_check(self, cards) == False:
            return 7 + __house_check(self, cards) / 100 + __high_card(self, cards, hand, table, 'house') / 1000000
        if not __flush(self, hand, table) == False:
            cardsTwo = sorted(
                [14 if x[-1] == 'e' else 13 if x[-1] == 'g' else 12 if x[-1] == 'n' else 11 if x[-1] == 'k' else int(x) for
                 x in [x[1:] if x[0] == __flush(self, hand, table) else False for x in hand + table] if
                 x != False])  # same thing as cards2
            return 6 + cardsTwo[-1] / 100 + __high_card(self, cards, hand, table, 'none') / 10000
        if not __straight(self, cards) == False:
            return 5 + __straight(self, cards) / 100 + __high_card(self, cards, hand, table, 'straight') / 10000
        if not __three_check(self, cards) == False:
            return 4 + __three_check(self, cards) / 100 + __high_card(self, cards, hand, table, 'three') / 10000
        if not __two_pair_check(self, cards) == False:
            return 3 + __two_pair_check(self, cards) / 100 + __high_card(self, cards, hand, table, 'twoPair') / 1000000
        if not __pair_check(self, cards) == False:
            return 2 + __pair_check(self, cards) / 100 + __high_card(self, cards, hand, table, 'pair') / 10000
        else:
            return 1 + __high_card(self, cards, hand, table, 'none') / 100

    def translate(self, score):  # Gives kind of match based on score
        if score >= 9.14:
            return 'ROYAL FLUSH'
        scores = {
            9: 'STRAIGHT FLUSH',
            8: 'FOUR OF A KIND',
            7: 'FULL HOUSE',
            6: 'FLUSH',
            5: 'STRAIGHT',
            4: 'THREE OF A KIND',
            3: 'TWO PAIR',
            2: 'PAIR',
            1: 'HIGH CARD'
        }
        return scores[int(score)]

