"""
This file includes several basic card models that will be
used by the blackjack.py file
"""
from enum import Enum
import pygame
import random


class Suits(Enum):
    """
    List of suits that are available in a standard deck
    """
    CLUB = 0
    SPADE = 1
    HEART = 2
    DIAMOND = 3


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
        self.image = pygame.image.load('images/' + self.suit.name + str(self.value) + '.jpg')

