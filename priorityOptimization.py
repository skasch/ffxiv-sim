# -*- coding: utf-8 -*-
"""
Created on Fri Jun 03 10:03:13 2016

@author: rmondoncancel
"""

import copy
from simulator import simulate
from priorityParser import priorityParser, priorityDeparser

model = 'monk'
strength = 1306
criticalHitRate = 814
determination = 523
skillSpeed = 741
weaponDamage = 81
weaponDelay = 2.56
weaponType = 'blunt'
duration = 8
variation = 0
nbSim = 1
runStatWeights = False
randomize = False

priorityList = priorityParser(model)

dmgLimit = simulate(
    priorityList,
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
    runStatWeights,
    randomize,
    dmgLimit = 'get',
    verbose = False
)

(_, _, refDPS, _, _, _, _) = simulate(
    priorityList,
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
    runStatWeights,
    randomize,
    dmgLimit = dmgLimit,
    verbose = False
)

print 'Reference DPS: ', refDPS

unoptimized = True
while unoptimized :
    unoptimized = False
    for i in range(len(priorityList) - 1):
        for j in range(i + 1, len(priorityList)):
#        j = i+1
            newPriorityList = copy.deepcopy(priorityList)
            newPriorityList[i], newPriorityList[j] = newPriorityList[j], newPriorityList[i]
            (_, _, newDPS, _, _, _, _) = simulate(
                newPriorityList,
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
                runStatWeights,
                randomize,
                dmgLimit = dmgLimit,
                verbose = False
            )
            print newDPS
            if newDPS > refDPS * 1.0001:
                unoptimized = True
                bestPerm = (i, j)
                refDPS = newDPS
        #
    if unoptimized :
        print 'Reference DPS: ', refDPS
        priorityList[bestPerm[0]], priorityList[bestPerm[1]] = priorityList[bestPerm[1]], priorityList[bestPerm[0]]

print priorityDeparser(priorityList)
        