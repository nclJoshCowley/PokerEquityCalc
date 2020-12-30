from pokerequitycalc.config import CARDS
from pokerequitycalc.config import SUITS
from pokerequitycalc.scoring import classify_hand

from collections import Counter
import random

# %%
class Card:
    """
    TODO: Documentation. Single card.
    """
    
    def __init__(self, card_str):
        assert len(card_str) == 2, "Input not 2 characters: " + card_str
        assert card_str[0] in CARDS, "Card not found: " + card_str
        assert card_str[1] in SUITS, "Suit not found: " + card_str
        self.val = CARDS[card_str[0]]
        self.suit = SUITS[card_str[1]]
    
    def __hash__(self):
        return hash(str(self.val) + str(self.suit))
    
    def __repr__(self):
        card_str = [s for (s,i) in CARDS.items() if i == self.val]
        suit_str = [s for (s,i) in SUITS.items() if i == self.suit]
        return "{}{}".format(card_str[0], suit_str[0])
    
    def __lt__(self, other):
        return (self.val < other.val)

    def __le__(self, other):
        return (self.val <= other.val)
    
    def __gt__(self, other):
        return (self.val > other.val)
    
    def __ge__(self, other):
        return (self.val >= other.val)
    
    def __eq__(self, other):
        return (self.val == other.val and self.suit == other.suit)
    
    def __ne__(self, other):
        return (self.val != other.val or self.suit != other.suit)


# %%    
class Hand:
    """
    TODO: Documentation. Five cards, with some hand strength.
    """
    
    def __init__(self, *args):
        # Validate input
        # all(map(lambda obj: isinstance(obj, Card), self.cards)):
        assert len(args) == 5, "Expected 5 objects"
        assert len(set(args)) == 5, "Duplicate cards found: " + str(args)
        
        # Classify hand        
        self.score, self._name = classify_hand(*args)
        
        # Sort by occurence on rank-sorted list (e.g. 22AKQ, AQT75, AAAKK)
        counts = Counter(c.val for c in args)
        self.cards = sorted(args,
                            key = lambda c : (counts.get(c.val), c.val),
                            reverse = True)

    def __repr__(self):
        with_sq_brackets = self.cards.__repr__()
        return "{}\n- {}".format(self._name, with_sq_brackets[1:-1])
    
    def __lt__(self, other):
        return (self.score < other.score)

    def __le__(self, other):
        return (self.score <= other.score)
    
    def __gt__(self, other):
        return (self.score > other.score)
    
    def __ge__(self, other):
        return (self.score >= other.score)
    
    def __eq__(self, other):
        return (self.score == other.score)
    
    def __ne__(self, other):
        return (self.score != other.score)

# %%
class Deck:
    """
    TODO: Documentation. Deck of cards
    """
    
    def __init__(self):
        self.cards = [Card(str(v) + str(s)) 
                      for v in CARDS.keys() 
                      for s in SUITS.keys()]
        self.cards.sort(reverse = True)
        self.n_cards = len(CARDS) * len(SUITS)
        
    def __repr__(self):
        return "{} cards remain.\n{}".format(
            self.n_cards,
            ", ".join([str(c) for c in self.cards])
            )
    
    def remove_card(self, *args):
        for rem_card in args:
            assert isinstance(rem_card, Card), "Argument not of 'Card' type."
            assert rem_card in self.cards, "Card not found in deck."
            self.cards.remove(rem_card)
            self.n_cards -= 1
        
    def draw_cards(self, n):
        assert n <= self.n_cards, "Not enough cards left in the deck."
        random_cards = random.sample(self.cards, n)
        for rc in random_cards:
            self.remove_card(rc)
        return random_cards
