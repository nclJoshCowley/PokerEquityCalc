#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from class_card import Card

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
        self.assertEqual(c.card, 12)
        self.assertEqual(c.suit, 2)
        
    def test_ace_gt_deuce(self):
        c_ace = Card("As")
        c_deuce = Card("2d")
        self.assertGreater(c_ace, c_deuce)
        
    def test_ace_equal(self):
        self.assertEqual(Card("Ah"), Card("As"))

if __name__ == '__main__':
    unittest.main()