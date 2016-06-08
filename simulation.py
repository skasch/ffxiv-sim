# -*- coding: utf-8 -*-
"""
Created on Thu May 19 15:30:35 2016

@author: rmondoncancel
"""
# imports
from simulator import simulate

#model = 'monk'
#strength = 1306
#criticalHitRate = 814
#determination = 523
#skillSpeed = 741
#weaponDamage = 81
#weaponDelay = 2.56
#weaponType = 'blunt'
#duration = 8
#variation = 0.2
#nbSim = 100
#runStatWeights = False
#randomize = True

model = raw_input('Priority model: ')
strength = int(raw_input('Character strength: '))
criticalHitRate = int(raw_input('Character critical hit rate: '))
determination = int(raw_input('Character determination: '))
skillSpeed = int(raw_input('Character skill speed: '))
weaponDamage = int(raw_input('Weapon damage: '))
weaponDelay = float(raw_input('Weapon delay: '))
weaponType = raw_input('Weapon type [slashing, piercing or blunt]: ')
duration = float(raw_input('Fight duration [in minutes]: '))
variation = float(raw_input('Fight duration variation [0.2 for 20%]: '))
nbSim = int(raw_input('Number of simulations: '))
runStatWeights = raw_input('Compute stat weights [Y/N]: ').lower() == 'y'
randomize = raw_input('Randomize simulations [Y/N]: ').lower() == 'y'

(states, results, avgDPS, avgTPSPS, tSkillCounts, gCycleSkills, statWeights) = simulate(
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
    randomize
)


