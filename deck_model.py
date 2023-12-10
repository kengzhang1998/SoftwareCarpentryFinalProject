"""
This file includes several basic card models that will be
used by the blackjack.py file
"""
import pygame
import random

# List the available suits and values in a deck
suits = ['Club', 'Spade', 'Heart', 'Diamond']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


class Card:
    """
    An instance of a card with suit and value, and associated pygame image
    Attributes:
        suit(int): represents the suit of the card
        value(str): represents the card value (2-A) of the card
        image(file): represents the associated image of the card
    """
    def __init__(self, suit, value):
        """
        Initializes a new card with given suit and value from the user,
        and pulls the corresponding card image from the images folder
        """
        self.suit = suit
        self.value = value
        self.image = pygame.image.load('images/' + self.suit + self.value + '.png')

    def get_value(self):
        return self.value


class Deck:
    """
    Represents a deck of playing cards for card games.
    Attributes:
        cards (list of str): List of cards in the deck.
    """
    def __init__(self):
        """
        Initializes the Deck instance with 52 cards
        and shuffles them.
        """
        self.cards = []
        for suit in suits:
            for value in values:
                self.cards.append(Card(suit, value))
        self.shuffle_deck()

    def shuffle_deck(self):
        """
        Randomly shuffles the cards in the deck.
        """
        random.shuffle(self.cards)

    def deal_card(self):
        """
        Deals the top card from the deck.
        If there are less than 52 cards, reshuffles the deck.
        Returns:
            str: The top card from the deck.
        """
        #if len(self.cards) < 52:
            #self.shuffle_deck()
        return self.cards.pop()
