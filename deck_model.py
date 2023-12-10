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
        Returns:
            str: The top card from the deck.
        """
        return self.cards.pop()

    def length(self):
        """
        Returns:
             int: the length of cards in the current deck
        """
        return len(self.cards)


class Player:
    """
    Represents a player in the game
    """
    def __init__(self, name, chips):
        """
        Initialize an instance of a player and their stats
        """
        self.name = name
        self.bought_chips = chips
        self.chips = chips
        self.wins = 0
        self.losses = 0

    def add_chips(self, amount):
        """
        Player add chips to their stash
        """
        self.bought_chips += amount
        self.chips += amount

    def win(self):
        """
        Adds player win count by 1
        """
        self.wins += 1

    def lose(self):
        """
        Adds player lose count by 1
        """
        self.losses += 1

    def display_results(self):
        """
        Returns summary statistics of user
        Returns:
            float: win probability of player
            int: earnings of player
        """
        win_probability = self.wins/(self.wins + self.losses)
        earnings = self.chips - self.bought_chips
        return win_probability, earnings