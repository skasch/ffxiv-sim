# -*- coding: utf-8 -*-
"""
Created on Wed Jun 08 15:45:03 2016

@author: rmondoncancel
"""
import random
import copy
import math
import matplotlib.pyplot as pl
import numpy as np
from stateManagement import addAction
from priorityParser import priorityParser
from priorityManagement import formatPriorityList
from timelineManagement import solveCurrentAction
from priorityParser import isFloat

def getInitializer(
    strength, 
    criticalHitRate, 
    determination, 
    skillSpeed, 
    weaponDamage, 
    weaponDelay, 
    weaponType,
) :
    """Returns a function to create the initial state with parameters constant
    across the simulations taking the variable ones as input
    autoAttack, dotTick and hp are the variable elements that can change from
    one simulation to another
    """
    return lambda autoAttack, dotTick, hp = None : initializeState(
        strength,
        criticalHitRate,
        determination,
        skillSpeed,
        weaponDamage,
        weaponDelay,
        weaponType,
        autoAttack,
        dotTick,
        hp,
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
    hp = None,
) :
    """Initialize the state of the simulation
    strength: Strength of the character
    criticalHitRate: Critical Hit Rate of the character
    determination: Determination of the character
    skillSpeed: Skill Speed of the character
    weaponDamage: Weapon Damage of the weapon of the character
    weaponDelay: Weapon Delay of the weapon of the character
    weaponType: Weapon damage type of the weapon of the character 
        (blunt/slashing/piercing)
    autoAttack: Timestamp of the first auto-attack, in [0, weaponDelay)
    dotTick: Timestamp of the first DoT tick, in [0, 3)
    hp: The number of HP of the enemy if HP based simulation
    """
    state = {}
    # PLayer state
    # buff: list of active buffs
    # baseStats: baseStats of the character
    # cooldown: list of skills on cooldown
    state['player'] = {
        'buff': [],
        'baseStats': {},
        'cooldown': [],
    }
    # Enemy state
    # debuff: list of debuffs
    # resistance: base resistances of the enemy
    state['enemy'] = {
        'debuff': [],
        'resistance': {
            'slashing': 1,
            'piercing': 1,
            'blunt': 1,
        }
    }
    # Simulation timeline state
    # timestamp: timestamp of the state
    # currentAction: action to be resolved in the current state
    # prepull: if global or instant skill is to be tried on prepull
    # prepullTimestamp: timestamps of the last global and instant skills used 
    #   in prepull
    # nextActions: next Actions to be resolved in the timeline
    state['timeline'] = {
        'timestamp': 0,
        'currentAction': { 'type': 'gcdSkill' },
        'prepull': { 'global': True, 'instant': True },
        'prepullTimestamp': { 'global': 0, 'instant': 0 },
        'nextActions': [],
    }
    state = addAction(state, autoAttack, { 'type': 'autoAttack' })
    state = addAction(state, dotTick, { 'type': 'dotTick' })
    
    # Add hp and maxHp parameters to the enemy if HP based simulation
    if hp is not None:
        state['enemy']['hp'] = hp
        state['enemy']['maxHp'] = hp
    
    # Set character base stats
    state['player']['baseStats'] = {
        'strength': applyPartyBuff(strength),
        'criticalHitRate': criticalHitRate,
        'determination': determination,
        'skillSpeed': skillSpeed,
        'weaponDamage': weaponDamage,
        'weaponDelay': weaponDelay,
        'weaponType': weaponType,
    }
    return state

def applyPartyBuff(stat):
    """Apply party buff of 3% to the given stat
    """
    return math.floor(stat * 1.03)

def getStatsWeights(initialState, priorityList, damageLimit, avgDPS) :
    """Computes the stats weights for a given context, with avgDPS being the
    reference DPS
    """
    stats = ['strength', 'criticalHitRate', 'determination', 'skillSpeed', 'weaponDamage'] 
    statWeights = {}
    for cStat in stats :
        # Create a new state with a modified base stat (+10 to base stat)
        mState = copy.deepcopy(initialState)
        mState['player']['baseStats'][cStat] = mState['player']['baseStats'][cStat] + 10
        (states, results) = runSim(mState, priorityList, damageLimit)
        (prepullEnd, simDuration) = getDuration(results)
        # Get the DPS of the new simulation
        cDPS = sum( r['damage'] for r in results if 'damage' in r ) / simDuration
        statWeights[cStat] = cDPS - avgDPS
    # Normalize weights: main stat weight = 1
    strWeight = statWeights['strength']
    for cStat in stats :
        statWeights[cStat] = statWeights[cStat] / strWeight 
    return statWeights

