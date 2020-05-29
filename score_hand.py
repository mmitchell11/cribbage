from cards import FULL_DECK

def check_fifteens(hand):
    fifteen_combos = []
    
    # get all 2 and 3 card cominations
    for i in range(5):
        for j in range(5):
            if j > i:
                if FULL_DECK[hand[i]]['count'] + FULL_DECK[hand[j]]['count'] == 15:
                    fifteen_combos.append([hand[i],hand[j]])

                card_nums = range(5)
                card_nums.remove(i)
                card_nums.remove(j)
                x,y,z = card_nums

                if FULL_DECK[hand[x]]['count'] + FULL_DECK[hand[y]]['count'] + FULL_DECK[hand[z]]['count'] == 15:
                    fifteen_combos.append([hand[x],hand[y],hand[z]])

    # get all 4 and 5 card combinations
    total_sum = 0
    for k in range(5):
        total_sum += FULL_DECK[hand[k]]['count']

        card_nums = range(5)
        card_nums.remove(k)
        a,b,c,d = card_nums

        if FULL_DECK[hand[a]]['count'] + FULL_DECK[hand[b]]['count'] + FULL_DECK[hand[c]]['count'] + FULL_DECK[hand[d]]['count'] == 15:
            fifteen_combos.append([hand[x],hand[y],hand[z]])

    if total_sum == 15:
        fifteen_combos.append(hand)

    return fifteen_combos

def check_runs(rank_counts):
    # initialize tracking
    ordered_ranks = rank_counts.keys()
    ordered_ranks.sort()
    prior_rank = ordered_ranks[0]
    consecutive = 1
    max_run = 1
    first_in_run = -1

    # loop over remaining ranks to check for runs
    for i in range(1,len(ordered_ranks)):
        if ordered_ranks[i] - prior_rank == 1:
            consecutive += 1
            if consecutive > max_run:
                max_run = consecutive
                if consecutive >= 3:
                    first_in_run = i - consecutive + 1
        # reset counter if card not in run
        else:
            consecutive = 1
        prior_rank = ordered_ranks[i]
    
    # initialize counters
    num_runs = 0
    cards_in_run = []
    # add to counters if there is a run
    if max_run >= 3:
        ranks_in_run = ordered_ranks[first_in_run:first_in_run+max_run]
        num_runs = 1
        for rank in ranks_in_run:
            num_runs *= rank_counts[rank]['count']
            cards_in_run.append(rank_counts[rank]['cards'])

    # print (num_runs, max_run, cards_in_run)
    return (num_runs, max_run, cards_in_run)


def analyze_hand(hand):
    # initialize tracking
    rank_counts = {}
    suits = {}
    jacks = []
    cards = hand['hand4'] + hand['cut']
    hand_ranks = []

    for card in hand['hand4']:
        # build dict for pairs
        hand_ranks.append(FULL_DECK[card]['rank'])
        if FULL_DECK[card]['rank'] not in rank_counts:
            rank_counts[FULL_DECK[card]['rank']] = {}
            rank_counts[FULL_DECK[card]['rank']]['count'] = 0
            rank_counts[FULL_DECK[card]['rank']]['cards'] = []
        rank_counts[FULL_DECK[card]['rank']]['count'] += 1
        rank_counts[FULL_DECK[card]['rank']]['cards'].append(card)

        # build dict for flushes
        if FULL_DECK[card]['suit'] not in suits:
            suits[FULL_DECK[card]['suit']] = 0
        suits[FULL_DECK[card]['suit']] += 1

        # build list for right jacks
        if FULL_DECK[card]['rank'] == 11:
            jacks.append(FULL_DECK[card]['suit'])

    # print rank_counts
    # print suits
    # print jacks
    # print hand_ranks
    # check how cut card adds to scoring
    for card in hand['cut']:
        # add to dict for pairs
        if FULL_DECK[card]['rank'] not in rank_counts:
            rank_counts[FULL_DECK[card]['rank']] = {}
            rank_counts[FULL_DECK[card]['rank']]['count'] = 0
            rank_counts[FULL_DECK[card]['rank']]['cards'] = []
        rank_counts[FULL_DECK[card]['rank']]['count'] += 1
        rank_counts[FULL_DECK[card]['rank']]['cards'].append(card)

        # add to possible flush
        if max(suits.values()) == 4 and FULL_DECK[card]['suit'] == suits.keys()[0]:
            suits[FULL_DECK[card]['suit']] += 1

    # check for fifteens and runs
    fifteens = check_fifteens(cards)
    runs = check_runs(rank_counts)

    return fifteens, rank_counts, runs, suits, jacks, hand_ranks

def count_hand(hand):
    fifteens, rank_counts, runs, suits, jacks, hand_ranks = analyze_hand(hand)
    score = 0

    # count number of 15s
    if len(fifteens) > 0:
        # print("{number} fifteens for {score}: {fifteens}".format(number = len(fifteens), score = 2*len(fifteens), fifteens = fifteens))
        score += 2*len(fifteens)

    # count number of pairs
    pairs = 0
    pair_cards = []
    for rank,rank_dict in rank_counts.iteritems():
        if rank_dict['count'] == 2:
            pairs += 1
            pair_cards.append(rank_dict['cards'])
        elif rank_dict['count'] == 3:
            pairs += 3
            pair_cards.append(rank_dict['cards'])
        elif rank_dict['count'] == 4:
            pairs += 6
            pair_cards.append(rank_dict['cards'])
    if pairs > 0:
        # print("{number} pairs for {score}: {pair_cards}".format(number = pairs, score = 2*pairs, pair_cards = pair_cards))
        score += 2*pairs

    # count number and length of runs
    (num_runs, run_length, run_cards) = runs
    if num_runs >= 1:
        run_points = num_runs * run_length
        # print("{number} runs for {score}: {run_cards}".format(number = num_runs, score = run_points, run_cards = run_cards))
        score += run_points

    # count flush points
    has_flush = 0
    for suit in suits:
        if suits[suit] >= 4:
            # print("{num_flush} of a kind for {num_flush}".format(num_flush = suits[suit]))
            has_flush = 1
            score += suits[suit]

    # count right jack
    for jack_suit in jacks:
        if jack_suit == FULL_DECK[hand['cut'][0]]['suit']:
            # print("Right Jack for 1")
            score += 1

    # print("Total Score of {}\n".format(score))
    return score, hand_ranks, has_flush

