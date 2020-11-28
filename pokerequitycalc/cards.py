#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Counter
import config

# %%
class Card:
    """
    TODO: Documentation. Single card.
    """
    
    def __init__(self, card_str):
        assert len(card_str) == 2, "Input not 2 characters: " + card_str
        assert card_str[0] in config.ALL_CARDS, "Card not found: " + card_str
        assert card_str[1] in config.ALL_SUITS, "Suit not found: " + card_str
        
        # Convert strings to values and 1-length lists to int
        self.card = [i for i, v in enumerate(config.ALL_CARDS) 
                     if v == card_str[0]]
        self.suit = [i for i, v in enumerate(config.ALL_SUITS) 
                     if v == card_str[1]]
        self.card = self.card[0]
        self.suit = self.suit[0]
    
    def __repr__(self):
        return "{}{}".format(config.ALL_CARDS[self.card], config.ALL_SUITS[self.suit])
    
    def __lt__(self, other):
        return (self.card < other. card)

    def __le__(self, other):
        return (self.card <= other. card)
    
    def __gt__(self, other):
        return (self.card > other. card)
    
    def __ge__(self, other):
        return (self.card >= other. card)
    
    def __eq__(self, other):
        return (self.card == other. card)
    
    def __ne__(self, other):
        return (self.card != other. card)

# %%    
class Hand:
    def __init__(self, inp):
        # Overload 1, inp is a string such as "Ah 2h 3h 4h 5h".
        if isinstance(inp, str):
            try:
                self.cards = [Card(x) for x in inp.split()]
            except:
                raise Exception("Couldn't parse hand string:" + inp)
        # Overload 2, inp is a list of Card objects.
        elif isinstance(inp, list):
            assert len(inp) == 5, "Expected 5 card objects got" + len(inp)
            if all(map(lambda obj: isinstance(obj, Card), inp)):
                self.cards = inp
            else:
                raise TypeError("Not all list elements were of type Card")
        else:
            raise Exception("Couldn't read cards as string or list")
        self.cards.sort()
        
        self.vals = [x.card for x in self.cards]
        self.suits = [x.suit for x in self.cards]
        
        counter = Counter(self.vals)
        self.counts = [counter[x] for x in range(13)]
        
        self.score = self.get_score()
        
    def __repr__(self):
        return "{}\n {}".format(
            config.ALL_HANDS[self.score],
            str([self.cards[i] for i in range(4,-1,-1)]))
    
    def is_four_of_a_kind(self):
        return (4 in self.counts)
    
    def is_full_house(self):
        return ((3 in self.counts) and (2 in self.counts))
    
    def is_flush(self):
        return (len(set(self.suits)) == 1)
    
    def is_broadway_straight(self):
        return (self.vals == list(range(8,13)))
    
    def is_straight(self):
        wheel = [0, 1, 2, 3, 12]
        consec = list(range(min(self.vals), max(self.vals) + 1))
        return (self.vals == wheel or self.vals == consec)
    
    def is_three_of_a_kind(self):
        return (3 in self.counts)

    def is_two_pair(self):
        return (2 == sum([c == 2 for c in self.counts]))
    
    def is_one_pair(self):
        return (2 in self.counts)
    
    # '++', '--' means yes, no to above [] indicates return value.
    # Four of a kind?
    # ++ [Four of a kind]
    # 
    # Full house?
    # ++ [Full house]
    # 
    # Flush?
    # ++ Straight?
    # ++ ++ Broadway straight?
    # ++ ++ ++ [Royal flush]
    # ++ ++ -- [Straight flush]
    # ++ -- [Flush]
    #
    # Straight?
    # ++ [Straight]
    #
    # Max count?
    # =3 [Three of a kind]
    # =2 Second highest count?
    # =2 =2 [Two pair]
    # =2 =1 [One pair]
    # =1 [High card]
    def get_score(self):
        
        is_straight = self.is_straight()
        
        if self.is_four_of_a_kind():
            return 7
        elif self.is_full_house():
            return 3
        elif self.is_flush():
            if is_straight:
                if self.is_broadway_straight():
                    return 9
                else:
                    return 8
            else:
                return 5
        elif is_straight:
            return 4
        elif self.is_three_of_a_kind():
            return 3
        elif self.is_two_pair():
            return 2
        elif self.is_one_pair():
            return 1
        else:
            return 0

        
# %%
# hand = Hand("Ah 2h 3h 4h 5h")
hand = Hand("Ah Kh Qh Jh Ts")
print(hand.is_straight())
print(hand.is_flush())
print(hand)
    
print(Hand("Ah Kh Qh Jh Ts"))
print(Hand("Ah Kh Qh Jh Th"))
print(Hand("Ah Kh Qh Jh 9h"))
