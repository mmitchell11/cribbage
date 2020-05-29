def median(lst):
    n = len(lst)
    s = sorted(lst)
    return (sum(s[n//2-1:n//2+1])/2.0, s[n//2])[n % 2] if n else None

def mean(lst):
    n = len(lst)
    s = sum(lst)
    return round(1000.0*s/n)/1000.0 if n else None

def analyze_all_hands(dist_ranks_points):
    for hand, hand_values in dist_ranks_points.iteritems():
        # get stats with no flushes
        avg_no_flush = mean(hand_values['no_flush'])
        median_no_flush = median(hand_values['no_flush'])
        min_no_flush = min(hand_values['no_flush'])
        max_no_flush = max(hand_values['no_flush'])
        
        # get stats with flushes
        avg_w_flush = 0
        median_w_flush = 0
        min_w_flush = 0
        max_w_flush = 0
        if hand_values['flush']:
            avg_w_flush = mean(hand_values['flush'])
            median_w_flush = median(hand_values['flush'])
            min_w_flush = min(hand_values['flush'])
            max_w_flush = max(hand_values['flush'])

        # print out stats
        hand_string = ''
        for card in hand:
            hand_string += RANK_TO_TYPE[card]
        print hand_string,"|",avg_no_flush,"|",median_no_flush,"|",min_no_flush,"|",max_no_flush,"|",avg_w_flush,"|",median_w_flush,"|",min_w_flush,"|",max_w_flush