def simContinue(state, timeLimit = None) :
    """Test if simulation should continue to next state:
    If time based: if simulation is after time limit
    If HP based: if enemy has HP left
    """
    if timeLimit is not None :
        return state['timeline']['timestamp'] <= timeLimit
    else :
        return state['enemy']['hp'] > 0
     
def runSim(initialState, priorityList, duration = None) :
    """Run a single simulation from initialState with priorityList
    duration is specific to time based simulations
    """
    states = [initialState]
    results = []
    nextState = copy.deepcopy(initialState)
    prepullEnd = 0
    isPrepull = True
    # Runs the simulation while it must continue
    while simContinue(nextState, duration * 60 + prepullEnd if duration is not None else None) :
        (nextState, nextResult) = solveCurrentAction(nextState, priorityList)
        # If the skill deals damage and the simulation is on prepull, then it's
        # the first non-prepull skill and it should be the beginning of the
        # simulation, so the timestamp is saved into prepullEnd
        if 'damage' in nextResult and isPrepull :
            prepullEnd = nextState['timeline']['timestamp']
            isPrepull = False
        states = states + [nextState]
        results = results + [nextResult]
    # Returns the list of states and results through the simulation
    return (states, results)

def getDuration(results) :
    """Returns the first timestamp of the simulation after the prepull and the
    duration of the simulation after the prepull
    """
    timestamps = [ r['timestamp'] for r in results  if 'damage' in r and 'timestamp' in r ]
    return (min(timestamps), max(timestamps) - min(timestamps))
    
