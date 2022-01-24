value_dict = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

def eval_hand(hand):
    # Return ranking: high card = 0, ... royal flush = 9
    # Also return high card(s) of rank

    values = sorted([c[0] for c in hand])
    suits = [c[1] for c in hand]
    straight = (values == range(min(values), max(values)+1))
    flush = all(s == suits[0] for s in suits)

    # Should not occur (too rare)
    if straight and flush:
        if values[0] == 10:
            return 9, None
        else: return 8, max(values)

    pairs = []
    pair_present = False
    three_of_a_kind = False
    three_value = None
    for v in set(values):
        if values.count(v) == 4:
            return 7, v
        if values.count(v) == 3:
            three_of_a_kind = True
            three_value = v
        if values.count(v) == 2:
            pair_present = True
            pairs.append(v)

    if three_of_a_kind and pair_present: return 6, (three_value, pairs[0])
    if flush: return 5, None
    if straight: return 4, max(values)
    if three_of_a_kind: return 3, three_value
    if len(pairs) == 2: return 2, pairs
    if len(pairs) == 1: return 1, pairs[0]
    return 0, max(values)

def tiebreaker(hand1, hand2, hand1_info, hand2_info):
    # Return True if player 1 wins
    #print(hand1, hand1_info, hand2, hand2_info)
    assert(type(hand1_info) != list) # Shortcut, no identical Two Pairs
    assert(type(hand1_info) == int) # Flushes (None type) can't be compared
    if hand1_info != hand2_info:
        return (hand1_info > hand2_info)

    values1 = sorted((c[0] for c in hand1), reverse=True)
    values2 = sorted((c[0] for c in hand2), reverse=True)
    print(values1, values2, values1 > values2)
    return (values1 > values2)


player1_wins = 0
ranks1 = [0]*10
ranks2 = [0]*10
with open("p054_poker.txt") as f:
    for line in f:
        s = line.split(' ')
        line_pairs = []
        for card in s:
            try:
                value = int(card[0])
            except:
                value = value_dict[card[0]]

            line_pairs.append((value, card[1]))

        hand1 = line_pairs[:5]
        hand2 = line_pairs[5:]
        hand1_rank, hand1_info = eval_hand(hand1)
        hand2_rank, hand2_info = eval_hand(hand2)

        ranks1[hand1_rank] += 1
        ranks2[hand2_rank] += 1

        if hand1_rank > hand2_rank:
            player1_wins += 1

        elif hand1_rank == hand2_rank and tiebreaker(hand1, hand2, hand1_info, hand2_info):
            player1_wins += 1


#print(eval_hand([(2,'D'), (2,'D'), (1,'H'), (4,'D'), (2,'D')]))
print(ranks1)
print(ranks2)
print(player1_wins)