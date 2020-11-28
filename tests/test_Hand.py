#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import

class TestCardClass(unittest.TestCase):

    def test_input_str(self):
        h = Hand("Ah Kh Qh Jh Th")
        self.assertEqual(h.card_values, [12, 11, 10, 9, 8])
        self.assertEqual(h.card_suits, [2, 2, 2, 2, 2])
        
    def test_straight(self):
        self.assertTrue(Hand("Ah 2s 3c 4h 5h").is_straight())
        self.assertTrue(Hand("6h 7s 8h 4h 5h").is_straight())
        self.assertFalse(Hand("2h 6h Qc Jh Th").is_straight())  
        
    # def test_flush(self):

if __name__ == '__main__':
    unittest.main()