def simulationAnalysis(states, results, gDeltaT) :
    """Returns a list of interesting metrics to analyze the results of a 
    simulation
    avgDPS: average DPS of the simulation
    avgTPSPS: average TP spent per second
    tSkill: table containing various metrics about the different skill
    gTimeline: list of skills cast by the player
    gDPS: averaged DPS over a window of [ts +/- gDeltaT] for each second of the
        simulation
    """
    # Get duration of the simulation and first timestamp
    (prepullEnd, simDuration) = getDuration(results)
    # Average DPS and TPSPS of the simulation
    avgDPS = sum( r['damage'] for r in results if 'damage' in r ) / simDuration
    avgTPSPS = sum( r['tpSpent'] for r in results if 'tpSpent' in r ) / simDuration
    
    # Timeline of the simulation with 1s step
    gTimeline = [ prepullEnd ]
    while gTimeline[-1] < simDuration + prepullEnd :
        gTimeline = gTimeline + [ gTimeline[-1] + 1 ]
    
    # Calculates the average DPS through the timeline on a [ts +/- gDeltaT]
    # window
    gDamage = [ sum( r['damage'] for r in results if 'damage' in r and r['timestamp'] >= t - gDeltaT and r['timestamp'] <= t + gDeltaT ) for t in gTimeline ]
    gDPS = [ d / (min(max(gTimeline), t + gDeltaT) - max(min(gTimeline), t - gDeltaT)) for (d, t) in zip(gDamage, gTimeline) ]
    
    # Sources and types of the skills
    gDmgSourcesTypes = np.unique([ (r['source'] if 'source' in r else '') + ' ' + (r['type'] if 'type' in r else '') for r in results if 'damage' in r ])
    gDmgSources = np.array([ r.split(' ')[0] for r in gDmgSourcesTypes ])
    gDmgTypes = np.array([ r.split(' ')[1] for r in gDmgSourcesTypes ])
    # Names of the skills
    gDmgSourceNames = np.array([ r.split(' ')[0] if r.split(' ')[1] == 'skill' else (r.split(' ')[0] + ' (DoT)' if r.split(' ')[1] == 'DoT' else 'autoAttack') for r in gDmgSourcesTypes ])
    # Number of each casts for each skills
    gCountAttacks = np.array([ len([ r for r in results if (('source' in r and r['source'] == s) or s == '') and ('type' in r and r['type'] == t) ]) for (s, t) in zip(gDmgSources, gDmgTypes) ])
    # Total damage for each skill
    gDamageAttacks = np.array([ sum([ r['damage'] for r in results if (('source' in r and r['source'] == s) or s == '') and ('type' in r and r['type'] == t) ]) for (s, t) in zip(gDmgSources, gDmgTypes) ])
    # Total potency for each skill    
    gPotencyAttacks = np.array([ sum([ r['potency'] for r in results if (('source' in r and r['source'] == s) or s == '') and ('type' in r and r['type'] == t) ]) for (s, t) in zip(gDmgSources, gDmgTypes) ])
    # Total damage if all normal hits
    gHitDamageAttacks = np.array([ sum([ r['hitDamage'] for r in results if (('source' in r and r['source'] == s) or s == '') and ('type' in r and r['type'] == t) ]) for (s, t) in zip(gDmgSources, gDmgTypes) ])
    # Total potency if all normal hits  
    gHitPotencyAttacks = np.array([ sum([ r['hitPotency'] for r in results if (('source' in r and r['source'] == s) or s == '') and ('type' in r and r['type'] == t) ]) for (s, t) in zip(gDmgSources, gDmgTypes) ])
    # Total damage if all crits
    gCritDamageAttacks = np.array([ sum([ r['critDamage'] for r in results if (('source' in r and r['source'] == s) or s == '') and ('type' in r and r['type'] == t) ]) for (s, t) in zip(gDmgSources, gDmgTypes) ])
    # Total potency if all crits
    gCritPotencyAttacks = np.array([ sum([ r['critPotency'] for r in results if (('source' in r and r['source'] == s) or s == '') and ('type' in r and r['type'] == t) ]) for (s, t) in zip(gDmgSources, gDmgTypes) ])
    # Sum of crit rates
    gCritChanceAttacks = np.array([ sum([ r['critChance'] for r in results if (('source' in r and r['source'] == s) or s == '') and ('type' in r and r['type'] == t) ]) for (s, t) in zip(gDmgSources, gDmgTypes) ])
    # Sum of crit bonuses
    gCritBonusAttacks = np.array([ sum([ r['critBonus'] for r in results if (('source' in r and r['source'] == s) or s == '') and ('type' in r and r['type'] == t) ]) for (s, t) in zip(gDmgSources, gDmgTypes) ])
    # Percentage of total damage of each skill
    gDamagePctAttacks = np.array([ d / sum(gDamageAttacks) * 100 for d in gDamageAttacks ])
    # Partial DPS for each skill
    gDPSAttacks = np.array([ d / simDuration for d in gDamageAttacks ])
    # Partial potency for each skill
    gPPSAttacks = np.array([ d / simDuration for d in gPotencyAttacks ])
    # Average damage per cast for each skill
    gAvgDmgAttacks = np.array([ d / c for (c, d) in zip(gCountAttacks, gDamageAttacks) ])
    # Average potency per cast for each skill
    gAvgPotAttacks = np.array([ d / c for (c, d) in zip(gCountAttacks, gPotencyAttacks) ])
    # Average normal hit damage per cast for each skill
    gAvgHitDmgAttacks = np.array([ d / c for (c, d) in zip(gCountAttacks, gHitDamageAttacks) ])
    # Average normal hit potency per cast for each skill
    gAvgHitPotAttacks = np.array([ d / c for (c, d) in zip(gCountAttacks, gHitPotencyAttacks) ])
    # Average normal hit damage per cast for each skill
    gAvgCritDmgAttacks = np.array([ d / c for (c, d) in zip(gCountAttacks, gCritDamageAttacks) ])
    # Average normal hit potency per cast for each skill
    gAvgCritPotAttacks = np.array([ d / c for (c, d) in zip(gCountAttacks, gCritPotencyAttacks) ])
    # Average normal hit damage per cast for each skill
    gAvgCritChcAttacks = np.array([ d / c * 100 for (c, d) in zip(gCountAttacks, gCritChanceAttacks) ])
    # Average normal hit potency per cast for each skill
    gAvgCritBonusAttacks = np.array([ d / c for (c, d) in zip(gCountAttacks, gCritBonusAttacks) ])
    # Order skills by name
    gNameOrder = [ i[0] for i in sorted(enumerate(gDmgSourceNames), key = lambda x: x[1]) ]
    # Table gathering the previous skill metrics
    tSkill = np.array([ gDmgSourceNames[gNameOrder], gCountAttacks[gNameOrder], gDamageAttacks[gNameOrder], gPotencyAttacks[gNameOrder], gDamagePctAttacks[gNameOrder], gDPSAttacks[gNameOrder], gPPSAttacks[gNameOrder], gAvgDmgAttacks[gNameOrder], gAvgPotAttacks[gNameOrder], gAvgHitDmgAttacks[gNameOrder], gAvgHitPotAttacks[gNameOrder], gAvgCritDmgAttacks[gNameOrder], gAvgCritPotAttacks[gNameOrder], gAvgCritChcAttacks[gNameOrder], gAvgCritBonusAttacks[gNameOrder] ])
    
    # List of skills cast
    gCycleSkills = np.array([ r['source'] for r in results if 'source' in r and r['type'] == 'skill' ])
    
    return (avgDPS, avgTPSPS, tSkill, gCycleSkills, gTimeline, gDPS)

