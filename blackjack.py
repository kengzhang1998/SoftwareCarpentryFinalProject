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

# The following sections are for debugging purposes
# Creating a deck
decks = Deck()

# Example of dealing 2 cards
card = decks.deal_card()
print("Dealt card:", card.get_value())
print(len(decks.cards))


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

    def deal(self):
        hands = []
        dealer_hand = Hand()
        hands.append(dealer_hand)
        image = pygame.image.load('images/Club2.png').convert()
        image = pygame.transform.scale(image, (100, 100))
        screen.blit(image, (200, 450))
        for player in self.players:
            hand = Hand(player)
            hands.append(hand)
        pygame.display.update()
        #for hand in hands:
            #card = self.deck.deal_card()
            #hand.add_card(card)
            #print("Dealt card:", card.get_value())
            #image = pygame.image.load('images/' + card.suit + card.value + '.png').convert()
            #image = pygame.transform.scale(image, (100, 100))
            #screen.blit(image, (200, 450))
            #clock.tick(300)
            #pygame.display.flip()

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


def draw_hand(hand):
    pass

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


"""
def play_hand(players, dealer, deck):
    """"""
    Manages the actions of each player during their turn in the game.
    Args:
        players (list of Player objects): The list of players in the game.
        dealer (Dealer object): The dealer of the game.
        deck (Deck object): The deck of cards used in the game.
    """"""
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
"""


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
card_width, card_height = 78, 120
card_gap = 20
black = (0, 0, 0)
white = (255, 255, 255)
DARK = (100, 100, 100)      # Dark color
LIGHT = (170, 170, 170)     # Light color
red = (255, 0, 0)
green = (0, 128, 0)
button_font = pygame.font.SysFont('arial', 30)
timer = pygame.time.Clock()
fps = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack game")
clock = pygame.time.Clock()

# Button method
def button(text, x, y, w, h, action=None):
    """
    Sets up a display button for player actions
    :param text: text to be added
    :param x: start horizontal position of button
    :param y: start vertical position of button
    :param w: width of button
    :param h: height of button
    :param action: associated action of the button
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, LIGHT, (x, y, w, h))
        if click[0] == 1 != None:
            action()
    else:
        pygame.draw.rect(screen, DARK, (x, y, w, h))
    display_text = button_font.render(text, True, black)
    screen.blit(display_text, ((x+(w/2)-50), (y+(h/2))-20))


# Variable to determine if the game is running
running = True

# Main game loop for when the game is running
while running:
    timer.tick(fps)
    screen.fill(green)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                game.deal()

    button("BET", 30, 50, 150, 50, game.bet)
    button("DEAL", 30, 150, 150, 50)
    button("HIT", 30, 250, 150, 50, game.hit)
    button("STAND", 30, 350, 150, 50, game.stand)
    button("DOUBLE", 30, 450, 150, 50, game.double)
    button("QUIT", 30, 800, 150, 50, game.quit)

    # Update portion of the screen
    pygame.display.flip()

# Quit the module
pygame.quit()
