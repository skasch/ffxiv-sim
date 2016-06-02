# -*- coding: utf-8 -*-
"""
Created on Tue May 31 16:47:37 2016

@author: rmondoncancel
"""

def d():
    d = {}
    d['touchOfDeath'] = {
        'name': 'touchOfDeath',
        'duration': 30,
        'type': 'DoT',
        'props': {
            'potency': 25
        },
    }
    d['demolish'] = {
        'name': 'demolish',
        'duration': 21,
        'type': 'DoT',
        'props': {
            'potency': 50
        },
    }
    d['dragonKick'] = {
        'name': 'dragonKick',
        'duration': 15,
        'type': 'debuff',
        'props': {
            'blunt': 0.1,
        },
    }
    d['fracture'] = {
        'name': 'fracture',
        'duration': 18,
        'type': 'DoT',
        'props': {
            'potency': 20,
        },
    }
    d['lowLife'] = {
        'name': 'lowLife',
        'type': 'debuff',
    }
    return d