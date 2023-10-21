# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 22:32:58 2023

@author: Lim Jing
"""

import enum

class Position(enum.IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    
class Bid(enum.IntEnum):
    C1 = 0
    C2 = 1
    C3 = 2
    C4 = 3
    C5 = 4
    C6 = 5
    C7 = 6
    D1 = 7
    D2 = 8
    D3 = 9
    D4 = 10
    D5 = 11
    D6 = 12
    D7 = 13
    H1 = 14
    H2 = 15
    H3 = 16
    H4 = 17
    H5 = 18
    H6 = 19
    H7 = 20
    S1 = 21
    S2 = 22
    S3 = 23
    S4 = 24
    S5 = 25
    S6 = 26
    S7 = 27
    NT1 = 28
    NT2 = 29
    NT3 = 30
    NT4 = 31
    NT5 = 32
    NT6 = 33
    NT7 = 34
    P = 35
    X = 36
    XX = 37
    
class Vuln(enum.Enum):
    NONE = 0
    NS = 1
    EW = 2
    ALL = 3
    
