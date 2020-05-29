import random
import datetime
from deal import deal_lots_6_no_cut
from cribbage import count_hands, discard_cards, track_discard_cards



if __name__ == '__main__':
    # Running this script will evaluate options for 6-card cribbage hands (2-player games)
    # To begin, it is purely evaluating hands on how to optimize the points in your hand, without regard for the effect on the crib

    print("{}::  {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Start"))

    # To analyze possible 6 card combinations
    dealt_hands = deal_lots_6_no_cut(10000)
    # dealt_hands = deal_lots_6_no_cut(10)
    # print dealt_hands
    final_hands, crib_hands = discard_cards(dealt_hands)
    # print final_hands


    print("{} hands".format(len(final_hands)))
    # count_hands(final_hands)
    count_hands(crib_hands)
    track_discard_cards(crib_hands)


    print("{}::  {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "End"))







