# -*- coding: utf-8 -*-
"""
Created on Fri Jun 03 10:03:13 2016

@author: rmondoncancel
"""

import copy
import matplotlib.pyplot as pl
import numpy as np
from priorityParser import priorityParser, priorityDeparser
from priorityManagement import formatPriorityList
from timelineManagement import solveCurrentAction

model = 'monk'
priorityList = priorityParser(model)

# Initialize State
state = {}
state['player'] = {
    'buff': [],
    'baseStats': {},
    'cooldown': [],
}
state['enemy'] = {
    'debuff': [],
    'resistance': {
        'slashing': 1,
        'piercing': 1,
        'blunt': 1,
    }
}
state['timeline'] = {
    'timestamp': 0,
    'currentAction': { 'type': 'gcdSkill' },
    'prepull': { 'global': True, 'instant': True },
    'prepullTimestamp': { 'global': 0, 'instant': 0 },
    'nextActions': [ (0.5, { 'type': 'autoAttack' }), (1, { 'type': 'dotTick' }) ],
}

# Player stats
state['player']['baseStats'] = {
    'strength': 1306,
    'criticalHitRate': 814,
    'determination': 523,
    'attackPower': 484,
    'skillSpeed': 741,
    'weaponDamage': 81,
    'weaponDelay': 2.56,
    'weaponType': 'blunt',
}

plist = formatPriorityList(priorityList)

states = [state]
results = []
nextState = copy.deepcopy(state)
maxTime = 8 * 60
prepullEnd = 0
while nextState['timeline']['timestamp'] <= maxTime + prepullEnd:
    (nextState, nextResult) = solveCurrentAction(nextState, plist)
    prepullEnd = max(nextState['timeline']['prepullTimestamp'].values())
    states = states + [nextState]
    results = results + [nextResult]
# [ r['source'] for r in results if 'source' in r and r['type'] == 'skill' ]
# sum( r['potency'] for r in results if 'potency' in r ) / maxTime
refDPS = sum( r['damage'] for r in results if 'damage' in r ) / maxTime
print refDPS

unoptimized = True
while unoptimized :
    unoptimized = False
    for i in range(len(priorityList) - 1):
        # for j in range(i + 1, len(priorityList)):
        j = i+1
        newPriorityList = copy.deepcopy(priorityList)
        newPriorityList[i], newPriorityList[j] = newPriorityList[j], newPriorityList[i]
        plist = formatPriorityList(newPriorityList)
        
        states = [state]
        results = []
        nextState = copy.deepcopy(state)
        prepullEnd = 0
        while nextState['timeline']['timestamp'] <= maxTime + prepullEnd:
            (nextState, nextResult) = solveCurrentAction(nextState, plist)
            prepullEnd = max(nextState['timeline']['prepullTimestamp'].values())
            states = states + [nextState]
            results = results + [nextResult]
        # [ r['source'] for r in results if 'source' in r and r['type'] == 'skill' ]
        # sum( r['potency'] for r in results if 'potency' in r ) / maxTime
        newDPS = sum( r['damage'] for r in results if 'damage' in r ) / maxTime
        print newDPS
        if newDPS > refDPS * 1.0001:
            unoptimized = True
            bestPerm = (i, j)
            refDPS = newDPS
    if unoptimized :
        priorityList[bestPerm[0]], priorityList[bestPerm[1]] = priorityList[bestPerm[1]], priorityList[bestPerm[0]]

print priorityDeparser(priorityList)
        