""" 
This module is a Pygame based blackjack game, where
the player is dealt cards and try to beat the dealer
with a hand as close to but not exceeding 21 as possible.
The player can customize game settings at the start of the game.
"""

# This is the main file for final project

from deck_model import *
import random
import pygame

# Creating 4 decks
decks = Deck()

# Example of dealing 2 cards
card = decks.deal_card()
print("Dealt card:", card.get_value())
print(len(decks.cards))

card = decks.deal_card()
print("Dealt card:", card.get_value())
print(len(decks.cards))


class BlackjackGame:
    """
    Manages a game of Blackjack, including players and game settings.
    Attributes:
        player_chips (int): The amount of chips the player starts with.
        num_computer_players (int): Number of computer players in the game.
        ai_difficulty (str): The difficulty level of AI players.
    """
    def __init__(self):
        """
        Initializes a new Blackjack game, setting up player chips, number of computer players,
        and AI difficulty.
        """
        self.player_chips = 500
        self.num_computer_players = self.get_num_computer_players()
        self.ai_difficulty = self.get_ai_difficulty()

    def get_num_computer_players(self):
        """
        Prompts the user to input the number of computer players (1-4).
        Returns:
            int: The number of computer players.
        """
        while True:
            try:
                num_players = int(input("Enter number of computer players (1-4): "))
                if 1 <= num_players <= 4:
                    return num_players
                else:
                    print("Invalid number. Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def get_ai_difficulty(self):
        """
        Asks the user to choose the AI difficulty level.
        Returns:
            str: The chosen AI difficulty ('easy', 'medium', or 'hard').
        """
        difficulty = input("Choose AI difficulty (Easy/Medium/Hard): ").lower()
        if difficulty in ["easy", "medium", "hard"]:
            return difficulty
        else:
            return "medium"


def place_bets_and_deal(players, dealer, deck):
    """
    Handles the betting and dealing of cards at the start of each game round.
    Args:
        players (list of Player objects): The list of players in the game.
        dealer (Dealer object): The dealer of the game.
        deck (Deck object): The deck of cards used in the game.
    """
    if len(deck) < 52:
        deck.shuffle()

    for player in players:
        if player.ask_for_chips():
            player.add_chips()

        bet_amount = player.place_bet()
        player.bet(bet_amount)

        # Deal cards
        player.hand.append(deck.deal_card(face_up=True))
        dealer.hand.append(deck.deal_card(face_up=True))

    # Deal second round of cards
    for player in players:
        player.hand.append(deck.deal_card(face_up=True))
    dealer.hand.append(deck.deal_card(face_up=False))


def play_hand(players, dealer, deck):
    """
    Manages the actions of each player during their turn in the game.
    Args:
        players (list of Player objects): The list of players in the game.
        dealer (Dealer object): The dealer of the game.
        deck (Deck object): The deck of cards used in the game.
    """
    for player in players:
        while True:
            action = player.choose_action()
            if action == 'hit':
                player.hand.append(deck.deal_card(face_up=True))
                if player.calculate_hand_value() > 21:
                    player.status = 'bust'
                    break
            elif action in ['split', 'double', 'stand']:
                # Implement the logic for split, double, stand
                break

    # AI players' turns
    for player in players:
        if player.is_ai:
            ai_logic(player)

    # Dealer's turn
    while dealer.calculate_hand_value() < 17:
        dealer.hand.append(deck.deal_card(face_up=True))


def settle_bets(players, dealer):
    '''
    Settles bets at the end of each hand based on the game's outcome.
    Args:
        players (list of Player objects): The list of players in the game.
        dealer (Dealer object): The dealer of the game.
    '''
    dealer_value = dealer.calculate_hand_value()
    for player in players:
        player_value = player.calculate_hand_value()
        if player.status == 'bust':
            player.lose_bet()
        elif player_value == 21 and len(player.hand) == 2:  # Blackjack
            player.win_bet(1.5)
        elif dealer_value == 21 and len(dealer.hand) == 2:  # Dealer Blackjack
            if player_value != 21 or len(player.hand) != 2:
                player.lose_bet()
            else:
                player.tie_bet()
        else:
            if player_value > dealer_value or dealer_value > 21:
                player.win_bet()
            elif player_value < dealer_value:
                player.lose_bet()
            else:
                player.tie_bet()


# Initializing the game
game = BlackjackGame()

# Constants
WIDTH, HEIGHT = 900, 500
black = (0, 0, 0)
white = (255, 255, 255)
DARK = (100, 100, 100)      # Dark color
LIGHT = (170, 170, 170)     # Light color
red = (255, 0, 0)
green = (0, 128, 0)
# font = pygame.font.SysFont('Times New Roman', 35)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack game")

# Variable to determine if the game is running
running = True

# Main game loop for when the game is running
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(green)

    # Draw buttons for betting options
    pygame.draw.rect(screen, red, [50, 250, 100, 40], 1, 1)
    pygame.draw.rect(screen, red, [50, 150, 100, 40], 1, 1)
    pygame.draw.rect(screen, red, [50, 50, 100, 40], 1, 1)

    # Update portion of the screen
    pygame.display.flip()

# Quit the module
pygame.quit()
