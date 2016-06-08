# -*- coding: utf-8 -*-
"""
Created on Wed Jun 08 15:45:03 2016

@author: rmondoncancel
"""
import copy
import matplotlib.pyplot as pl
import numpy as np
from priorityParser import priorityParser
from priorityManagement import formatPriorityList
from timelineManagement import solveCurrentAction

def getInitializer(
    strength, 
    criticalHitRate, 
    determination, 
    skillSpeed, 
    weaponDamage, 
    weaponDelay, 
    weaponType,
) :
    return lambda autoAttack, dotTick : initializeState(
        strength,
        criticalHitRate,
        determination,
        skillSpeed,
        weaponDamage,
        weaponDelay,
        weaponType,
        autoAttack,
        dotTick,
    )

def initializeState(
    strength,
    criticalHitRate,
    determination,
    skillSpeed,
    weaponDamage,
    weaponDelay,
    weaponType,
    autoAttack,
    dotTick,
) :
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
        'nextActions': [ (autoAttack, { 'type': 'autoAttack' }), (dotTick, { 'type': 'dotTick' }) ],
    }
    
    # Player stats
    state['player']['baseStats'] = {
        'strength': strength,
        'criticalHitRate': criticalHitRate,
        'determination': determination,
        'skillSpeed': skillSpeed,
        'weaponDamage': weaponDamage,
        'weaponDelay': weaponDelay,
        'weaponType': weaponType,
    }
    return state

def getStatsWeights(initialState, priorityList, damageLimit, avgDPS) :
    stats = ['strength', 'criticalHitRate', 'determination', 'skillSpeed', 'weaponDamage'] 
    statWeights = {}
    for cStat in stats :
        mState = copy.deepcopy(initialState)
        mState['player']['baseStats'][cStat] = mState['player']['baseStats'][cStat] + 10
        (states, results) = runSim(mState, priorityList, damageLimit)
        (prepullEnd, simDuration) = getDuration(results)
        cDPS = sum( r['damage'] for r in results if 'damage' in r ) / simDuration
        statWeights[cStat] = cDPS - avgDPS
    strWeight = statWeights['strength']
    for cStat in stats :
        statWeights[cStat] = statWeights[cStat] / strWeight 
    return statWeights

def simContinue(state, totDamage, timeLimit, damageLimit, timeBased) :
    if timeBased :
        return state['timeline']['timestamp'] <= timeLimit
    else :
        return totDamage <= damageLimit
     
def runSim(initialState, priorityList, limit, timeBased = False) :
    states = [initialState]
    results = []
    nextState = copy.deepcopy(initialState)
    maxTime = limit * 60
    prepullEnd = 0
    totDamage = 0
    isPrepull = True
    while simContinue(nextState, totDamage, maxTime + prepullEnd, limit, timeBased) :
        (nextState, nextResult) = solveCurrentAction(nextState, priorityList)
        if 'damage' not in nextResult and isPrepull :
            prepullEnd = nextState['timeline']['timestamp']
        if 'damage' in nextResult:
            totDamage = totDamage + nextResult['damage']
            if isPrepull :
                isPrepull = False
        states = states + [nextState]
        results = results + [nextResult]
    return (states, results)

def getDuration(results) :
    return (
        min( r['timestamp'] for r in results  if 'damage' in r and 'timestamp' in r ),
        max( r['timestamp'] for r in results if 'damage' in r and 'timestamp' in r ) - \
            min( r['timestamp'] for r in results  if 'damage' in r and 'timestamp' in r )
    )

