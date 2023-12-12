""" 
This module is a Pygame based blackjack game, where
the player is dealt cards and try to beat the dealer
with a hand as close to but not exceeding 21 as possible.
The player can customize game settings at the start of the game.
"""

# This is the main file for the final project

from deck_model import *
import random
import pygame
import sys
import time

# initializing pygame
pygame.init()

class BlackjackGame:
    """
    Manages a game of Blackjack, including players 
    and game settings.
    Attributes:
        players (list): Players in the game, including AI.
        ai_difficulty (str): AI difficulty level.
        deck (Deck): Current deck of cards.
    Methods:
        get_num_computer_players: Gets AI player count.
        get_ai_difficulty: Selects AI difficulty level.
        bet: Player places a bet.
        double: Doubles player's bet and ends turn.
        hit: Adds card to player's hand, checks for bust.
        stand: Ends player's turn.
        quit: Exits the game.
    """
    def __init__(self):
        """
        Sets up game with initial player chips, 
        AI players, and difficulty.
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
        Prompts the user to input the number 
        of computer players (1-4).
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


def display_hand(curr_hand, x, y, is_dealer=False):
    """
    :param curr_hand: the given hand to be displayed
    :param x: starting x-coord of first card
    :param y: starting y-coord of first card
    :param is_dealer: True if the hand is from the dealer
    :return:

    Displays a hand of cards at specified coordinates.
    For the dealer's first turn, shows one card face down.
    """
    
    for index, item in enumerate(curr_hand):
        if is_dealer and index == 1:
            image = pygame.image.load('images/card_back.png')
            image = pygame.transform.scale(image, (card_width, card_height))
            screen.blit(image, (x + index * 50, y + index * 10))
        else:
            image = item.get_image()
            image = pygame.transform.scale(image, (card_width, card_height))
            screen.blit(image, (x + index * 50, y + index * 10))


def place_bets_and_deal(players, dealer, deck):
    """
    Handles the betting and dealing of cards at the start of each game round.
    Args:
        players (list): Players in the game.
        dealer (object): Dealer of the game.
        deck (object): Deck of cards.
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


def is_black_jack(curr_hand):
    """
    Checks if a hand is a blackjack.
    Args:
        curr_hand (list): Hand to check.
    Returns:
        bool: True if blackjack, False otherwise.
    """
    ace = []
    not_ace = []
    for card in curr_hand:
        if card.get_value() == 'A':
            ace.append(card)
        else:
            not_ace.append(card)
    if len(ace) == 1:
        if len(not_ace) == 1:
            if not_ace[0].get_value() in 'JQK10':
                return True
    return False


def settle_bets(curr_player_hand, curr_dealer_hand, curr_player, curr_bet):
    """
    Settles bets based on player and dealer hands.
    Args:
        curr_player_hand, 
        curr_dealer_hand (list): Player and dealer hands.
        curr_player (object): Current player.
        curr_bet (int): Current bet amount.
    """
    dealer_value = calc_hand(curr_dealer_hand)
    player_value = calc_hand(curr_player_hand)
    new_bet = 0
    if player_value > 21:    # Player bust, loses bet
        condition = 'loss'
    elif is_black_jack(curr_player_hand):  # Player Blackjack
        if is_black_jack(curr_dealer_hand):   # Dealer also gets Blackjack, tie
            new_bet = curr_bet
            condition = 'draw'
        else:                        # Only player has blackjack, wins 2.5 * bet
            new_bet = curr_bet * 2.5
            condition = 'win'
    elif is_black_jack(curr_dealer_hand):  # Dealer Blackjack only, loses bet
        condition = 'loss'
    else:
        if player_value > dealer_value or dealer_value > 21:  # Dealer busts or smaller than player
            new_bet = curr_bet * 2
            condition = 'win'
        elif player_value < dealer_value:  # Dealer has bigger hand
            condition = 'loss'
        else:  # Dealer and player has same value
            new_bet = curr_bet
            condition = 'draw'
    curr_player.tally(condition)
    curr_player.settle(new_bet)
    return True


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
text_font = pygame.font.SysFont('times new roman', 30)
timer = pygame.time.Clock()
fps = 60
playing = False           # Tracks if the round is active
can_act = False           # Tracks if the player can take actions
end_game = False          # Tracks if the end game is reached
scoring = False           # Tracks if scoring can happen
new_game = False          # Allows for a new game
betting = True           # Tracks if the user is in betting stage or not
input_active = False      # Allows user to enter bet amount if active
user_text = ''            # User input into betting text inbox
round_bet = 0             # User betting amount

# Initialize variables that update/reset each round
dealer_hand = []
player_hand = []
player_score = 0
dealer_score = 0

