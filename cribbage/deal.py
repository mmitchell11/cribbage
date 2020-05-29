import random
from cards import FULL_DECK

def deal_lots_4_w_cut(num_hands):
    # deal num_hands number of 4-player, 4-card hands
    hands = {}
    for g in range(num_hands):
        dist_cards = FULL_DECK.keys()
        hands[g*4] = {'hand4': [], 'cut': []}
        hands[g*4+1] = {'hand4': [], 'cut': []}
        hands[g*4+2] = {'hand4': [], 'cut': []}
        hands[g*4+3] = {'hand4': [], 'cut': []}
        for i in range(16):
            chosen_card = random.choice(dist_cards)
            hands[g*4+i%4]['hand4'].append(chosen_card)
            dist_cards.remove(chosen_card)

        cut_card = random.choice(dist_cards)
        for j in range(4):
            hands[g*4+j]['cut'].append(cut_card)

    return hands

def deal_all_4_w_cut():
    # deal all possible 4 card combinations
    dist_cards = FULL_DECK.keys()
    hands = {}
    counter = 0
    for i in range(52):
        for j in range(52):
            for k in range(52):
                for l in range(52):
                    if j > i and k > j and l > k:
                        for c in range(52):
                            if c != i and c != j and c != k and c != l:
                                hands[counter] = {'hand4': [dist_cards[i],dist_cards[j],dist_cards[k],dist_cards[l]], 'cut': [dist_cards[c]]}
                                counter += 1
    return hands

def deal_lots_6_no_cut(num_hands):
    # deal num_hands number of 2-player, 6-card hands
    hands = {}
    for g in range(num_hands):
        dist_cards = FULL_DECK.keys()
        hands[g*2] = {'hand6': [], 'cut': []}
        hands[g*2+1] = {'hand6': [], 'cut': []}
        for i in range(12):
            chosen_card = random.choice(dist_cards)
            hands[g*2+i%2]['hand6'].append(chosen_card)
            dist_cards.remove(chosen_card)


    return hands

def add_cut(hand):
    possible_cut_cards = []
    for card in FULL_DECK:
        if card in hand['hand4']:
            continue
        possible_cut_cards.append(card)
    cut_card = random.choice(possible_cut_cards)
    hand['cut'] = [cut_card]
    return hand
