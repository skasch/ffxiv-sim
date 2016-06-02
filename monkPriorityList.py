# -*- coding: utf-8 -*-
"""
Created on Tue May 31 17:02:24 2016

@author: rmondoncancel
"""

priorityList = [
    {
        'name': 'fistOfFire',
        'group': 'monk',
        'prepull': True,
        'condition': {
            'type': 'buffPresent',
            'name': 'fistOfFire',
            'comparison': lambda x, y: x == y,
            'value': False,
        }
    },
    {
        'name': 'perfectBalance',
        'group': 'pugilist',
        'prepull': True,
    },
    {
        'name': 'bloodForBlood',
        'group': 'lancer',
        'condition': {
            'logic': lambda x, y: x and y,
            'list': [
                {
                    'type': 'buffAtMaxStacks',
                    'name': 'greasedLightning',
                    'comparison': lambda x, y: x == y,
                    'value': True,
                },
            ]
        }
    },
    {
        'name': 'perfectBalance',
        'group': 'pugilist',
        'condition': {
            'type': 'cooldownPresent',
            'name': 'tornadoKick',
            'comparison': lambda x, y: x == y,
            'value': False,
        }
    },
    {
        'name': 'tornadoKick',
        'group': 'monk',
        'condition': {
            'logic': lambda x, y: x and y,
            'list': [
                {
                    'type': 'buffTimeLeft',
                    'name': 'perfectBalance',
                    'comparison': lambda x, y: x >= y,
                    'value': 7,
                },
                {
                    'type': 'buffAtMaxStacks',
                    'name': 'greasedLightning',
                    'comparison': lambda x, y: x == y,
                    'value': True,
                }
            ],
        }
    },
    {
        'name': 'internalRelease',
        'group': 'pugilist',
        'condition': {
            'logic': lambda x, y: x and y,
            'list': [
                {
                    'type': 'buffAtMaxStacks',
                    'name': 'greasedLightning',
                    'comparison': lambda x, y: x == y,
                    'value': True,
                },
                {
                    'type': 'cooldownTimeLeft',
                    'name': 'elixirField',
                    'comparison': lambda x, y: x <= y,
                    'value': 6,
                },
            ]
        }
    },
    {
        'name': 'potionOfStrengthHQ',
        'group': 'item',
        'condition': {
            'logic': lambda x, y: x and y,
            'list': [
                {
                    'type': 'buffAtMaxStacks',
                    'name': 'greasedLightning',
                    'comparison': lambda x, y: x == y,
                    'value': True,
                },
            ]
        }
    },
    {
        'name': 'howlingFist',
        'group': 'pugilist',
        'condition': {
            'type': 'buffPresent',
            'name': 'internalRelease',
            'comparison': lambda x, y: x == y,
            'value': True,
        }
    },
    {
        'name': 'elixirField',
        'group': 'monk',
        'condition': {
            'logic': lambda x, y: x or y,
            'list': [
                {
                    'type': 'buffPresent',
                    'name': 'internalRelease',
                    'comparison': lambda x, y: x == y,
                    'value': True,
                },
                {
                    'type': 'cooldownTimeLeft',
                    'name': 'internalRelease',
                    'comparison': lambda x, y: x >= y,
                    'value': 20,
                },
            ],
        }
    },
    {
        'name': 'steelPeak',
        'group': 'pugilist',
        'condition': {
            'logic': lambda x, y: x and y,
            'list': [
                {
                    'type': 'buffAtMaxStacks',
                    'name': 'greasedLightning',
                    'comparison': lambda x, y: x == y,
                    'value': True,
                },
            ]
        }
    },
    {
        'name': 'touchOfDeath',
        'group': 'pugilist',
        'condition': {
            'logic': lambda x, y: x and y,
            'list': [
                {
                    'type': 'debuffTimeLeft',
                    'name': 'touchOfDeath',
                    'comparison': lambda x, y: x <= y,
                    'value': 1.5,
                },
                {
                    'type': 'debuffPresent',
                    'name': 'dragonKick',
                    'comparison': lambda x, y: x == y,
                    'value': True,
                },
                {
                    'type': 'buffPresent',
                    'name': 'twinSnakes',
                    'comparison': lambda x, y: x == y,
                    'value': True,
                },
            ]
        }
    },
    {
        'name': 'fracture',
        'group': 'marauder',
        'condition': {
            'logic': lambda x, y: x and y,
            'list': [
                {
                    'type': 'debuffTimeLeft',
                    'name': 'fracture',
                    'comparison': lambda x, y: x <= y,
                    'value': 1.5,
                },
                {
                    'type': 'debuffPresent',
                    'name': 'dragonKick',
                    'comparison': lambda x, y: x == y,
                    'value': True,
                },
                {
                    'type': 'buffPresent',
                    'name': 'twinSnakes',
                    'comparison': lambda x, y: x == y,
                    'value': True,
                },
            ]
        }
    },
    {
        'name': 'demolish',
        'group': 'pugilist',
        'condition': {
            'type': 'debuffTimeLeft',
            'name': 'demolish',
            'comparison': lambda x, y: x <= y,
            'value': 4,
        },
    },
    {
        'name': 'twinSnakes',
        'group': 'pugilist',
        'condition': {
            'type': 'buffTimeLeft',
            'name': 'twinSnakes',
            'comparison': lambda x, y: x <= y,
            'value': 5,
        },
    },
    {
        'name': 'snapPunch',
        'group': 'pugilist',
    },
    {
        'name': 'dragonKick',
        'group': 'monk',
        'condition': {
            'type': 'debuffTimeLeft',
            'name': 'dragonKick',
            'comparison': lambda x, y: x <= y,
            'value': 5,
        },
    },
    {
        'name': 'trueStrike',
        'group': 'pugilist',
    },
    {
        'name': 'bootshine',
        'group': 'pugilist',
    },
]