# Set up display, caption, clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack game")
clock = pygame.time.Clock()


# Button method
def make_buttons(betting_status, playing_status, curr_player, new_game_status):
    """
    Creates interactive buttons based on game status.
    Args:
        playing_status, new_game_status (bool): Current game statuses.
        curr_player (object): Current player.
    Returns:
        list: Interactive buttons for game actions.
    """
    button_list = []
    if betting_status:
        bet = pygame.draw.rect(screen, white, [550, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, red, [550, 20, 300, 100], 3, 5)
        bet_text = button_font.render('BET', True, black)
        screen.blit(bet_text, (585, 50))
        button_list.append(bet)
    if not playing_status:
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
        records = curr_player.get_records()
        score_text = game_font.render(f'Wins: {records[0]} Losses: {records[1]} Draws: {records[2]}', True, white)
        screen.blit(score_text, (15, 840))
    if new_game_status:
        next_game = pygame.draw.rect(screen, white, [300, 100, 300, 100], 0, 5)
        pygame.draw.rect(screen, red, [300, 100, 300, 100], 3, 5)
        game_text = button_font.render('New Game', True, black)
        screen.blit(game_text, (350, 100))
        button_list.append(next_game)
    return button_list


def calc_hand(curr_hand):
    """
    Calculates total value of a hand.
    Args:
        curr_hand (list): Hand to calculate.
    Returns:
        int: Total hand value.
    """
    ace = []
    not_ace = []
    curr_val = 0
    for card in curr_hand:
        if card.get_value() == 'A':
            ace.append(card)
        else:
            not_ace.append(card)
    for card in not_ace:
        if card.get_value() in 'JQK':
            curr_val += 10
        else:
            curr_val += int(card.get_value())

    for card in ace:
        if curr_val <= 10:
            curr_val += 11
        else:
            curr_val += 1
    return curr_val


def display_text(text, x, y):
    """
    Displays text at specified coordinates on the screen.
    """
    screen.blit(text_font.render(text, True, black), (x, y))


# Variable to determine if the game is running
running = True

player = Player(500, 0)

# print(line)


# Main game loop for when the game is running
def deal_cards(curr_dealer_hand, curr_player_hand, curr_game):
    for i in range(2):
        curr_dealer_hand.append(curr_game.deck.deal_card())
        curr_player_hand.append(curr_game.deck.deal_card())


def draw_score(curr_score, x, y, text):
    screen.blit(text_font.render(f'{text:}[{curr_score}]', True, black), (x, y))


while running:
    timer.tick(fps)
    screen.fill(green)

    # Install buttons
    buttons = make_buttons(betting, playing, player, new_game)

    if playing:
        display_text(f'Available chips: {player.chips}', 100, 900)
        display_text("Dealer's hand", 100, 100)
        display_text("Player's hand", 600, 100)
        display_hand(player_hand, 600, 250)
        dealer_score = calc_hand(dealer_hand)
        if not can_act:       # Player turn finishes
            if dealer_score < 17:       # Dealer hits when value is < 17
                dealer_hand.append(game.deck.deal_card())
            else:
                end_game = True       # Ready to be settled
            display_hand(dealer_hand, 100, 250)     # Reviews dealer's hidden card
            draw_score(dealer_score, 100, 600, "Dealer score")
        else:         # Display dealer's hidden card
            display_hand(dealer_hand, 100, 250, True)
        player_score = calc_hand(player_hand)
        draw_score(player_score, 600, 600, "Player score")

    if betting:
        display_text(user_text, 900, 900)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if betting:
                if buttons[0].collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
            elif not playing:
                if buttons[0].collidepoint(event.pos):
                    playing = True
                    dealer_hand = []
                    player_hand = []
                    deal_cards(dealer_hand, player_hand, game)
                    can_act = True
                    scoring = False
            else:
                if buttons[0].collidepoint(event.pos) and player_score < 21 and can_act:
                    player_hand.append(game.deck.deal_card())
                elif buttons[1].collidepoint(event.pos):
                    can_act = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        scoring = False
                        new_game = False
                        end_game = False
                        playing = False
                        dealer_hand = []
                        player_hand = []
                        can_act = True
                        player_score = 0
                        dealer_score = 0
                        betting = True
        if event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    print(user_text)
                    betting = False
                    round_bet = int(user_text)
                    player.bet(round_bet)
                    user_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
    # If player has reached 21 after hitting
    if can_act and player_score >= 21:
        can_act = False

    if end_game and scoring is False:
        new_game = settle_bets(player_hand, dealer_hand, player, round_bet)
        scoring = True

    # Update portion of the screen
    pygame.display.flip()

# Quit the module
pygame.quit()
