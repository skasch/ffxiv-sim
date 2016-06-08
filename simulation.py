# -*- coding: utf-8 -*-
"""
Created on Thu May 19 15:30:35 2016

@author: rmondoncancel
"""
# imports
from simulator import simulate

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
random = False

(states, results, avgDPS, tSkillCounts, gCycleSkills, statWeights) = simulate(
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
    runStatWeights,
    random
)