def sortTable(tSkill):
    """ Sort tSkill by decreasing total damage
    """
    # Order of the skills by decreasing total damage
    gDmgOrder = [ i[0] for i in sorted(enumerate([ float(t) for t in tSkill[2] ]), key = lambda x: x[1], reverse = True) ]
    for i in range(len(tSkill)):
        tSkill[i] = tSkill[i][gDmgOrder]
    return tSkill

def showGraphs(gTimeline, gDPS, tSkill) :
    """Displays 2 graphs:
    DPS over time
    Damage distribution by skill
    """
    # DPS over time
    pl.plot(gTimeline, gDPS)
    pl.show()
    # Damage distribution
    pl.bar(range(len(tSkill[0])), tSkill[2])
    pl.xticks([ i + 0.5 for i in range(len(tSkill[0])) ], tSkill[0], rotation=90)
    pl.show()

def printTable(table, titles) :
    """Pretty print of a table with given titles
    """
    # Creates a format for each line with variable width
    row_format = ''.join( '{:>' + str(max([len(titles[i])] + [ len('{:.3f}'.format(float(t))) if isFloat(t) else len(t) for t in table[i] ]) + 1) + '}' for i in range(len(titles)) )
    # Print the titles
    print row_format.format(*titles)
    # Print each line of the table
    for i in range(len(table[0])):
        print row_format.format(*[ '{:.3f}'.format(float(t[i])) if isFloat(t[i]) else t[i] for t in table ])

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
    randomize = True,
    autoAttack = 0.5,
    dotTick = 1,
    dmgLimit = None,
    verbose = True,
    gDeltaT = 5,
) :
    """Runs a complete simulation
    model: model to be used; the name of a file in the priorityLists folder
    strength, criticalHitRate, determination, skillSpeed, weaponDamage,
    weaponDelay, weaponType: main stats of the character
    duration: fight duration target, in min
    variation: fight duration variation, as a ration (0.2 = 20%)
    nbSim: number of simulations to run if randomized
    runStatWeights: if stat weights should be calculated
    randomize: if simulation should be randomized
    autoAttack: timestamp of the first auto-attack
    dotTick: timestamp of the first DoT tick
    dmgLimit: damage limit if damage based instead of time based objective
    verbose: if results should be printed
    gDeltaT: window length for the DPS over time graph, in sec
    """
    # Priority list; loads the file if a file name, otherwise understand model
    # as a priority list object
    if type(model) is str :
        priorityList = priorityParser(model)
    else :
        priorityList = model
    # Format priority list
    plist = formatPriorityList(priorityList)
    # Initial state initializer with constant stats
    initializer = getInitializer(strength,
                                 criticalHitRate,
                                 determination,
                                 skillSpeed,
                                 weaponDamage,
                                 weaponDelay,
                                 weaponType)
    
    # Get damage limit if not already specified
    if not isFloat(dmgLimit) :
        initialState = initializer(autoAttack, dotTick)
        (states, results) = runSim(initialState, plist, duration)
        damageLimit = sum( r['damage'] for r in results if 'damage' in r )
        
        # Returns the damage limit if simulation is to get the damage limit for
        # other simulations
        if dmgLimit == 'get':
            (avgDPS, avgTPSPS, tSkill, gCycleSkills, gTimeline, gDPS) = simulationAnalysis(states, results, gDeltaT)
            return damageLimit
    # Else use the provided damage limit
    else :
        damageLimit = dmgLimit
    
    # Titles for the skill table (cf printTable and simulationAnalysis)
    titles = ['skill', 'ticks', 'totDmg', 'totPot', '%age', 'partialDPS', 'partialPot', 'dmg/tick', 'pot/tick', 'dmg/hit', 'pot/hit', 'dmg/crit', 'pot/crit', 'crit%', 'crit bonus' ]
    # If simulation is randomized
    if randomize:
        # Create arrays for results of each simulation
        avgDPS = []
        avgTPSPS = []
        tSkill = []
        statWeights = []
        # Index of the sample for single simulation results:
        # skill list in order, graphs and states/results
        sampleIndex = random.choice(range(nbSim))
        for i in range(nbSim):
            # Randomize first auto-attack timestamp, first DoT tick timestamp
            # and damage limit within +/- variation
            autoAttack = random.uniform(0, weaponDelay)
            dotTick = random.uniform(0, 3)
            randDmgLimit = random.uniform(damageLimit * (1 - variation), damageLimit * (1 + variation))
            # Run simulation
            initialState = initializer(autoAttack, dotTick, randDmgLimit)
            (locStates, locResults) = runSim(initialState, plist)
            # Retrieve numeric analysis of the results
            (locAvgDPS, locAvgTPSPS, locTSkill, locGCycleSkills, locGTimeline, locGDPS) = simulationAnalysis(locStates, locResults, gDeltaT)
            # Update arrays of results
            avgDPS = avgDPS + [locAvgDPS]
            avgTPSPS = avgTPSPS + [locAvgTPSPS]
            tSkill = tSkill + [locTSkill]
            # Fill single simulation sample if chosen index
            if i == sampleIndex:
                states = locStates
                results = locResults
                gCycleSkills = locGCycleSkills
                gTimeline = locGTimeline
                gDPS = locGDPS
                sTSkill = locTSkill
            # TODO ############################################################
            # stat weights for each simulation if asked for it
            locStatWeights = {}
            if runStatWeights:
                locStatWeights = getStatsWeights(initialState, priorityList, damageLimit, avgDPS)
            statWeights = statWeights + [locStatWeights]
        # Averages results of skill table through the different simulations
        avgTSkill = sTSkill
        for i in range(1, len(avgTSkill)) :
            for j in range(len(avgTSkill[i])) :
                avgTSkill[i][j] = np.mean([ float(ts[i][j]) for ts in tSkill ])
        # Sorts average table and example table
        sTSkill = sortTable(sTSkill)
        avgTSkill = sortTable(avgTSkill)
        if verbose:
            # Displays graphs of results for the single simulation example:
            # DPS over time and DPS distribution across skills
            showGraphs(gTimeline, gDPS, sTSkill)
            # Shows DPS distribution across simulations
            pl.hist(avgDPS, bins = 20)
            pl.show()
            # Shows the first 50 actions of the character for the example
            print 'First 50 actions:'
            for i in range(50):
                print gCycleSkills[i]
            # Pretty prints the table of skills averaged across simulations
            printTable(avgTSkill, titles) 
            # Average DPS and TPSPS averaged across simulations
            print 'average DPS: ', np.mean(avgDPS)
            print 'average TP spent per second',  np.mean(avgTPSPS)
        # Returns all elements necessary for further analyses
        return (states, results, np.mean(avgDPS), np.mean(avgTPSPS), avgTSkill, gCycleSkills, statWeights)
    # If not randomized
    else:
        #Runs simulation
        initialState = initializer(autoAttack, dotTick, damageLimit)
        (states, results) = runSim(initialState, plist)
        # Gets numeric analysis of the results
        (avgDPS, avgTPSPS, tSkill, gCycleSkills, gTimeline, gDPS) = simulationAnalysis(states, results, gDeltaT)
        # Gets the stat weights if asked for it
        statWeights = {}
        if runStatWeights:
            statWeights = getStatsWeights(initialState, priorityList, damageLimit, avgDPS)
        # Sorts the skill table
        tSkill = sortTable(tSkill)
        if verbose:
            # Displays graphs of results for the simulation:
            # DPS over time and DPS distribution across skills
            showGraphs(gTimeline, gDPS, tSkill)
            # Shows the first 50 actions of the character
            print 'First 50 actions:'
            for i in range(50):
                print gCycleSkills[i]
            # Pretty prints the table of skills
            printTable(tSkill, titles) 
            # Average DPS and TPSPS
            print 'average DPS: ', avgDPS
            print 'average TP spent per second', avgTPSPS
        # Returns all elements necessary for further analyses
        return (states, results, avgDPS, avgTPSPS, tSkill, gCycleSkills, statWeights)


  