# my-blackjack
some experiments on blackjack strategies

I make the following assumptions with my simulations:
• One player and one dealer are in the game
• One deck of 52 cards are used
• After each game, the deck is reset and shued
• The dealer keeps hitting until a soft 17
• The initial bet is 1 dollar, and player can double down at most once
• Each strategy is played with 10000 games to calculate the total prot for
comparisons

The following 3 sets of experiments are run:
• Soft threshold : similar to how dealer stops at a soft 17, I experiment with
player stopping at different soft thresholds
• Hard threshold : while guaranteeing not to risk exploding, also set a hard
threshold above which the player will stop drawing
• Double Down : if the player has a good hand value, double the bets for
more potential profit


