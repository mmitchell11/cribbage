import random
import datetime
from deal import deal_all_4_w_cut
from cribbage import count_hands



if __name__ == '__main__':
    # Running this script should evaluate all possible 5 card combinations for cribbage points
    # The results should match what is found here" https://en.wikipedia.org/wiki/Cribbage_statistics#Odds

    print("{}::  {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Start"))

    # To check for all possible 4 card hands with cuts
    dealt_hands = deal_all_4_w_cut()
    final_hands = dealt_hands


    print("{} hands".format(len(final_hands)))
    count_hands(final_hands)


    print("{}::  {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "End"))







