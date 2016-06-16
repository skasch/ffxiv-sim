# -*- coding: utf-8 -*-
"""
Created on Tue May 31 17:00:31 2016

@author: rmondoncancel
"""
from priorityManagement import reduceConditions
from skills import s
from stateManagement import \
    nextAction, removeBuff, removeDebuff, removeCooldown
from applyActions import \
    applyDot, applySingleDot, applySkill, applyAutoAttack, applySpecialAction

def findBestSkill(state, priorityList) :
    """Finds the best skill possible for a given state, i.e. the highest skill
    in the priorityList whose conditions are True
    """
    # If no skill found, returns None
    skill = None
    # Tests for each element in the priorityList
    for priorityElement in priorityList :
        # If the condition is True for the current state
        if reduceConditions(state, priorityElement['condition']) :
            # If True, return this skill as the best possible skill
            skill = s(state['player']['class'])[priorityElement['group']][priorityElement['name']]
            break
    return skill

def solveCurrentAction(state, priorityList) :
    """Solve the current action of the state, given a specific priorityList
    """
    actionType = state['timeline']['currentAction']['type']
    result = {}
    # Action to remove a specific buff
    if actionType == 'removeBuff' :
        newState = removeBuff(state, [ state['timeline']['currentAction']['name'] ])
        newState = nextAction(newState)
    # Action to remove a specific debuff
    elif actionType == 'removeDebuff' :
        newState = removeDebuff(state, [ state['timeline']['currentAction']['name'] ])
        newState = nextAction(newState)
    # Action to remove a specific cooldown (skill now available)
    elif actionType == 'removeCooldown' :
        newState = removeCooldown(state, [ state['timeline']['currentAction']['name'] ])
        newState = nextAction(newState)
    # Action to create the dot actions for each currently applied DoT when the
    # DoT global tick happens
    elif actionType == 'dotTick' :
        newState = applyDot(state)
    # Action to resolve the damage done by a single DoT when the DoT tick 
    # happens
    elif actionType == 'dot' :
        (newState, result) = applySingleDot(state, [ d for d in state['enemy']['debuff'] if d['name'] == state['timeline']['currentAction']['name'] ][0])
    # Action to resolve a specific skill during prepull
    elif any(state['timeline']['prepull'].values()) and (actionType == 'gcdSkill' or actionType == 'instantSkill') :
        prepullPriorityList = [ priorityElement for priorityElement in priorityList if 'prepull' in priorityElement ]
        bestSkill = findBestSkill(state, prepullPriorityList)
        (newState, result) = applySkill(state, bestSkill)
    # Action to resolve a specific skill (gcd or instant)
    elif actionType == 'gcdSkill' or actionType == 'instantSkill' :
        cyclePriorityList = [ priorityElement for priorityElement in priorityList if 'prepull' not in priorityElement ]
        bestSkill = findBestSkill(state, cyclePriorityList)
        (newState, result) = applySkill(state, bestSkill)
    # Action to resolve the damage done by an auto-attack
    elif actionType == 'autoAttack' :
        (newState, result) = applyAutoAttack(state)
    # Action to resolve special actions created by specific mechanisms
    elif actionType == 'special' :
        (newState, result) = applySpecialAction(state, state['timeline']['currentAction']['name'])
    return (newState, result)