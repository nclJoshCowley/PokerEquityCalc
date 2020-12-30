#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
What does this script do?

@author:   Josh Cowley
@email:    j.cowley1@ncl.ac.uk
Created:   Tue Dec 22 19:12:16 2020
Modified:  Tue Dec 22 19:12:16 2020
"""

from pokerequitycalc.classes import Card
from pokerequitycalc.classes import Deck
from pokerequitycalc.config import CARDS
from pokerequitycalc.config import SUITS

d = Deck()
d # 52

d.remove_card(Card("Ac"))
d # 51

d.remove_card(Card("Ac")) # Err

deuce_to_five = [Card(str(c) + s) for c in range(2,6) for s in SUITS.keys()]
d.remove_card(*deuce_to_five)
d # 35


