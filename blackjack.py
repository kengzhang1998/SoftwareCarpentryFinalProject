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
import sys
import time

# initializing pygame
pygame.init()


class BlackjackGame:
    """
    Manages a game of Blackjack, including players and game settings.
    Attributes:
        players (list of Player objects): The amount of players in the game
        ai_difficulty (str): The difficulty level of AI players.
        deck (Deck object): The deck in play
    """
    def __init__(self):
        """
        Initializes a new Blackjack game, setting up player chips, number of computer players,
        and AI difficulty.
        """
        self.players = []
        num_computer_players = self.get_num_computer_players()
        for i in range(num_computer_players + 1):
            player = Player(500, i)
            self.players.append(player)
        self.ai_difficulty = self.get_ai_difficulty()
        self.deck = Deck()
        self.player_bet = 0

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

    def bet(self, amount):
        """
        Places a bet for the current player.
        Args:
            amount (int): The amount to bet.
        """
        # Get the current player
        current_player = self.players[0]

        # Check if the player has enough chips
        if current_player.chips >= amount:
            # Deduct the bet amount from the player's chips
            current_player.chips -= amount
            # Record the bet amount
            self.player_bet = amount
            print(f"{current_player.name} has placed a bet of {amount}. Remaining chips: {current_player.chips}")
        else:
            # Not enough chips to place the bet
            print(f"Insufficient chips. You have {current_player.chips}, but tried to bet {amount}.")

        pass

    def double(self):
        """
        The player doubles their bet, receives one more card, and then stands.
        """
        # Assuming the first player in the list is the current player
        current_player = self.players[0]  
        if current_player.chips >= self.player_bet:
            current_player.chips -= self.player_bet
            self.player_bet *= 2
            print(f"Bet doubled. New bet is {self.player_bet}.")
            self.hit()
            self.stand()
        else:
            print("Not enough chips to double the bet.")

        pass

    def hit(self):
        """
        The player receives another card. If the total exceeds 21, they bust.
        """
        # Assuming the first player in the list is the current player
        current_player = self.players[0]
        new_card = self.deck.deal_card()
        current_player.hand.add_card(new_card)
        print(f"Dealt {new_card}. Total hand value now: {current_player.hand.value}")

        if current_player.hand.value > 21:
            print("Bust! You've exceeded 21.")

        pass

    def stand(self):
        """
        The player ends their turn without taking any additional cards.
        """
        print("Stand. No more cards.")
        pass

    def quit(self):
        """
        Quits the game if user decides to press the quit button
        """
        sys.exit()


def display_hand(curr_hand, x, y, isdealer = False):
    """

    :param hand: the given hand to be displayed
    :param x: starting x-coord of first card
    :param y: starting y-coord of first card
    :return:
    """
    for index, item in enumerate(curr_hand):
        image = item.get_image()
        image = pygame.transform.scale(image, (card_width, card_height))
        screen.blit(image, (x + index*50, y + index*10))


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


def settle_bets(player_hands, dealer_hand):
    """
    Settles bets at the end of each round based on the hands of each player.
    Args:
        player_hands (list of Hand objects): The list of hands of players in the game.
        dealer_hand (Hand object): The hand of dealer this round.
    """
    dealer_value = dealer_hand.calc_hand()
    for player_hand in player_hands:
        player_value = player_hand.calc_hand()
        if player_hand.value > 21:
            player_hand.lose_bet()
        elif player_hand.get_blackjack:  # Blackjack
            player_hand.win_bet(1.5)
        elif dealer_hand.get_blackjack:  # Dealer Blackjack
            if player_hand.get_blackjack is False:
                player_hand.lose_bet()
            else:
                player_hand.tie_bet()
        else:
            if player_value > dealer_value or dealer_value > 21:
                player_hand.win_bet()
            elif player_value < dealer_value:
                player_hand.lose_bet()
            else:
                player_hand.tie_bet()


# Initializing the game
game = BlackjackGame()

# Constants
WIDTH, HEIGHT = 1000, 1000
card_width, card_height = 200, 300
card_gap = 20
black = (0, 0, 0)
white = (255, 255, 255)
DARK = (100, 100, 100)      # Dark color
LIGHT = (170, 170, 170)     # Light color
red = (255, 0, 0)
green = (0, 128, 0)
button_font = pygame.font.SysFont('arial', 45)
game_font = pygame.font.SysFont('comicsansms', 30)
timer = pygame.time.Clock()
fps = 60
playing = False

dealer_hand = []
player_hand = []

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack game")
clock = pygame.time.Clock()


# Button method
def make_buttons(playing, player):
    button_list = []
    if not playing:
        deal = pygame.draw.rect(screen, white, [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, red, [150, 20, 300, 100], 3, 5)
        deal_text = button_font.render('DEAL', True, black)
        screen.blit(deal_text, (165, 50))
        button_list.append(deal)
    else:
        hit = pygame.draw.rect(screen, white, [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, red, [0, 700, 300, 100], 3, 5)
        hit_text = button_font.render('HIT', True, black)
        screen.blit(hit_text, (55, 735))
        button_list.append(hit)
        stand = pygame.draw.rect(screen, white, [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, red, [300, 700, 300, 100], 3, 5)
        stand_text = button_font.render('STAND', True, black)
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)
        records = player.get_records()
        score_text = game_font.render(f'Wins: {records[0]} Losses: {records[1]} Draws: {records[2]}', True, white)
        screen.blit(score_text, (15, 840))
    return button_list

# Variable to determine if the game is running
running = True

player = Player(500, 0)
player.tally('win')


# Main game loop for when the game is running
def deal_cards(curr_dealer_hand, curr_player_hand, curr_game):
    for i in range(2):
        curr_dealer_hand.append(curr_game.deck.deal_card())
        curr_player_hand.append(curr_game.deck.deal_card())


while running:
    timer.tick(fps)
    screen.fill(green)

    # Install buttons
    buttons = make_buttons(playing, player)

    if playing:
        display_hand(dealer_hand, 100, 350)
        display_hand(player_hand, 600, 350)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not playing:
                if buttons[0].collidepoint(event.pos):
                    playing = True
                    dealer_hand = []
                    player_hand = []
                    deal_cards(dealer_hand, player_hand, game)
    # Debug

    # Update portion of the screen
    pygame.display.flip()

# Quit the module
pygame.quit()
