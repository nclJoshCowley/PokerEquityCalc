from pokerequitycalc.config import CARDS
from pokerequitycalc.config import SUITS
from pokerequitycalc.classes import Card
from pokerequitycalc.classes import Hand

import unittest

class TestHandClass(unittest.TestCase):

    def test_input_str(self):
        h = Hand("Ah Kh Qh Jh Th")
        self.assertEqual([c.val for c in h.cards],
                         [CARDS[x] for x in ["A","K","Q","J","T"]])
        self.assertEqual([c.suit for c in h.cards],
                         [SUITS[x] for x in ["h","h","h","h","h"]])
        
    def test_input_cards(self):
        h = Hand([Card("Ah"), Card("Kh"), Card("Qh"), Card("Jh"), Card("Th")])
        self.assertEqual([c.val for c in h.cards],
                         [CARDS[x] for x in ["A","K","Q","J","T"]])
        self.assertEqual([c.suit for c in h.cards],
                         [SUITS[x] for x in ["h","h","h","h","h"]])
    
    def test_too_few_cards(self):
        with self.assertRaises(AssertionError):
            Hand("Ah Kh")
            
    def test_too_many_cards(self):
        with self.assertRaises(AssertionError):
            Hand("Ah Kh Qh Jh Th 9h 8h")
    
    def test_duplicate_cards(self):
        with self.assertRaises(AssertionError):
            Hand("Ah Ah Ah Ah Kh")

    def test_straight(self):
        self.assertTrue(Hand("6h 7s 8h 4h 5h").is_straight())
        self.assertFalse(Hand("2h 6h Qc Jh Th").is_straight())
        
    def test_wheel(self):
        self.assertTrue(Hand("Ah 2s 3c 4h 5h").is_straight())
        self.assertGreater(Hand("Jc Td 9h 8s 7c"), Hand("Ah 2s 3c 4h 5h"))
        
    def test_flush(self):
        self.assertTrue(Hand("Ah 2h 3h 4h 5h").is_flush())
        self.assertTrue(Hand("4h 5h 6h 7h 8h").is_flush())
        self.assertFalse(Hand("2h 6d Qc Js Th").is_flush())
        
    def test_score(self):
        h_list = [
            Hand("Jc Td 9h 8s 6c"), # High card
            Hand("Jc Td 9h 8s Js"), # Pair
            Hand("Jc Jd Th Ts 7c"), # Two pair
            Hand("Jc Jd Jh 8s 7c"), # Three of a kind
            Hand("Jc Td 9h 8s 7c"), # Straight
            Hand("Jh Th 9h 8h 2h"), # Flush
            Hand("Jc Jd Jh Ts Th"), # Full house
            Hand("Jc Jd Jh Js 7h"), # Four of a kind
            Hand("Jh Th 9h 8h 7h"), # Straight flush
            Hand("Ah Kh Qh Jh Th")  # Royal flush
        ]
        h_score_diff = [abs(hh.score - ii) for ii, hh in enumerate(h_list)]
        self.assertTrue(all(x > 0 for x in h_score_diff))
        
    def test_gtlt(self):
        self.assertGreater(Hand("Jc Jd Jh Ts Th"), Hand("Jc Td 9h 8s Js"))
        self.assertLess(Hand("Jc Td 9h 8s 6c"), Hand("Jc Jd Jh Js 7h"))

if __name__ == '__main__':
    unittest.main()