def simulate(
    model,
    strength,
    criticalHitRate,
    determination,
    skillSpeed,
    weaponDamage,
    weaponDelay,
    weaponType,
    duration,
    variation,
    nbSim,
    runStatWeights = False,
    random = True,
    autoAttack = 0.5,
    dotTick = 1,
    gDeltaT = 5,
) :
    # Priority list
    priorityList = priorityParser(model)
    plist = formatPriorityList(priorityList)
    initializer = getInitializer(strength,
                                 criticalHitRate,
                                 determination,
                                 skillSpeed,
                                 weaponDamage,
                                 weaponDelay,
                                 weaponType)
    
    # Get damage limit
    initialState = initializer(autoAttack, dotTick)
    (states, results) = runSim(initialState, plist, duration, True)
    damageLimit = sum( r['damage'] for r in results if 'damage' in r )
    
    # Initial state
    if random:
        pass
    else:
        initialState = initializer(autoAttack, dotTick)
        (states, results) = runSim(initialState, plist, damageLimit)
        (prepullEnd, simDuration) = getDuration(results)
        
        avgDPS = sum( r['damage'] for r in results if 'damage' in r ) / simDuration
        
        gTimeline = [ prepullEnd ]
        while gTimeline[-1] < simDuration + prepullEnd :
            gTimeline = gTimeline + [ gTimeline[-1] + 1 ]
        
        gDamage = [ sum( r['damage'] for r in results if 'damage' in r and r['timestamp'] >= t - gDeltaT and r['timestamp'] <= t + gDeltaT ) for t in gTimeline ]
        gDPS = [ d / (min(max(gTimeline), t + gDeltaT) - max(min(gTimeline), t - gDeltaT)) for (d, t) in zip(gDamage, gTimeline) ]
        
        pl.plot(gTimeline, gDPS)
        pl.show()
        
        gDmgSourcesTypes = np.unique([ (r['source'] if 'source' in r else '') + ' ' + (r['type'] if 'type' in r else '') for r in results if 'damage' in r ])
        gDmgSourceNames = np.array([ r.split(' ')[0] if r.split(' ')[1] == 'skill' else (r.split(' ')[0] + ' (DoT)' if r.split(' ')[1] == 'DoT' else 'autoAttack') for r in gDmgSourcesTypes ])
        gDmgSources = np.array([ r.split(' ')[0] for r in gDmgSourcesTypes ])
        gDmgTypes = np.array([ r.split(' ')[1] for r in gDmgSourcesTypes ])
        gCountAttacks = np.array([ len([ r for r in results if (('source' in r and r['source'] == s) or s == '') and ('type' in r and r['type'] == t) ]) for (s, t) in zip(gDmgSources, gDmgTypes) ])
        gDamageAttacks = np.array([ sum([ r['damage'] for r in results if (('source' in r and r['source'] == s) or s == '') and ('type' in r and r['type'] == t) ]) for (s, t) in zip(gDmgSources, gDmgTypes) ])
        gPotencyAttacks = np.array([ sum([ r['potency'] for r in results if (('source' in r and r['source'] == s) or s == '') and ('type' in r and r['type'] == t) ]) for (s, t) in zip(gDmgSources, gDmgTypes) ])
        gDamagePctAttacks = np.array([ d / sum(gDamageAttacks) * 100 for d in gDamageAttacks ])
        gDPSAttacks = np.array([ d / simDuration for d in gDamageAttacks ])
        gPPSAttacks = np.array([ d / simDuration for d in gPotencyAttacks ])
        gAvgDmgAttacks = np.array([ d / c for (c, d) in zip(gCountAttacks, gDamageAttacks) ])
        gAvgPotAttacks = np.array([ d / c for (c, d) in zip(gCountAttacks, gPotencyAttacks) ])
        
        gDmgOrder = [ i[0] for i in sorted(enumerate(gDamageAttacks), key = lambda x: x[1], reverse = True) ]
        
        tSkillCounts = np.array([ gDmgSourceNames[gDmgOrder], gCountAttacks[gDmgOrder], gDamageAttacks[gDmgOrder], gPotencyAttacks[gDmgOrder], gDamagePctAttacks[gDmgOrder], gDPSAttacks[gDmgOrder], gPPSAttacks[gDmgOrder], gAvgDmgAttacks[gDmgOrder], gAvgPotAttacks[gDmgOrder] ])
        
        pl.bar(range(len(gDmgSourceNames)), gDamageAttacks[gDmgOrder])
        pl.xticks([ i + 0.5 for i in range(len(gDmgSourceNames)) ], gDmgSourceNames[gDmgOrder], rotation=90)
        pl.show()
        
        print sum( r['damage'] for r in results if 'damage' in r ) / simDuration
        print sum( r['tpSpent'] for r in results if 'tpSpent' in r ) / simDuration
        
        gCycleSkills = np.array([ r['source'] for r in results if 'source' in r and r['type'] == 'skill' ])
        
        statWeights = {}
        if runStatWeights:
            statWeights = getStatsWeights(initialState, priorityList, damageLimit, avgDPS)
        
        return (states, results, avgDPS, tSkillCounts, gCycleSkills, statWeights)


  