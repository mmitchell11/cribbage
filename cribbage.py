import random
import datetime
from cards import FULL_DECK, RANK_TO_TYPE
from stats import analyze_all_hands, mean, median
from deal import deal_lots_4_w_cut, deal_all_4_w_cut, deal_lots_6_no_cut, add_cut
from score_hand import count_hand


def check_all_cuts(hand):
    point_list = []
    possible_cuts = []
    for card in FULL_DECK:
        if card not in hand:
            possible_cuts.append(card)

    for card in possible_cuts:
        score, hand_ranks, has_flush = count_hand({'hand4': hand, 'cut': [card]})
        point_list.append(score)

    return point_list
        


def optimal_discard_6(hand):
    # loop over all possible discard options
    possible_hands_scores = {}
    for i in range(6):
        for j in range(6):
            if j > i:
                possible_hand = []
                counter = -1
                for card in hand['hand6']:
                    counter += 1
                    if counter == i or counter == j:
                        continue
                    possible_hand.append(card)
                
                # get total list of possible scores for that hand
                point_list = check_all_cuts(possible_hand)
                possible_hands_scores[tuple(possible_hand)] = point_list

    max_expected_points = 0
    best_hand = []
    for poss_hand, point_list in possible_hands_scores.iteritems():
        expected_points = mean(point_list)
        # print hand, expected_points
        if expected_points > max_expected_points:
            max_expected_points = expected_points
            best_hand = poss_hand

    discard = list(set(hand['hand6']) - set(best_hand))

    # print("Best Hand = {} for {} points".format(best_hand, max_expected_points))
    return list(best_hand), discard



def discard(hand):
    final_hand, discards = optimal_discard_6(hand)
    # final_hand = dealer_discard_6(hand)
    # final_hand = pone_discard_6(hand)

    return final_hand, discards

def discard_cards(hands):
    final_hands = {}
    crib_hands = {}
    for player,hand in hands.iteritems():
        if player % 1000 == 0:
            print("{}::  {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Discarding Hand {}".format(player)))
        full_hand = {}
        final_hand, discards = discard(hand)

        # print player, hand, final_hand, discards

        full_hand['hand4'] = final_hand
        add_cut(full_hand)
        final_hands[player] = full_hand
        if player/2 not in crib_hands:
            crib_hands[player/2] = {}
            crib_hands[player/2]['hand4'] = []
        crib_hands[player/2]['hand4'].extend(discards)
        if player%2 == 1:
            add_cut(crib_hands[player/2])

    return final_hands, crib_hands

def track_discard_cards(crib_hands):
    crib_cards = {}
    for game, hand in crib_hands.iteritems():
        for card in hand['hand4']:
            if RANK_TO_TYPE[FULL_DECK[card]['rank']] not in crib_cards:
                crib_cards[RANK_TO_TYPE[FULL_DECK[card]['rank']]] = 0
            crib_cards[RANK_TO_TYPE[FULL_DECK[card]['rank']]] += 1

    print("Distribution of cards in crib")
    for card,count in crib_cards.iteritems():
        print card,"|",count

def track_discard_impact(hand, score, discard_crib_points):
    # print hand, score
    for i in range(2):
        discard_cards = hand['hand4'][2*i:2*i+2]
        discard_ranks = []
        discard_string = ''

        suited = False
        first_suit = None
        for card in discard_cards:
            discard_ranks.append(FULL_DECK[card]['rank'])
            if not first_suit:
                first_suit = FULL_DECK[card]['suit']
            elif FULL_DECK[card]['suit'] == first_suit:
                suited = True
        discard_ranks.sort()
        for rank in discard_ranks:
            discard_string += RANK_TO_TYPE[rank]
        if discard_string not in discard_crib_points:
            discard_crib_points[discard_string] = {}
            # True and false for whether the cards are suited or not
            discard_crib_points[discard_string][True] = []
            discard_crib_points[discard_string][False] = []
        discard_crib_points[discard_string][suited].append(score)

    return discard_crib_points


def count_hands(hands):
    point_counts = {}
    dist_ranks_points = {}

    discard_crib_points = {}
    for player,hand in hands.iteritems():
        if player % 1000000 == 0:
            print("{}::  {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Analyzing Hand {}".format(player)))
        score, hand_ranks, has_flush = count_hand(hand)
        if score not in point_counts:
            point_counts[score] = 0
        point_counts[score] += 1

        # to look at the impact of specific discards
        discard_crib_points = track_discard_impact(hand, score, discard_crib_points)

    # # track scoring of all potential 4 card hands
    #     hand_ranks.sort()
    #     hand_ranks_tuple = tuple(hand_ranks)
    #     if hand_ranks_tuple not in dist_ranks_points:
    #         dist_ranks_points[hand_ranks_tuple] = {'flush': [], 'no_flush': []}
    #     if has_flush:
    #         dist_ranks_points[hand_ranks_tuple]['flush'].append(score)
    #     else:
    #         dist_ranks_points[hand_ranks_tuple]['no_flush'].append(score)

    # analyze_all_hands(dist_ranks_points)

    # print out score distribution
    print("Distribution of scores")
    for point,count in point_counts.iteritems():
        print point,"|",count

    print("Impact of throws on crib score")
    for throw_string, score_dict in discard_crib_points.iteritems():
        print throw_string,"|",'suited',"|",len(score_dict[True]),"|",mean(score_dict[True])
        print throw_string,"|",'unsuited',"|",len(score_dict[False]),"|",mean(score_dict[False])


if __name__ == '__main__':
    print("No longer using cribbage.py to run specific scripts")
    







