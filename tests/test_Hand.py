#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pokerequitycalc.config import CARDS
from pokerequitycalc.config import SUITS
from pokerequitycalc.classes import Card
from pokerequitycalc.classes import Hand

import unittest

class TestHandClass(unittest.TestCase):

    def test_input_str(self):
        h = Hand("Ah Kh Qh Jh Th")
        self.assertEqual(h.vals, [CARDS[x] for x in ["A","K","Q","J","T"]])
        self.assertEqual(h.suits, [SUITS[x] for x in ["h","h","h","h","h"]])
        
    def test_input_cards(self):
        h = Hand([Card("Ah"), Card("Kh"), Card("Qh"), Card("Jh"), Card("Th")])
        self.assertEqual(h.vals, [CARDS[x] for x in ["A","K","Q","J","T"]])
        self.assertEqual(h.suits, [SUITS[x] for x in ["h","h","h","h","h"]])
    
    def test_too_few_cards(self):
        with self.assertRaises(AssertionError):
            Hand("Ah Kh")
    
    def test_duplicate_cards(self):
        with self.assertRaises(AssertionError):
            Hand("Ah Ah Ah Ah Kh")

    def test_straight(self):
        self.assertTrue(Hand("Ah 2s 3c 4h 5h").is_straight())
        self.assertTrue(Hand("6h 7s 8h 4h 5h").is_straight())
        self.assertFalse(Hand("2h 6h Qc Jh Th").is_straight())  
        
    # def test_flush(self):

if __name__ == '__main__':
    unittest.main()