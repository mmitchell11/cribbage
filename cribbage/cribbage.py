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
    for hand, point_list in possible_hands_scores.iteritems():
        expected_points = mean(point_list)
        # print hand, expected_points
        if expected_points > max_expected_points:
            max_expected_points = expected_points
            best_hand = hand

    # print("Best Hand = {} for {} points".format(best_hand, max_expected_points))
    return list(best_hand)



def discard(hand):
    final_hand = optimal_discard_6(hand)
    # final_hand = dealer_discard_6(hand)
    # final_hand = pone_discard_6(hand)

    return final_hand

def discard_cards(hands):
    final_hands = {}
    for player,hand in hands.iteritems():
        if player % 100 == 0:
            print("{}::  {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Discarding Hand {}".format(player)))
        full_hand = {}
        final_hand = discard(hand)
        full_hand['hand4'] = final_hand
        add_cut(full_hand)
        final_hands[player] = full_hand

    return final_hands


def count_hands(hands):
    point_counts = {}
    dist_ranks_points = {}
    for player,hand in hands.iteritems():
        if player % 1000000 == 0:
            print("{}::  {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Analyzing Hand {}".format(player)))
        score, hand_ranks, has_flush = count_hand(hand)
        if score not in point_counts:
            point_counts[score] = 0
        point_counts[score] += 1

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
    for point,count in point_counts.iteritems():
        print point,"|",count


if __name__ == '__main__':
    print("{}::  {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Start"))
    
    # # To test out things with a bunch of 4 card hands with cut
    # dealt_hands = deal_lots_4_w_cut(2500)
    # final_hands = dealt_hands

    # # To check for all possible 4 card hands with cuts
    # dealt_hands = deal_all_4_w_cut()
    # final_hands = dealt_hands

    # To analyze possible 6 card combinations
    dealt_hands = deal_lots_6_no_cut(10000)
    # print dealt_hands
    final_hands = discard_cards(dealt_hands)
    # print final_hands

    print("{} hands".format(len(final_hands)))

    count_hands(final_hands)
    print("{}::  {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "End"))







