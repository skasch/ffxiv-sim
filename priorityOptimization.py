# -*- coding: utf-8 -*-
"""
Created on Fri Jun 03 10:03:13 2016

@author: rmondoncancel
"""

import copy
from simulator import simulate
from priorityParser import priorityParser, priorityDeparser

# Run the optimization algorithm to find the best priority order to maximize 
# the DPS

# Simulation parameters
model = 'monk'
duration = 5
variation = 0
nbSim = 1
runStatWeights = False
randomize = False

# Get priority list
(priorityList, character) = priorityParser(model)

# Get damage limit to run simulation with HP limit
dmgLimit = simulate(
    (priorityList, character),
    duration,
    variation,
    nbSim,
    runStatWeights = runStatWeights,
    randomize = randomize,
    dmgLimit = 'get',
    verbose = False
)

# Get reference DPS for damage limit
(_, _, refDPS, _, _, _, _) = simulate(
    (priorityList, character),
    duration,
    variation,
    nbSim,
    runStatWeights = runStatWeights,
    randomize = randomize,
    dmgLimit = dmgLimit,
    verbose = False
)

print 'Reference DPS: ', refDPS

unoptimized = True
while unoptimized :
    unoptimized = False
    # Try to switch two elements from the priority list and calcuate the new DPS
    for i in range(len(priorityList) - 1):
#        for j in range(i + 1, len(priorityList)):
        j = i+1
        newPriorityList = copy.deepcopy(priorityList)
        newPriorityList[i], newPriorityList[j] = newPriorityList[j], newPriorityList[i]
        (_, _, newDPS, _, _, _, _) = simulate(
            (newPriorityList, character),
            duration,
            variation,
            nbSim,
            runStatWeights = runStatWeights,
            randomize = randomize,
            dmgLimit = dmgLimit,
            verbose = False
        )
        print newDPS
        # if new DPS is higher than old DPS update reference DPS
        if newDPS > refDPS * 1.0001:
            unoptimized = True
            bestPerm = (i, j)
            refDPS = newDPS
        #
    if unoptimized :
        # if reference DPS has changed, update priority list accordingly
        print 'Reference DPS: ', refDPS
        priorityList[bestPerm[0]], priorityList[bestPerm[1]] = priorityList[bestPerm[1]], priorityList[bestPerm[0]]

# Print the priority list in correct order
print priorityDeparser(priorityList)
        