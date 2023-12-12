# Software Carpentry Final Project
## Section 1 Initializing deck
1. Creating 4 decks with 52 cards
2. Randomly shuffle decks in the beginning
3. Keep track of dealt cards, reshuffle when remaining card < 0
## Section 2 Initializing game
1. At the beginning of the game, ask player for # of computer players (5 player max)
2. Assign player 500 chips
3. Ask player to choose AI difficulty (optional)
## Section 3 Placing bets and dealing
1. At beginning of each game, ask player if they want more chips
2. Ask player to place bets
3. Deal 1 card face up to each player
4. Deal 1 card face up to players and 1 card face down to dealer
## Section 4 Play the hand
1. When it is player's turn, ask player for options (hit/stand/double)
  1.5 When the player's card values > 21, assign "bust" to the player
2. Play other player's cards with AI logic
3. Play dealer's hand (keep hitting until 17 is reached)
## Section 5 Settlement
1. Players who went bust have their bets taken
2. Players who score Ace+face card gets 1.5*bet
3. If dealer rolls Ace+face, all players without Ace+face loses their bets, and the rest are a tie
4. For all other players, calculate bets based on card values
## Section 6
1. Use pygame module to create GUI for the game
2. Create interface with buttons including chip management, difficulty selection, player selection etc.
3. Create interface for betting options
4. Create interface for game round (hit/stand/double etc.)
5. Load unique images of 52 cards and be able to display the hand
