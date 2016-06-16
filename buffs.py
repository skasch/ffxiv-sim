# -*- coding: utf-8 -*-
"""
Created on Tue May 31 16:47:05 2016

@author: rmondoncancel
"""

from skillManagement import prepareGroup

def b(pClass):
    """Returns the list of buffs
    name: name of the buff
    buff: dict containing [key, buff] couples; possible keys:
        damage, critChance, speed: stat modifier (0.1 = +10%)
        strength: (ratio, max), the strength ratio and max bonus; will 
            calculate the lowest value for a given state.
    [duration]: duration of the buff
    [maxStacks]: max stacks of the buff
    """
    b = {}
    b['potionOfStrength'] = {
        'name': 'potionOfStrength',
        'duration': 15,
        'buff': {
            'strength': (0.16, 84),    
        },
    }
    b['potionOfStrengthHQ'] = {
        'name': 'potionOfStrengthHQ',
        'duration': 15,
        'buff': {
            'strength': (0.2, 105),    
        },
    }
    b['opoOpoForm'] = {
        'name': 'opoOpoForm',
        'duration': 10,
        'buff': {},
    }
    b['raptorForm'] = {
        'name': 'raptorForm',
        'duration': 10,
        'buff': {},
    }
    b['coerlForm'] = {
        'name': 'coerlForm',
        'duration': 10,
        'buff': {},
    }
    b['bootshineCrit'] = {
        'name': 'bootshineCrit',
        'duration': 0,
        'buff': {
            'critChance': 1,
        },
    }
    b['greasedLightning'] = {
        'name': 'greasedLightning',
        'duration': 14,
        'buff': {
            'damage': 0.1,
            'speed': -0.05,
        },
        'traitBonus': {
            'class': 'pugilist', 
            'level': 40, 
            'bonus': {
                'maxStacks': 3,
            }
        },
    }
    b['internalRelease'] = {
        'name': 'internalRelease',
        'duration': 15,
        'buff': {
            'critChance': 0.1,    
        },
        'traitBonus': {
            'class': 'pugilist', 
            'level': 36, 
            'bonus': {
                'buff': { 'critChance': 0.3 },
            }
        },
    }
    b['twinSnakes'] = {
        'name': 'twinSnakes',
        'duration': 15,
        'buff': {
            'damage': 0.05,
        },
        'traitBonus': {
            'class': 'pugilist', 
            'level': 28, 
            'bonus': {
                'buff': { 'damage': 0.1 },
            }
        },
    }
    b['perfectBalance'] = {
        'name': 'perfectBalance',
        'duration': 10,
        'buff': {},
    }
    b['fistOfFire'] = {
        'name': 'fistOfFire',
        'buff': {
            'damage': 0.05,
        },
    }
    b['chakra'] = {
        'name': 'chakra',
        'maxStacks': 5,
        'buff': {},
    }
    b['bloodForBlood'] = {
        'name': 'bloodForBlood',
        'duration': 20,
        'buff': {
            'damage': 0.1,    
        },
        'traitBonus': {
            'class': 'lancer', 
            'level': 44, 
            'bonus': {
                'buff': { 'damage': 0.3 },
            }
        },
    }
    b['heavyThrust'] = {
        'name': 'heavyThrust',
        'duration': 12,
        'buff': {
            'damage': 0.15,
        },
        'traitBonus': {
            'class': 'lancer', 
            'level': 40, 
            'bonus': {
                'duration': 24,
            }
        },
    }
    b['lifeSurge'] = {
        'name': 'lifeSurge',
        'duration': 10,
        'buff': {
            'critChance': 1,
        },
    }
    b['powerSurge'] = {
        'name': 'powerSurge',
        'duration': 10,
        'buff': {},
    }
    b['surgeBonus'] = {
        'name': 'surgeBonus',
        'duration': 0,
        'buff': {
            'potency': 0.5,        
        },
    }
    b['battleLitany'] = {
        'name': 'battleLitany',
        'duration': 20,
        'buff': {
            'critChance': 0.15,
        },
    }
    b['bloodOfTheDragon'] = {
        'name': 'bloodOfTheDragon',
        'duration': 15,
        'buff': {},
    }
    b['sharperFangAndClaw'] = {
        'name': 'sharperFangAndClaw',
        'duration': 10,
        'buff': {},
    }
    b['enhancedWheelingThrust'] = {
        'name': 'enhancedWheelingThrust',
        'duration': 10,
        'buff': {},
    }
    return prepareGroup(b, pClass)