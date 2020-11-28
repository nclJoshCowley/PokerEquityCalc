#!/usr/bin/env python
# -*- coding: utf-8 -*-
from class_card import Card

class Hand:
    def __init__(self, cards):
        if isinstance(cards, str):
            try:
                cards_l = [Card(x) for x in cards.split()]
            except:
                raise "Couldn't parse hand string:" + cards
        elif isinstance(cards, list):
            cards_l = cards
        else:
            raise Exception("Couldn't read cards as string or list")
        assert len(cards_l) == 5, "Expected 5 cards not " + str(len(cards_l))
        cards_l.sort(reverse = True)
        self.card_values = [x.card for x in cards_l]
        self.card_suits = [x.suit for x in cards_l]
        self.strength = "Unknown."
        
    def __repr__(self):
        return "TODO"
    
    def is_straight(self):
        is_wheel = self.card_values == [12, 3, 2, 1, 0]
        is_consec = ( self.card_values == 
            list(range(max(self.card_values), min(self.card_values) - 1, -1)) )
        return is_wheel or is_consec
    
    def is_flush(self):
        return len(set(self.card_suits)) == 1
        
# %%
if __name__ == '__main__':
    hand = Hand("Ah 2h 3h 4h 5h")
    print(hand)

