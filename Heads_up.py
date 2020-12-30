#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Typical use-case. All in pre, 1v1 equity?

@author:   Josh Cowley
@email:    j.cowley1@ncl.ac.uk
Created:   Tue Dec 22 17:01:20 2020
Modified:  
"""

from pokerequitycalc.classes import Card
from pokerequitycalc.classes import Deck

from pokerequitycalc.scoring import classify_hand

import itertools as it

# %%
def find_best_hand(*args):
    """Takes some cards and produces the best possible hand.
    Parameters
    ----------
    args : Multiple 'Card' type.
        These cards form the sample of cards to use to attempt to make the
        best hand possible.
    
    Returns
    -------
    TODO
    
    """
    assert len(args) >= 6, "Less than 6 cards provided."
    
    combos = it.combinations(args, 5)
    
    # Look at first combo 
    best_hand = next(combos)
    best_score = classify_hand(*best_hand)
    
    # Search for better combos
    for c in combos:
        cur_score = classify_hand(*c)
        if cur_score > best_score:
            best_hand, best_score = c, cur_score
            
    return best_hand, best_score


# %%
def calc_equity(p1, p2, board, deck = None):
    """TODO
    Parameters
    ----------
    p1:
    p2:
    board:
    deck: 
    
    Returns
    -------
    TODO
    """
    if deck is None:
        deck = Deck()
    
    deck.remove_card(*p1, *p2, *board)
    n_draws = 5 - len(board)
    n_trials = sum(1 for _ in it.combinations(deck.cards, n_draws))
    
    p1_avail_cards = ((*p1, *board, *i) for i in it.combinations(deck.cards, n_draws))
    p2_avail_cards = ((*p2, *board, *i) for i in it.combinations(deck.cards, n_draws))

    p1_scores = (find_best_hand(*i)[1] for i in p1_avail_cards)
    p2_scores = (find_best_hand(*i)[1] for i in p2_avail_cards)
    
    return sum(1 if s1>s2 else (0.5 if s1==s2 else 0)
               for s1,s2 in zip(p1_scores, p2_scores)) / n_trials

# %% 
if __name__ == "__main__":
    p1_AKs = (Card("Ah"), Card("Kh"))
    p2_55 = (Card("5s"), Card("5d"))
    runout = tuple(Card(st) for st in ("Qh", "Jh", "5c"))
    
    p1_equity = calc_equity(p1_AKs, p2_55, runout)
    
    print("Player 1 Equity {} - {:.2%}".format(p1_AKs, p1_equity))
    print("Player 2 Equity {} - {:.2%}".format(p2_55, 1 - p1_equity))
