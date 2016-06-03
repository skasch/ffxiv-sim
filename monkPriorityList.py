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
            'comparison': 'is',
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
            'logic': 'and',
            'list': [
                {
                    'type': 'buffAtMaxStacks',
                    'name': 'greasedLightning',
                    'comparison': 'is',
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
            'comparison': 'is',
            'value': False,
        }
    },
    {
        'name': 'tornadoKick',
        'group': 'monk',
        'condition': {
            'logic': 'and',
            'list': [
                {
                    'type': 'buffTimeLeft',
                    'name': 'perfectBalance',
                    'comparison': '>=',
                    'value': 7,
                },
                {
                    'type': 'buffAtMaxStacks',
                    'name': 'greasedLightning',
                    'comparison': 'is',
                    'value': True,
                }
            ],
        }
    },
    {
        'name': 'internalRelease',
        'group': 'pugilist',
        'condition': {
            'logic': 'and',
            'list': [
                {
                    'type': 'buffAtMaxStacks',
                    'name': 'greasedLightning',
                    'comparison': 'is',
                    'value': True,
                },
                {
                    'type': 'cooldownTimeLeft',
                    'name': 'elixirField',
                    'comparison': '<=',
                    'value': 6,
                },
            ]
        }
    },
    {
        'name': 'potionOfStrengthHQ',
        'group': 'item',
        'condition': {
            'logic': 'and',
            'list': [
                {
                    'type': 'buffAtMaxStacks',
                    'name': 'greasedLightning',
                    'comparison': 'is',
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
            'comparison': 'is',
            'value': True,
        }
    },
    {
        'name': 'elixirField',
        'group': 'monk',
        'condition': {
            'logic': 'or',
            'list': [
                {
                    'type': 'buffPresent',
                    'name': 'internalRelease',
                    'comparison': 'is',
                    'value': True,
                },
                {
                    'type': 'cooldownTimeLeft',
                    'name': 'internalRelease',
                    'comparison': '>=',
                    'value': 20,
                },
            ],
        }
    },
    {
        'name': 'steelPeak',
        'group': 'pugilist',
        'condition': {
            'logic': 'and',
            'list': [
                {
                    'type': 'buffAtMaxStacks',
                    'name': 'greasedLightning',
                    'comparison': 'is',
                    'value': True,
                },
            ]
        }
    },
    {
        'name': 'touchOfDeath',
        'group': 'pugilist',
        'condition': {
            'logic': 'and',
            'list': [
                {
                    'type': 'debuffTimeLeft',
                    'name': 'touchOfDeath',
                    'comparison': '<=',
                    'value': 1.5,
                },
                {
                    'type': 'debuffPresent',
                    'name': 'dragonKick',
                    'comparison': 'is',
                    'value': True,
                },
                {
                    'type': 'buffPresent',
                    'name': 'twinSnakes',
                    'comparison': 'is',
                    'value': True,
                },
            ]
        }
    },
    {
        'name': 'fracture',
        'group': 'marauder',
        'condition': {
            'logic': 'and',
            'list': [
                {
                    'type': 'debuffTimeLeft',
                    'name': 'fracture',
                    'comparison': '<=',
                    'value': 1.5,
                },
                {
                    'type': 'debuffPresent',
                    'name': 'dragonKick',
                    'comparison': 'is',
                    'value': True,
                },
                {
                    'type': 'buffPresent',
                    'name': 'twinSnakes',
                    'comparison': 'is',
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
            'comparison': '<=',
            'value': 4,
        },
    },
    {
        'name': 'twinSnakes',
        'group': 'pugilist',
        'condition': {
            'type': 'buffTimeLeft',
            'name': 'twinSnakes',
            'comparison': '<=',
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
            'comparison': '<=',
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
