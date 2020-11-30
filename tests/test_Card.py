#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from pokerequitycalc.config import CARDS
from pokerequitycalc.config import SUITS
from pokerequitycalc.classes import Card

class TestCardClass(unittest.TestCase):

    def test_nonesense(self):
        with self.assertRaises(AssertionError):
            Card("King of hearts")
    
    def test_bad_card(self):
        with self.assertRaises(AssertionError):
            Card("Wh")
    
    def test_bad_suit(self):
        with self.assertRaises(AssertionError):
            Card("Ae")
    
    def test_ace_hearts(self):
        c = Card("Ah")
        self.assertEqual(c.val, 14)
        self.assertEqual(c.suit, 2)
        
    def test_ace_gt_deuce(self):
        c_ace = Card("As")
        c_deuce = Card("2d")
        self.assertGreater(c_ace, c_deuce)
        
    def test_ace_equal(self):
        self.assertNotEqual(Card("Ah"), Card("As"))
        self.assertEqual(Card("Ah"), Card("Ah"))
        
    def test_hash_unique(self):
        all_cards = [Card(c+s) for c in CARDS.keys() for s in SUITS.keys()]
        all_hashes = set(c.__hash__() for c in all_cards)
        self.assertEqual(len(all_hashes), len(CARDS) * len(SUITS))

if __name__ == '__main__':
    unittest.main()