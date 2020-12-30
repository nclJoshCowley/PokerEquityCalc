#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pokerequitycalc.config import WHEEL
from collections import Counter

def classify_hand(*args):
    """
    TODO
    """    
    # '++' / '--' means yes / no to above and [] indicates return value
    # Flush?
    # ++ Broadway straight?
    # ++ ++ [9, Royal flush]
    # ++ -- Straight?
    # ++ -- ++ [8, Straight flush]
    # ++ -- -- [5, Flush]
    # -- Straight?
    # -- ++ [4, Straight]
    # -- ...
    # 
    # raw_counts
    # = [4, 1]          [7, Four of a kind]
    # = [3, 2]          [6, Full house]
    # = [3, 1, 1]       [3, Three of a kind]
    # = [2, 2, 1]       [2, Two pair]
    # = [2, 1, 1, 1]    [1, One pair]
    # = [1, 1, 1, 1, 1] [0, High card]
    assert len(args) == 5, "Expected 5 card objects"
    
    # Straight check happens twice, store result
    (is_straight, straight_score) = check_straight(*args)
    
    if check_flush(*args):
        if is_straight:
            if all(c.val in (14, 13, 12, 11, 10) for c in args):
                return 9 # "Royal flush"
            else:
                return 8 + straight_score # "Straight flush"
        else:
            sub_score = float("0." + "".join(
                str(c.val).zfill(2) for c in sorted(args, reverse=True)))
            return 5 + sub_score # "Flush"
    elif is_straight:
        return 4 + straight_score # "Straight"
    else:
        # Score hands based on unique cards, sorted by occurrence
        # so AAAA2 (7.1402) > 2222A (7.0214)
        counts = Counter(c.val for c in args).most_common(5)
        counts.sort(key = lambda x : (x[1], x[0]), reverse = True)
        
        ranks, freq = zip(*counts)
        sub_score = float("0." + "".join(str(r).zfill(2) for r in ranks))
        
        if 4 in freq:
            return 7 + sub_score # "Four of a kind"
        elif 3 in freq:
            if 2 in freq:
                return 6 + sub_score # "Full house"
            else:
                return 3 + sub_score # "Three of a kind"
        elif 2 in freq:
            if sum(f == 2 for f in freq) == 2:
                return 2 + sub_score # "Two pair"
            else:
                return 1 + sub_score # "One pair"
        else:
            return sub_score # "High card"
        
def check_straight(*args):
    assert len(args) == 5, "Expected 5 objects"
    vals = set(c.val for c in args)
    if len(vals) == 5 or min(vals) <= 10:
        if all(i in vals for i in range(min(vals), min(vals)+5)):
            return True, 0.01 * max(args).val
        elif all(i in vals for i in WHEEL):
            return True, 0.05
    return False, None
    
def check_flush(*args):
    return len(set(c.suit for c in args)) == 1

