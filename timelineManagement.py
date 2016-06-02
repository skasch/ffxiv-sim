# -*- coding: utf-8 -*-
"""
Created on Tue May 31 17:00:31 2016

@author: rmondoncancel
"""
from priorityManagement import reduceConditions
from skills import s
from stateManagement import \
    nextAction, removeBuff, removeDebuff, removeCooldown
from applyActions import  applyDot, applySingleDot, applySkill, applyAutoAttack

def findBestSkill(state, priorityList) :
    skill = None
    for priorityElement in priorityList :
        if reduceConditions(state, priorityElement['condition']) :
            skill = s()[priorityElement['group']][priorityElement['name']]
            break
    return skill

def solveCurrentAction(state, priorityList) :
    actionType = state['timeline']['currentAction']['type']
    result = {}
    if actionType == 'removeBuff' :
        newState = removeBuff(state, [ state['timeline']['currentAction']['name'] ])
        newState = nextAction(newState)
    elif actionType == 'removeDebuff' :
        newState = removeDebuff(state, [ state['timeline']['currentAction']['name'] ])
        newState = nextAction(newState)
    elif actionType == 'removeCooldown' :
        newState = removeCooldown(state, [ state['timeline']['currentAction']['name'] ])
        newState = nextAction(newState)
    elif actionType == 'dotTick' :
        newState = applyDot(state)
    elif actionType == 'dot' :
        (newState, result) = applySingleDot(state, [ d for d in state['enemy']['debuff'] if d['name'] == state['timeline']['currentAction']['name'] ][0])
    elif any(state['timeline']['prepull'].values()) and (actionType == 'gcdSkill' or actionType == 'instantSkill') :
        prepullPriorityList = [ priorityElement for priorityElement in priorityList if 'prepull' in priorityElement ]
        bestSkill = findBestSkill(state, prepullPriorityList)
        (newState, result) = applySkill(state, bestSkill)
    elif actionType == 'gcdSkill' or actionType == 'instantSkill' :
        bestSkill = findBestSkill(state, priorityList)
        (newState, result) = applySkill(state, bestSkill)
    elif actionType == 'autoAttack' :
        (newState, result) = applyAutoAttack(state)
    return (newState, result)