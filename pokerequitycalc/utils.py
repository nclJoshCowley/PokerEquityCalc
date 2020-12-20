from pokerequitycalc.config import CARDS
from pokerequitycalc.config import SUITS
from pokerequitycalc.classes import Card
from pokerequitycalc.classes import Hand
from pokerequitycalc.classes import Deck

import itertools as it

# %%
def find_best_hand(cards):
    """Takes some cards and produces the best possible hand.
    
    Parameters
    ----------
    cards : list of 'Card' type.
        These cards form the sample of cards to use to attempt to make the
        best hand possible.

    Returns
    -------
    best_hand : 'Hand' type
        Returns the best hand as an object where individual attributes 
        (such as score) can be accessed via that object.

    """
    assert len(cards) >= 6, "Less than 6 hands provided."
    possible_hands = [Hand(list(tt)) for tt in it.combinations(cards, 5)]
    
    best_hand = possible_hands[0]
    for hand in possible_hands:
        if hand.score > best_hand.score:
            best_hand = hand
            
    return best_hand

# %%
if __name__ == '__main__':
    p1 = [Card(st) for st in ("Ah", "Kh")]
    p2 = [Card(st) for st in ("5c", "5s")]
    
    p1_tie_p2 = [0, 0, 0]
    
    n_iter = 1712304
    
    for i in range(n_iter):
        deck = Deck()
        for hc in (p1 + p2):
            deck.remove_card(hc)
        
        board = deck.draw_cards(5)
        p1_best = find_best_hand(p1 + board)
        p2_best = find_best_hand(p2 + board)
        
        if p1_best.score > p2_best.score:
            p1_tie_p2[0] += 1
        elif p1_best.score == p2_best.score:
            p1_tie_p2[1] += 1
        else:
            p1_tie_p2[2] += 1

    equity = [100 * (i / n_iter) for i in p1_tie_p2]
    print(equity)
