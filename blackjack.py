import random
import matplotlib.pyplot as plt

threshold_hard = 1
double_down = 1

def new_deck():
    deck = []
    for i in range (0,4):
        for j in range (2,10):
            deck.append(j)     # 4 of 2-9 (32)
        deck.append(-1)        # 4 of Ace (4)
    for i in range (0,16):
        deck.append(10)        # 16 of 10 (16)
    random.shuffle(deck)
    return deck

def init_game(deck):
    dealer_card = []
    player_card = []
    dealer_card.append(deck.pop())
    dealer_card.append(deck.pop())
    player_card.append(deck.pop())
    player_card.append(deck.pop())
    return dealer_card, player_card

# return all possible hand values that are valid as a list
def hand_value(cards):
    # first sum all fixed values
    fixed_value = 0
    for v in cards:
        if (v!=-1):
            fixed_value = fixed_value + v
    num_ace = cards.count(-1)
    # if dead for sure, return empty list
    if (fixed_value + num_ace > 21):
        return []
    # if no ace cards, return fixed value
    if (num_ace == 0):
        return [fixed_value]
    # if there are ace cards, calculate all valid values after adding fixed_value
    ace_values = []   
    for i in range (0,num_ace+1):
        v = 10 * i + 1 * (num_ace-i)
        ace_values.append(v)
    result = []
    for v in ace_values:
        if v+fixed_value <= 21:
            result.append(v+fixed_value)

    return result

def check_natural(dealer_hand, player_hand):
    dealer_hand = hand_value(dealer_card)
    player_hand = hand_value(player_card)
    if (dealer_hand[-1] == 21 and player_hand[-1] < 21):
        return "Dealer"
    if (dealer_hand[-1] < 21 and player_hand[-1] == 21):
        return "Player"
    if (dealer_hand[-1] == 21 and player_hand[-1] == 21):
        return "Draw"
    if (dealer_hand[-1] < 21 and player_hand[-1] < 21):
        return "None"
    return False

def soft_threshold_draw(deck, cards, threshold):
    hand = hand_value(cards)
    while (hand != [] and hand[0] < threshold):
        cards.append(deck.pop())
        hand = hand_value(cards)

def hard_threshold_draw(deck, cards, threshold):
    hand = hand_value(cards)
    while (hand != [] and hand[0] <= 11 and hand[-1] < threshold):
        cards.append(deck.pop())
        hand = hand_value(cards)

if __name__ == "__main__":
    dealer_threshold = 17
    num_games = 10000
    thresholds = [i for i in range(11,20)]
    profits = []
    for player_threshold in thresholds:
        player_profit = 0
        for games in range (0,num_games):
            # start with a bet of 1
            bet = 1
            # each game reset deck
            deck = new_deck()
            # deal initial cards
            dealer_card, player_card = init_game(deck)
            # check natural
            natural = check_natural(dealer_card, player_card)
            if (natural == "Dealer"):
                player_profit -= bet
                continue
            if (natural == "Player"):
                player_profit += bet
                continue
            if (natural == "Draw"):
                continue
            # player's turn
            if (threshold_hard):
                hard_threshold_draw(deck, player_card, player_threshold)
            else:
                soft_threshold_draw(deck, player_card, player_threshold)
            player_hand = hand_value(player_card)
            if (player_hand == []):
                player_profit -= bet
                continue
            if (double_down):
                if (player_hand[-1] >= 19):
                    bet *= 2
            # dealer's turn
            soft_threshold_draw(deck, dealer_card, dealer_threshold)
            dealer_hand = hand_value(dealer_card)
            if (dealer_hand == []):
                player_profit += bet
                continue
            # final hand values
            player_final = player_hand[-1]
            dealer_final = dealer_hand[-1]
            if (player_final == 21 or player_final > dealer_final):
                player_profit += bet
            elif (dealer_final > player_final):
                player_profit -= bet
        profits.append(player_profit)
        #print("stand when min hand value is " + str(player_threshold)  +" player profit is " + str(player_profit))
    plt.plot(thresholds, profits)
    plt.xlabel('Thresholds')
    plt.ylabel('Profits')
    if (threshold_hard == 0):
        plt.title('Soft Threshold')
        plt.savefig('soft_threshold.png')
    elif double_down == 0:
        plt.title('Hard Threshold')
        plt.savefig('hard_threshold.png')
    else:
        plt.title('Hard Threshold + Double Down')
        plt.savefig('double_down.png')
