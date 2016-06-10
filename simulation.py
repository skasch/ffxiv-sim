# -*- coding: utf-8 -*-
"""
Created on Thu May 19 15:30:35 2016

@author: rmondoncancel
"""
# imports
from simulator import simulate

# Example of inputs / uncomment that and comment CLI inputs to run the 
# simulation directly
#model = 'monk'
#strength = 1306
#criticalHitRate = 814
#determination = 523
#skillSpeed = 741
#weaponDamage = 81
#weaponDelay = 2.56
#weaponType = 'blunt'
#duration = 5
#variation = 0.2
#nbSim = 10
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
runStatWeights = raw_input('Compute stat weights [Y/N]: ').lower()[0] == 'y'
randomize = raw_input('Randomize simulations [Y/N]: ').lower()[0] == 'y'

# Run the simulation with given parameters
(states, results, avgDPS, avgTPSPS, tSkill, gCycleSkills, statWeights) = simulate(
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


