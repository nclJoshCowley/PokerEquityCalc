from pokerequitycalc.config import CARDS
from pokerequitycalc.config import SUITS

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
        return 1000 + (100 * self.suit) + self.val
    
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
    
    _wheel = [CARDS[x] for x in ["A","5","4","3","2"]]
    
    def __init__(self, inp):
        # Overload 1, inp is a string such as "Ah 2h 3h 4h 5h".
        if isinstance(inp, str):
            try:
                self.cards = [Card(x) for x in inp.split()]
            except:
                raise Exception("Couldn't parse hand string:" + inp)
        # Overload 2, inp is a list of Card objects.
        elif isinstance(inp, list):
            if all(map(lambda obj: isinstance(obj, Card), inp)):
                self.cards = inp
            else:
                raise TypeError("Not all list elements were of type Card")        
        # Invalid inp
        else:
            raise Exception("Couldn't read cards as string or list")
        
        # Validate input
        assert len(self.cards) == 5, (
            "Can't make Hand from %i card(s)" % len(self.cards))
        assert len(set(self.cards)) == 5, (
            "Duplicate cards found: " + str(self.cards))
        
        # Dictionary with key : value = card_str : occurences
        counts = Counter([crd.val for crd in self.cards])
        self.counts = {i:v for i,v in counts.items() if v > 0}
        
        # Sort by biggest pair / three of a kind etc. or by value
        if len(self.counts) < 5:
            self.cards.sort(key = lambda x : self.counts[x.val], 
                            reverse = True)
        else:
            self.cards.sort(reverse = True)
        
        # Other attr's
        self._vals = [crd.val for crd in self.cards]
        self.score, self._str = self.classify_hand()
    
    def __repr__(self):
        with_sq_brackets = self.cards.__repr__()
        return "{}\n- {}".format(self._str, with_sq_brackets[1:-1])
    
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
    
    def is_flush(self):
        return (len(set([crd.suit for crd in self.cards])) == 1)
    
    def is_straight(self):
        consec = list(range(max(self._vals), min(self._vals) - 1, -1))
        return (self._vals == self._wheel or self._vals == consec)
        
    def classify_hand(self):
        """
        Should return float reprsenting hand strength
        and string representing name
        """        
        # Create subscore using already *ordered* cards 
        # wheel changed from A5432 to 5432A to account for relative strength
        if self._vals == self._wheel:
            sub_score = 0.0504030214
        else:
            sub_string = "".join([str(x).zfill(2) for x in self._vals])
            sub_score = 1e-10 * int(sub_string)
        
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
            
        is_flush = self.is_flush()
        is_straight = self.is_straight()
        
        if is_flush:
            if self._vals == [14, 13, 12, 11, 10]:
                return 9 + sub_score, "Royal flush"
            elif is_straight:
                return 8 + sub_score, "Straight flush"
            else:
                return 5 + sub_score, "Flush"
        elif is_straight:
            return 4 + sub_score, "Straight"
        else:
            raw_counts = list(self.counts.values())
            raw_counts.sort()
            if raw_counts == [1, 4]:
                return 7 + sub_score, "Four of a kind"
            elif raw_counts == [2, 3]:
                return 6 + sub_score, "Full house"
            elif raw_counts == [1, 1, 3]:
                return 3 + sub_score, "Three of a kind"
            elif raw_counts == [1, 2, 2]:
                return 2 + sub_score, "Two pair"
            elif raw_counts == [1, 1, 1, 2]:
                return 1 + sub_score, "One pair"
            else:
                return 0 + sub_score, "High card"

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
        self.n_cards = len(self.cards)
        
    def __repr__(self):
        return "{} cards remain.\n{}".format(
            self.n_cards,
            ", ".join([str(c) for c in self.cards])
            )
    
    def remove_card(self, rem_card):
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
