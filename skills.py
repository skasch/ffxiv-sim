# -*- coding: utf-8 -*-
"""
Created on Tue May 31 16:23:07 2016

@author: rmondoncancel
"""

def s():
    """Returns the list of skills
    name: name of the buff
    level: level necessary to unlock the skill
    tpCost: TP cost of the skill
    gcdType: global or instant, if the skill is on GCD or not
    cooldown: cooldown duration for the skill
    castTime: cast time of the skill; not implemented yet
    animationLock: animation lock of the skill, duration when using another 
        skill is impossible
    [range]: skill range of the skill; useless so far
    [radius]: radius of the skill; useless so far
    [potency]: base potency of the skill
    [type]: type of the attack [blunt/slashing/piercing]
    [gcdModifier]: ratio of next GCD duration; for example, Meditation halves
        the next GCD duration
    [requiedBuff]: array of buffs requied to use the skill; at least one should
        be present and at max stacks if the buff has stacks
    [removeBuff]: array of buffs removed when the skill is used
    [addBuff]: array of buffs added when the skill is used; when the buff has
        stacks, adds one stack
    [addDebuff]: array of debuffs added when the skill is used
    [special]: special action to be resolved when the skill is used
    [condition]: special condition to be added to the hidden conditions of the
        skill
    """
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