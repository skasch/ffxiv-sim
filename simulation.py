# -*- coding: utf-8 -*-
"""
Created on Thu May 19 15:30:35 2016

@author: rmondoncancel
"""
# imports
from simulator import simulate

# Example of inputs / uncomment that and comment CLI inputs to run the 
# simulation directly
model = 'monk'
duration = 10
variation = 0.2
nbSim = 20
useTp = True
runStatWeights = False
plotStats = []
randomize = False

#model = raw_input('Priority model: ')
#duration = float(raw_input('Fight duration [in minutes]: '))
#variation = float(raw_input('Fight duration variation [0.2 for 20%]: '))
#nbSim = int(raw_input('Number of simulations: '))
#runStatWeights = raw_input('Compute stat weights [Y/N]: ').lower()[0] == 'y'
#randomize = raw_input('Randomize simulations [Y/N]: ').lower()[0] == 'y'

# Run the simulation with given parameters
(states, results, avgDPS, avgTPSPS, tSkill, gCycleSkills, statWeights) = simulate(
    model,
    duration,
    variation,
    nbSim,
    useTp,
    runStatWeights = runStatWeights,
    randomize = randomize,
#    plotStats
)