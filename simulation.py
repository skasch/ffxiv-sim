# -*- coding: utf-8 -*-
"""
Created on Thu May 19 15:30:35 2016

@author: rmondoncancel
"""
# imports
import copy
import matplotlib.pyplot as pl
import numpy as np
from priorityParser import priorityParser
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
avgDPS = sum( r['damage'] for r in results if 'damage' in r ) / maxTime
print avgDPS

gTimeline = [ prepullEnd ]
while gTimeline[-1] < maxTime + prepullEnd :
    gTimeline = gTimeline + [ gTimeline[-1] + 1 ]

gDeltaT = 5

gDamage = [ sum( r['damage'] for r in results if 'damage' in r and r['timestamp'] >= t - gDeltaT and r['timestamp'] <= t + gDeltaT ) for t in gTimeline ]
gDPS = [ d / (min(max(gTimeline), t + gDeltaT) - max(min(gTimeline), t - gDeltaT)) for (d, t) in zip(gDamage, gTimeline) ]

pl.plot(gTimeline, gDPS)
pl.show()

tSkills = [ (r['source'], r['timestamp']) for r in results if 'type' in r and r['type'] == 'skill' ]

gDmgSourcesTypes = np.unique([ (r['source'] if 'source' in r else '') + ' ' + (r['type'] if 'type' in r else '') for r in results if 'damage' in r ])
gDmgSourceNames = np.array([ r.split(' ')[0] if r.split(' ')[1] == 'skill' else (r.split(' ')[0] + ' (DoT)' if r.split(' ')[1] == 'DoT' else 'autoAttack') for r in gDmgSourcesTypes ])
gDmgSources = np.array([ r.split(' ')[0] for r in gDmgSourcesTypes ])
gDmgTypes = np.array([ r.split(' ')[1] for r in gDmgSourcesTypes ])
gCountAttacks = np.array([ len([ r for r in results if (('source' in r and r['source'] == s) or s == '') and ('type' in r and r['type'] == t) ]) for (s, t) in zip(gDmgSources, gDmgTypes) ])
gDamageAttacks = np.array([ sum([ r['damage'] for r in results if (('source' in r and r['source'] == s) or s == '') and ('type' in r and r['type'] == t) ]) for (s, t) in zip(gDmgSources, gDmgTypes) ])
gDamagePctAttacks = np.array([ d / sum(gDamageAttacks) * 100 for d in gDamageAttacks ])
gDPSAttacks = np.array([ d / maxTime for d in gDamageAttacks ])
gAvgDmgAttacks = np.array([ d / c for (c, d) in zip(gCountAttacks, gDamageAttacks) ])

gDmgOrder = [ i[0] for i in sorted(enumerate(gDamageAttacks), key = lambda x: x[1], reverse = True) ]

tSkillCounts = np.array([ gDmgSourceNames[gDmgOrder], gCountAttacks[gDmgOrder], gDamageAttacks[gDmgOrder], gDamagePctAttacks[gDmgOrder], gDPSAttacks[gDmgOrder], gAvgDmgAttacks[gDmgOrder] ])

dmgBar = pl.bar(range(len(gDmgSourceNames)), gDamageAttacks[gDmgOrder])
pl.xticks([ i + 0.5 for i in range(len(gDmgSourceNames)) ], gDmgSourceNames[gDmgOrder], rotation=90)
pl.show()

print sum( r['damage'] for r in results if 'damage' in r ) / maxTime
print sum( r['tpSpent'] for r in results if 'tpSpent' in r ) / maxTime

gCycleSkills = np.array([ r['source'] for r in results if 'source' in r and r['type'] == 'skill' ])

stats = ['strength', 'criticalHitRate', 'determination', 'skillSpeed', 'weaponDamage']

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


statWeights = {}

for cStat in stats :
    mState = copy.deepcopy(state)
    mState['player']['baseStats'][cStat] = mState['player']['baseStats'][cStat] + 1
    states = [mState]
    results = []
    nextState = copy.deepcopy(mState)
    prepullEnd = 0
    while nextState['timeline']['timestamp'] <= maxTime + prepullEnd:
        (nextState, nextResult) = solveCurrentAction(nextState, plist)
        prepullEnd = max(nextState['timeline']['prepullTimestamp'].values())
        states = states + [nextState]
        results = results + [nextResult]
    # [ r['source'] for r in results if 'source' in r and r['type'] == 'skill' ]
    # sum( r['potency'] for r in results if 'potency' in r ) / maxTime
    cDPS = sum( r['damage'] for r in results if 'damage' in r ) / maxTime
    statWeights[cStat] = cDPS - avgDPS

for cStat in stats :
    statWeights[cStat] = statWeights[cStat] / statWeights['strength']

print statWeights
