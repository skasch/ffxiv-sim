# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 14:38:55 2016

@author: rmondoncancel
"""

import copy

def applyTrait(elem, pClass) :
    if 'traitBonus' in elem and elem['traitBonus']['class'] == pClass :
        for bonus in elem['traitBonus']['bonus'] :
            elem[bonus] = elem['traitBonus']['bonus'][bonus]
    return elem
    
def applyTraits(l, pClass, skill = False) :
    newL = {}
    if skill :
        for group in l :
            newL[group] = applyTraits(l[group], pClass)
        return newL
    for name in l :
        newL[name] = applyTrait(l[name], pClass)
    return newL

def removeLifeSurge(l, skill) :
    if not skill :
        return l
    newL = copy.deepcopy(l)
    for group in l :
        for name in l[group] :
            if 'potency' in newL[group][name] :
                newL[group][name]['removeBuff'] = (newL[group][name]['removeBuff'] if 'removeBuff' in newL[group][name] else []) + ['lifeSurge']
    return newL

def removeBloodOfTheDragonBuffs(l, skill) :
    if not skill :
        return l
    newL = copy.deepcopy(l)
    for group in l :
        for name in l[group] :
            if 'potency' in newL[group][name] and newL[group][name]['gcdType'] == 'global' and newL[group][name]['name'] not in ['sharperFangAndClaw', 'enhancedWheelingThrust'] :
                newL[group][name]['removeBuff'] = (newL[group][name]['removeBuff'] if 'removeBuff' in newL[group][name] else []) + ['sharperFangAndClaw', 'enhancedWheelingThrust']
    return newL

def prepareGroup(l, pClass, skill = False) :
    newL = applyTraits(l, pClass, skill)
    newL = removeLifeSurge(newL, skill)
    newL = removeBloodOfTheDragonBuffs(newL, skill)
    return newL