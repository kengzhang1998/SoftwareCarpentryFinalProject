""" 
This module is a Pygame based blackjack game, where
the player is dealt cards and try to beat the dealer
with a hand as close to but not exceeding 21 as possible.
The player can customize game settings at the start of the game.
"""

# This is the main file for the final project
from deck_model import *
import pygame

# initializing pygame
pygame.init()


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


def is_black_jack(curr_hand):
    """
    Checks if a hand is a blackjack.
    Args:
        curr_hand (list): Hand to check.
    Returns:
        bool: True if blackjacked, False otherwise.
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
        curr_player_hand (list): The player's hand.
        curr_dealer_hand (list): The dealer's hand.
        curr_player (object): Current player.
        curr_bet (int): Current bet amount.
    """
    dealer_value = calc_hand(curr_dealer_hand)
    player_value = calc_hand(curr_player_hand)
    new_bet = 0
    message = ''
    if player_value > 21:    # Player bust, loses bet
        condition = 'loss'
        message = "You busted!"
    elif is_black_jack(curr_player_hand):  # Player Blackjack
        if is_black_jack(curr_dealer_hand):   # Dealer also gets Blackjack, tie
            new_bet = curr_bet
            condition = 'draw'
            message = "You both get blackjack, it's a draw!"
        else:                        # Only player has blackjack, wins 2.5 * bet
            new_bet = curr_bet * 2.5
            condition = 'win'
            message = "You win blackjack! Congratulations!"
    elif is_black_jack(curr_dealer_hand):  # Dealer Blackjack only, loses bet
        condition = 'loss'
        message = "Dealer gets blackjack! You lose"
    else:
        if player_value > dealer_value or dealer_value > 21:  # Dealer busts or smaller than player
            new_bet = curr_bet * 2
            condition = 'win'
            message = "You won this round!"
        elif player_value < dealer_value:  # Dealer has bigger hand
            condition = 'loss'
            message = 'Dealer wins this round!'
        else:  # Dealer and player has same value
            new_bet = curr_bet
            condition = 'draw'
            message = "You have the same value, it's a draw!"
    curr_player.tally(condition)
    curr_player.settle(new_bet)
    return True, message


# Constants
WIDTH, HEIGHT = 1000, 1000
card_width, card_height = 200, 300
card_gap = 20
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 128, 0)
button_font = pygame.font.SysFont('arial', 45)
game_font = pygame.font.SysFont('comicsansms', 30)
text_font = pygame.font.SysFont('times new roman', 30)
timer = pygame.time.Clock()
fps = 60

# Game variables
deck = Deck()
playing = False           # Tracks if the round is active
can_act = False           # Tracks if the player can take actions
end_game = False          # Tracks if the end game is reached
scoring = False           # Tracks if scoring can happen
new_game = False          # Allows for a new game
betting = True            # Tracks if the user is in betting stage or not
input_active = False      # Allows user to enter bet amount if active
user_text = ''            # User input into betting text inbox
round_bet = 0             # User betting amount
warning_status = -1       # Tracks the warning message to be displayed
warning_texts = ["You don't have enough chips to place this bet!",
                 "Please make a bet before beginning round!",
                 "You don't have enough chips to double your bet",
                 "Please only add chips when your remaining chips is less than 500"]
results = False           # Display game summary when user clicks 'Summary'
round_message = ''        # Message that displays results at end of each round

# Initialize variables that update/reset each round
dealer_hand = []
player_hand = []
player_score = 0
dealer_score = 0

# Set up display, caption, clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack game")
clock = pygame.time.Clock()


def make_button(x, y, w, h, curr_text):
    temp = pygame.draw.rect(screen, white, [x, y, w, h], 0, 5)
    pygame.draw.rect(screen, red, [x, y, w, h], 3, 5)
    temp_text = button_font.render(curr_text, True, black)
    screen.blit(temp_text, (x + 35, y + 20))
    return temp


