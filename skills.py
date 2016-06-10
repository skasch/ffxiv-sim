# -*- coding: utf-8 -*-
"""
Created on Tue May 31 16:23:07 2016

@author: rmondoncancel
"""

def s():
    s = {}
    # Pugilist
    s['pugilist'] = {}
    s['pugilist']['bootshine'] = {
        'name': 'bootshine',
        'level': 1,
        'tpCost': 60,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 150,
        'animationLock': 0.75,
        'type': 'blunt',
        'removeBuff': ['opoOpoForm'],
        'addBuff': ['raptorForm'],
        'special': 'bootshineCrit',
    }
    s['pugilist']['trueStrike'] = {
        'name': 'trueStrike',
        'level': 2,
        'tpCost': 50,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 190,
        'animationLock': 0.75,
        'type': 'blunt',
        'requiredBuff': ['raptorForm', 'perfectBalance'],
        'removeBuff': ['raptorForm'],
        'addBuff': ['coerlForm'],
    }
    s['pugilist']['snapPunch'] = {
        'name': 'snapPunch',
        'level': 6,
        'tpCost': 50,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 180,
        'animationLock': 0.75,
        'type': 'blunt',
        'requiredBuff': ['coerlForm', 'perfectBalance'],
        'removeBuff': ['coerlForm'],
        'addBuff': ['opoOpoForm', 'greasedLightning'],
    }
    s['pugilist']['internalRelease'] = {
        'name': 'internalRelease',
        'level': 12,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 60,
        'castTime': 0,
        'animationLock': 0.75,
        'addBuff': ['internalRelease'],
    }
    s['pugilist']['touchOfDeath'] = {
        'name': 'touchOfDeath',
        'level': 15,
        'tpCost': 80,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 20,
        'animationLock': 0.75,
        'type': 'blunt',
        'addDebuff': ['touchOfDeath'],
    }
    s['pugilist']['twinSnakes'] = {
        'name': 'twinSnakes',
        'level': 18,
        'tpCost': 60,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 140,
        'animationLock': 0.75,
        'type': 'blunt',
        'requiredBuff': ['raptorForm', 'perfectBalance'],
        'removeBuff': ['raptorForm'],
        'addBuff': ['coerlForm', 'twinSnakes'],
    }
    s['pugilist']['demolish'] = {
        'name': 'demolish',
        'level': 30,
        'tpCost': 130,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 70,
        'animationLock': 0.75,
        'type': 'blunt',
        'requiredBuff': ['coerlForm', 'perfectBalance'],
        'removeBuff': ['coerlForm'],
        'addBuff': ['opoOpoForm', 'greasedLightning'],
        'addDebuff': ['demolish'],
    }
    s['pugilist']['steelPeak'] = {
        'name': 'steelPeak',
        'level': 38,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 40,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 150,
        'animationLock': 0.75,
        'type': 'blunt',
    }
    s['pugilist']['howlingFist'] = {
        'name': 'howlingFist',
        'level': 46,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 60,
        'castTime': 0,
        'range': 10,
        'radius': 10,
        'potency': 210,
        'animationLock': 0.75,
        'type': 'blunt',
    }
    s['pugilist']['perfectBalance'] = {
        'name': 'perfectBalance',
        'level': 46,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 240,
        'castTime': 0,
        'animationLock': 0.75,
        'addBuff': ['perfectBalance'],
        'special': 'removeForms',
    }
    
    # Monk
    s['monk'] = {}
    s['monk']['shoulderTackle'] = {
        'name': 'shoulderTackle',
        'level': 35,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 30,
        'castTime': 0,
        'range': 20,
        'radius': 0,
        'potency': 100,
        'animationLock': 0.75,
        'type': 'blunt',
    }
    s['monk']['fistOfFire'] = {
        'name': 'fistOfFire',
        'level': 40,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 3,
        'castTime': 0,
        'animationLock': 0.75,
        'addBuff': ['fistOfFire'],
    }
    s['monk']['dragonKick'] = {
        'name': 'dragonKick',
        'level': 50,
        'tpCost': 60,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 150,
        'animationLock': 0.75,
        'type': 'blunt',
        'removeBuff': ['opoOpoForm'],
        'addBuff': ['raptorForm'],
        'special': 'dragonKick',
    }
    s['monk']['formShift'] = {
        'name': 'formShift',
        'level': 52,
        'tpCost': 0,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'animationLock': 0.75,
        'special': 'nextForm'
    }
    s['monk']['meditation'] = {
        'name': 'meditation',
        'level': 54,
        'tpCost': 0,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'animationLock': 0.75,
        'gcdModifier': 0.5,
        'addBuff': ['chakra'],
    }
    s['monk']['forbiddenChakra'] = {
        'name': 'forbiddenChakra',
        'level': 54,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 5,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 320,
        'animationLock': 0.75,
        'type': 'blunt',
        'requiredBuff': ['chakra'],
        'removeBuff': ['chakra'],
    }
    s['monk']['elixirField'] = {
        'name': 'elixirField',
        'level': 56,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 30,
        'castTime': 0,
        'range': 0,
        'radius': 5,
        'potency': 220,
        'animationLock': 0.75,
        'type': 'blunt',
    }
    s['monk']['tornadoKick'] = {
        'name': 'tornadoKick',
        'level': 60,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 40,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 330,
        'animationLock': 0.75,
        'type': 'blunt',
        'requiredBuff': ['greasedLightning'],
        'removeBuff': ['greasedLightning'],
    }
    
    # Lancer
    s['lancer'] = {}
    s['lancer']['bloodForBlood'] = {
        'name': 'bloodForBlood',
        'level': 34,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 80,
        'castTime': 0,
        'animationLock': 0.75,
        'addBuff': ['bloodForBlood'],
    }
    
    # Marauder
    s['marauder'] = {}
    s['marauder']['fracture'] = {
        'name': 'fracture',
        'level': 6,
        'tpCost': 80,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 100,
        'animationLock': 0.75,
        'type': 'slashing',
        'addDebuff': ['fracture'],
    }
    s['marauder']['mercyStroke'] = {
        'name': 'mercyStroke',
        'level': 26,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 90,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 200,
        'animationLock': 0.75,
        'type': 'slashing',
        'condition': {
            'comparison': '<=',
            'type': 'enemy',
            'name': 'lifePercent',
            'value': 20,
        }
    }
    
    # Items
    s['item'] = {}
    s['item']['potionOfStrength'] = {
        'name': 'potionOfStrength',
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 300,
        'castTime': 0,
        'animationLock': 0.75,
        'addBuff': ['potionOfStrength'],
    }
    s['item']['potionOfStrengthHQ'] = {
        'name': 'potionOfStrengthHQ',
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 300,
        'castTime': 0,
        'animationLock': 0.75,
        'addBuff': ['potionOfStrengthHQ'],
    }
    return s