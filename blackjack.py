""" 
This module is a Pygame based blackjack game, where
the player is dealt cards and try to beat the dealer
with a hand as close to but not exceeding 21 as possible.
The player can customize game settings at the start of the game.
"""
# This is the main file for final project


import random
class Deck:
    def __init__(self):
        self.cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] * 16
        self.shuffle_deck()

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if len(self.cards) < 52:
            self.shuffle_deck()
        return self.cards.pop()

# Creating 4 decks
decks = Deck()

# Example of dealing a card
card = decks.deal_card()
print("Dealt card:", card)
print(len(decks.cards))
class BlackjackGame:
    def __init__(self):
        self.player_chips = 500
        self.num_computer_players = self.get_num_computer_players()
        self.ai_difficulty = self.get_ai_difficulty()

    def get_num_computer_players(self):
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
        difficulty = input("Choose AI difficulty (Easy/Medium/Hard): ").lower()
        if difficulty in ["easy", "medium", "hard"]:
            return difficulty
        else:
            return "medium"

# Initializing the game
game = BlackjackGame()

import pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
black = (0, 0, 0)
white = (255, 255, 255)
DARK = (100, 100, 100)      # Dark color
LIGHT = (170, 170, 170)     # Light color
red = (255, 0, 0)
font = pygame.font.SysFont('Times New Roman', 35)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack game")

# Variable to determine if the game is running
running = True

# Main game loop for when the game is running
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(white)

    # Draw buttons for betting options
    pygame.draw.rect(screen, red, [50, 250, 100, 40], 1, 1)
    pygame.draw.rect(screen, red, [50, 150, 100, 40], 1, 1)
    pygame.draw.rect(screen, red, [50, 50, 100, 40], 1, 1)

    # Update portion of the screen
    pygame.display.flip()

# Quit the module
pygame.quit()