# Button method
def make_buttons(betting_status, playing_status, curr_player, new_game_status, end_game_status):
    """
    Creates interactive buttons based on game status.
    Args:
        betting_status (bool): whether betting is in session
        playing_status (bool): whether round has started
        new_game_status (bool): whether new game is being called
        curr_player (object): Current player.
    Returns:
        list: Interactive buttons for game actions.
    """
    if end_game_status:
        return
    button_list = []
    if betting_status:
        bet = make_button(550, 50, 300, 100, 'BET')
        button_list.append(bet)
        add_chips = make_button(150, 700, 300, 100, 'ADD CHIPS')
        button_list.append(add_chips)
    if not playing_status:
        deal = make_button(150, 50, 300, 100, 'DEAL')
        button_list.append(deal)
    else:
        # Implement hit button
        hit = make_button(50, 700, 300, 100, 'HIT')
        button_list.append(hit)
        # Implement stand button
        stand = make_button(350, 700, 300, 100, 'STAND')
        button_list.append(stand)
        # Implement Double button
        double = make_button(650, 700, 300, 100, 'DOUBLE')
        button_list.append(double)
        # Display records
        records = curr_player.get_records()
        score_text = game_font.render(f'Wins: {records[0]} Losses: {records[1]} Draws: {records[2]}', True, white)
        screen.blit(score_text, (15, 840))
    if new_game_status:
        next_game = make_button(350, 50, 300, 100, 'NEW GAME')
        button_list.append(next_game)
    summary = make_button(550, 850, 300, 100, 'Summary')
    button_list.append(summary)
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
    Args:
        text (str): The text to be displayed.
        x (int): The x-coordinate for the text.
        y (int): The y-coordinate for the text.
    """
    screen.blit(text_font.render(text, True, black), (x, y))


def can_bet(curr_chips, intended_bet):
    """
    Determines if a given bet is valid
    Args:
        curr_chips (int): number of chips a player has
        intended_bet: the amount of chips that player tries to put down
    Returns:
        bool: whether a given bet can be made
    """
    if curr_chips < intended_bet:
        return False
    else:
        return True


# Variable to determine if the game is running
running = True

player = Player(500, 0)


# Main game loop for when the game is running
def deal_cards(curr_dealer_hand, curr_player_hand, curr_deck):
    """
    Deals two cards each to the dealer and the player.
    Args:
        curr_dealer_hand (list): The current hand of the dealer.
        curr_player_hand (list): The current hand of the player.
        curr_deck (Deck): The deck of cards being used.
    """
    for i in range(2):
        curr_dealer_hand.append(curr_deck.deal_card())
        curr_player_hand.append(curr_deck.deal_card())


def draw_score(curr_score, x, y, text):
    """
    Draws the score of a hand on the game screen.
    Args:
        curr_score (int): The score to be displayed.
        x (int): The x-coordinate for the score.
        y (int): The y-coordinate for the score.
        text (str): Additional text to display alongside the score.
    """
    screen.blit(text_font.render(f'{text} [{curr_score}]', True, black), (x, y))


def display_results():
    """
    Displays the summary of the game, including chips added, 
    total chips, net earnings, and win/loss/draw records.
    """
    screen.blit(game_font.render('Summary', True, black), (400, 100))
    screen.blit(game_font.render(f'Chips added: {player.bought_chips}', True, black), (100, 200))
    screen.blit(game_font.render(f'Chips total: {player.chips}', True, black), (100, 300))
    screen.blit(game_font.render(f'Net earnings: {player.chips - player.bought_chips}', True, black), (100, 400))
    screen.blit(game_font.render(f'Win/loss/draw: {player.records[0]}/{player.records[1]}/{player.records[2]}', True, black), (100, 500))
    screen.blit(game_font.render(f'Win rate: {player.win_probability()*100}%', True, black), (100, 600))


while running:
    # Set game frame rate
    timer.tick(fps)

    # Fill background
    screen.fill(green)

    # Install buttons
    buttons = make_buttons(betting, playing, player, new_game, results)

    # Display total chips
    if betting or playing:
        display_text(f'Available chips: {player.chips}', 100, 900)

    if results:
        display_results()

    # If a new round is started
    if playing:
        display_text("Dealer's hand", 150, 100)
        display_text("Player's hand", 690, 100)
        display_hand(player_hand, 600, 200)
        dealer_score = calc_hand(dealer_hand)
        if not can_act:       # Player turn finishes
            if dealer_score < 17:       # Dealer hits when value is < 17
                dealer_hand.append(deck.deal_card())
            else:
                end_game = True       # Ready to be settled
                screen.blit(game_font.render(round_message, True, black), (100, 600))
            display_hand(dealer_hand, 100, 200)     # Reviews dealer's hidden card
            draw_score(dealer_score, 150, 550, "Dealer score")
        else:         # Display dealer's hidden card
            display_hand(dealer_hand, 100, 200, True)
        player_score = calc_hand(player_hand)
        draw_score(player_score, 650, 550, "Player score")
        display_text(f'Bet this round: {round_bet}', 650, 620)

    # User is entering bet amount
    if input_active:
        display_text(f'Please enter amount you want to bet: {user_text}', 100, 200)

    # Display warning message
    if warning_status >= 0:
        display_text(warning_texts[warning_status], 100, 150)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if buttons[-1].collidepoint(event.pos):
                results = True
                playing = False
                dealer_hand = []
                player_hand = []
                can_act = False
                betting = False
                end_game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if betting:
                if buttons[2].collidepoint(event.pos):
                    warning_status = 1
                    input_active = False
                elif buttons[0].collidepoint(event.pos):
                    input_active = True
                    warning_status = -1
                elif buttons[1].collidepoint(event.pos):
                    if player.chips < 500:
                        player.add_chips(500)
                        warning_status = -1
                    else:
                        warning_status = 3
                    input_active = False
                else:
                    input_active = False
            elif not playing:
                if buttons[0].collidepoint(event.pos):
                    playing = True
                    dealer_hand = []
                    player_hand = []
                    deal_cards(dealer_hand, player_hand, deck)
                    can_act = True
                    scoring = False
            else:
                if buttons[0].collidepoint(event.pos) and player_score < 21 and can_act:
                    warning_status = -1
                    player_hand.append(deck.deal_card())
                elif buttons[1].collidepoint(event.pos):
                    warning_status = -1
                    can_act = False
                elif buttons[2].collidepoint(event.pos) and player_score < 21 and can_act and len(player_hand) == 2:
                    if can_bet(player.chips, round_bet):
                        player_hand.append(deck.deal_card())
                        player.bet(round_bet)
                        round_bet = round_bet * 2
                        can_act = False
                    else:
                        warning_status = 2
                elif len(buttons) == 5:
                    if buttons[3].collidepoint(event.pos):
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
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    round_bet = int(user_text)
                    if can_bet(player.chips, round_bet):
                        betting = False
                        player.bet(round_bet)
                    else:
                        round_bet = 0
                        warning_status = 0
                    input_active = False
                    user_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
    # If player has reached 21 after hitting
    if can_act and player_score >= 21:
        can_act = False

    # Perform bet settling
    if end_game and scoring is False:
        new_game, round_message = settle_bets(player_hand, dealer_hand, player, round_bet)
        scoring = True

    # Update portion of the screen
    pygame.display.flip()

# Quit the module
pygame.quit()
