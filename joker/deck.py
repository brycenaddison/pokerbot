import random

FULL_DECK = ['♦2', '♥2', '♠2', '♣2',
             '♦3', '♥3', '♠3', '♣3',
             '♦4', '♥4', '♠4', '♣4',
             '♦5', '♥5', '♠5', '♣5',
             '♦6', '♥6', '♠6', '♣6',
             '♦7', '♥7', '♠7', '♣7',
             '♦8', '♥8', '♠8', '♣8',
             '♦9', '♥9', '♠9', '♣9',
             '♦10', '♥10', '♠10', '♣10',
             '♦J', '♥J', '♠J', '♣J',
             '♦Q', '♥Q', '♠Q', '♣Q',
             '♦K', '♥K', '♠K', '♣K',
             '♦A', '♥A', '♠A', '♣A']


def new_deck():
    deck = FULL_DECK
    random.shuffle(deck)
    return deck


def draw(deck):
    card = deck[0]
    deck = deck[1:]
    return card, deck
