# -*- coding: utf-8 -*-
"""
Created on Tue May 31 16:53:07 2016

@author: rmondoncancel
"""

def baseDamage(pot, wd, st, det, buf) :
    potW = 1./100.
    wdW = 0.0432544
    stW = 0.1027246
    detW = 1./7290.
    bufF = reduce(lambda x, y: x + y, buf, 1)
    return (pot * potW) * (st * stW) * (1. + wd * wdW) * (1. + det * detW) * bufF - 2.

def basePotency(pot, buf) :
    bufF = reduce(lambda x, y: x + y, buf, 1)
    return pot * bufF
    
def critChance(crt, buf) :
    bufF = reduce(lambda x, y: x + y, buf, 0)
    return min(1, ((crt - 354.) / (858. * 5.)) + 0.05 + bufF)

def critBonus(crt) :
    return ((crt - 354.) / (858. * 5.)) + 0.45

def gcdTick(ss, buf) :
    bufF = reduce(lambda x, y: x + y, buf, 1)
    return (2.50245 - ((ss - 354.) * 0.0003776)) * bufF

def dotTick(ss) :
    return ((ss - 354.) / 7722. + 1)