# -*- coding: utf-8 -*-
"""
Created on Tue May 31 16:47:37 2016

@author: rmondoncancel
"""

def d():
    """Returns the list of debuffs
    name: name of the debuff
    duration: duration of the debuff
    type: DoT or debuff, if it's a DoT or a stat debuff
    props: dict containing [key, buff] couples; possible keys:
        potency: potency of each tick if a DoT
        blunt, slashing, piercing: modifier for resistances
    """
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
    return d