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
    Represents a playing card with suit, value, and image.
    Attributes:
        suit (str): The suit of the card (e.g., 'Club', 'Spade').
        value (str): The value of the card (e.g., '2', 'A').
        image (pygame.Surface): The pygame image object 
        representing the card's visual.
    Methods:
        get_value: Returns the value of the card.
        get_image: Returns the pygame image of the card.
    """
    
    # Initializes a new card with the specified suit and value.
    def __init__(self, suit, value):
        """
        Initializes a new card instance with the specified suit and value.

        Args:
            suit (str): The suit of the card.
            value (str): The face value of the card.
        """
        # The suit of the card.
        self.suit = suit
        # The value of the card.
        self.value = value
        self.image = pygame.image.load('images/' + self.suit + self.value + '.png')
    
    # Returns the face value of the card.
    def get_value(self):
        return self.value
        
    # Returns the pygame image associated with the card.
    def get_image(self):
        return self.image


class Deck:
    """
    Represents a deck of playing cards.
    Attributes:
        cards (list of Card): A list of Card objects representing the deck.
    Methods:
        shuffle_deck: Shuffles the cards in the deck randomly.
        deal_card: Deals and returns the top card from the deck.
        length: Returns the number of cards remaining in the deck.
    """
    
    def __init__(self):
        """
        Initializes the Deck instance with 52 cards
        and shuffles them.
        """
        self.cards = []
        for i in range(4):
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

        # Reinitialize the deck if it's empty
        if len(self.cards) >= 1:
            return self.cards.pop()
        else:
            for i in range(4):
                for suit in suits:
                    for value in values:
                        self.cards.append(Card(suit, value))
            self.shuffle_deck()
            return self.cards.pop()
    
    # Returns the number of cards currently in the deck.
    def length(self):
        """
        Returns:
             int: the length of cards in the current deck
        """
        return len(self.cards)


class Player:
    """
    Represents a player in a card game, handling chips and records.
    Attributes:
        bought_chips (int): The initial number of chips bought by the player.
        chips (int): The current number of chips the player has.
        records (list of int): A list tracking the player's wins, losses, and draws.
        player_id (int): The unique identifier for the player.
    Methods:
        add_chips: Adds a specified amount of chips to the player's stash.
        tally: Updates the player's records based on game results.
        display_results: Calculates and returns the player's win probability and earnings.
        get_records: Returns the player's win, loss, and draw records.
        settle: Adjusts the player's chips based on the bet outcome.
        bet: Places a bet by deducting chips from the player's stash.
    """
    
    def __init__(self, chips, player_id):
        """
        Initialize an instance of a player and their stats
        Args:
            chips (int): The initial number of chips the player has.
            player_id (int): The unique identifier for the player.
        """
        self.bought_chips = chips
        self.chips = chips
        self.records = [0, 0, 0]     # Tracks wins/losses/draws
        self.player_id = player_id

    def add_chips(self, amount):
        """
        Adds a specified amount of chips to the player's current stash.
        Args:
            amount (int): The number of chips to add.
        """
        self.bought_chips += amount
        self.chips += amount

    def tally(self, condition):
        """
        Updates the player's win, loss, or draw record based on the game's outcome.
        Args:
            condition (str): The outcome of the game ('win', 'loss', 'draw').
        """
        if condition == 'win':
            self.records[0] += 1
        elif condition == 'loss':
            self.records[1] += 1
        elif condition == 'draw':
            self.records[2] += 1

    def win_probability(self):
        """
        Returns summary statistics of user
        Returns:
            float: win probability of player
            int: earnings of player
        """
        if sum(self.records) != 0:
            win_probability = self.records[0]/(sum(self.records))
            return win_probability
        else:
            return 0

    def get_records(self):
        """
        Returns the player's game records.
        Returns:
            list of int: The player's wins, losses, and draws.
        """
        return self.records

    def settle(self, bet):
        """
        Adjusts the player's chips based on the outcome of a bet.
        Args:
            bet (int): The amount to adjust the player's chips by.
        """
        self.chips += bet

    def bet(self, amount):
        """
        Places a bet by deducting a specified amount from the player's chips.
        Args:
            amount (int): The bet amount.
        """
        self.chips -= amount
