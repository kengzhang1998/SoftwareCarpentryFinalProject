# Software Carpentry Final Project
## Section 1 Initializing game
1. Creating 4 decks with 52 cards
2. Randomly shuffle decks in the beginning
3. Keep track of dealt cards, add 4 decks and reshuffle when remaining card is 0
4. Create player object and assign 500 chips
## Section 2 Placing bets
1. At beginning of each game, player can add 500 chips if their current chip amount is less than 500
2. Ask the player to place bets (check if the bet is valid)
3. Player can click 'Deal' button to proceed to playing
## Section 3 Dealing
1. Deal 1 card face up the player and the dealer
2. Deal 1 card face up to the player and 1 card face down to dealer
3. Display cards
## Section 4 Play the hand
1. When it is player's turn, ask player for options (hit/stand/double)
  1.1 Hit allows player to add cards if total score is less than 21
  1.2 If playing presses 'double' button, player draws one card and ends the turn
  1.3 When player presses 'stand' button, player ends the turn
2. Dealer automatically fills dealer's hand (keep hitting until 17 is reached or bust)
3. Display results
## Section 5 Settlement
1. Player who went bust have their bets taken
2. Player who score Ace+face card gets 2.5*bet
3. If dealer rolls Ace+face, all players without Ace+face loses their bets, and the rest are a tie (bet returns to player)
4. For all other conditions, calculate bets based on card values
5. A 'new game' button can be pressed to repeat steps 2-5 
## Section 6 Summary
1. Pressing the 'summary' button at any time will cause the game to end and the settlement screen to appear
2. Results including wins, losses, win rate, earned or lost money will be displayed
