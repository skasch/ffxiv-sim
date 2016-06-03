# -*- coding: utf-8 -*-
"""
Created on Tue May 31 16:47:05 2016

@author: rmondoncancel
"""

def b():
    b = {}
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
        'maxStacks': 3,
        'buff': {
            'damage': 0.1,
            'speed': -0.05,
        },
    }
    b['internalRelease'] = {
        'name': 'internalRelease',
        'duration': 15,
        'buff': {
            'critChance': 0.3,    
        },
    }
    b['twinSnakes'] = {
        'name': 'twinSnakes',
        'duration': 15,
        'buff': {
            'damage': 0.1,
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
        'maxStack': 5,
        'buff': {},
    }
    b['bloodForBlood'] = {
        'name': 'bloodForBlood',
        'duration': 20,
        'buff': {
            'damage': 0.1,    
        },
    }
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
    return b