# -*- coding: utf-8 -*-
"""
Created on Tue May 31 16:53:07 2016

@author: rmondoncancel
"""

def strBonus(stBuff, st) :
    """Get the strength bonus
    Given a specific strength and a stBuff = (ratio, max) value, get the lowest
    bonus of both st * (1 + ratio) and st + max
    """
    return reduce(lambda x, y: min(x * (1 + y[0]), x + y[1]), stBuff, st)

def reduceBuffs(buf):
    return reduce(lambda x, y: x * (1 + y), buf, 1)

def buffedPotency(pot, buf) :
    """Get the base potency of the skill given specific buffs; applied BEFORE
    damage/potency calculation for damage buffs
    """
    bufF = reduceBuffs(buf)
    return pot * bufF

def baseDamage(pot, wd, st, det, buf) :
    """Get the damage output for given potency, stats, and buffs
    See Dervy's damage formula for source
    """
    potW = 1./100.
    wdW = 0.0432544
    stW = 0.1027246
    detW = 1./7290.
    bufF = reduceBuffs(buf)
    return (pot * potW) * (st * stW) * (1. + wd * wdW) * (1. + det * detW) * bufF - 2.

def basePotency(pot, buf) :
    """Get the modified potency for given potency and buffs
    """
    bufF = reduceBuffs(buf)
    return pot * bufF
    
def critChance(crt, buf) :
    """Get the critical hit chance for given stats and buffs
    See Dervy's damage formula for source
    """
    bufF = reduce(lambda x, y: x + y, buf, 0)
    return min(1, ((crt - 354.) / (858. * 5.)) + 0.05 + bufF)

def critBonus(crt) :
    """Get the critical hit damage bonus (as a ratio) for given stats and buffs
    See Dervy's damage formula for source
    """
    return ((crt - 354.) / (858. * 5.)) + 0.45

def gcdTick(ss, buf) :
    """Get the GCD tick duration for given stats and buffs
    See Dervy's damage formula for source
    """
    bufF = reduceBuffs(buf)
    return (2.50245 - ((ss - 354.) * 0.0003776)) * bufF

def getWeaponDelay(delay, buf) :
    """Get the GCD tick duration for given stats and buffs
    See Dervy's damage formula for source
    """
    bufF = reduceBuffs(buf)
    return delay * bufF

def dotTick(ss) :
    """Get the skill speed based damage bonus for DoTs
    See Dervy's damage formula for source
    """
    return (ss - 354.) / 7722.