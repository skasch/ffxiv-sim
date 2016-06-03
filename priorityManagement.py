# -*- coding: utf-8 -*-
"""
Created on Tue May 31 16:58:16 2016

@author: rmondoncancel
"""

import copy
from skills import s
from buffs import b

def operatorToFunction(operator) :
    if operator == 'is':
        return lambda x, y: x == y
    elif operator == '>=':
        return lambda x, y: x >= y
    elif operator == '>':
        return lambda x, y: x > y
    elif operator == '<=':
        return lambda x, y: x <= y
    elif operator == '<':
        return lambda x, y: x < y
    elif operator == 'isnt':
        return lambda x, y: x != y
    elif operator == 'and':
        return lambda x, y: x and y
    elif operator == 'or':
        return lambda x, y: x or y

def formatPriorityList(priorityList) :
    return [ addHiddenConditions(pe) for pe in priorityList ]
    
def addHiddenConditions(priorityElement) :
    skill = s()[priorityElement['group']][priorityElement['name']]
    newPriorityElement = copy.deepcopy(priorityElement)
    if 'condition' not in newPriorityElement :
        newPriorityElement['condition'] = {
            'type': 'gcdType',
            'comparison': 'is',
            'value': skill['gcdType']
        }
    else :
        newPriorityElement['condition'] = {
            'logic': 'and',
            'list': [
                newPriorityElement['condition'],
                {
                    'type': 'gcdType',
                    'comparison': 'is',
                    'value': skill['gcdType']
                },
            ],
        }
    if 'requiredBuff' in skill :
        reqBufList = []
        for bufName in skill['requiredBuff'] :
            if 'maxStacks' in b()[bufName] :
                reqBufList = reqBufList + [ {
                    'type': 'buffAtMaxStacks', 
                    'name': bufName,
                    'comparison': 'is',
                    'value': True,
                } ]
            else :
                reqBufList = reqBufList + [ {
                    'type': 'buffPresent', 
                    'name': bufName,
                    'comparison': 'is',
                    'value': True,
                } ]
        newPriorityElement['condition'] = {
            'logic': 'and',
            'list': [
                newPriorityElement['condition'],
                {
                    'logic': 'or',
                    'list': reqBufList,
                },
            ],
        }
    if skill['cooldown'] > 0:
        newPriorityElement['condition'] = {
            'logic': 'and',
            'list': [
                newPriorityElement['condition'],
                {
                    'type': 'cooldownPresent',
                    'name': skill['name'],
                    'comparison': 'is',
                    'value': False,
                },
            ],
        }
    if skill['gcdType'] == 'instant' and 'prepull' not in newPriorityElement:
        newPriorityElement['condition'] = {
            'logic': 'and',
            'list': [
                newPriorityElement['condition'],
                {
                    'type': 'gcdDelay',
                    'delay': skill['animationLock'],
                    'comparison': '<=',
                    'value': 0,
                },
            ],
        }
    return newPriorityElement

def actionToGcdType(actionType) :
    if actionType == 'gcdSkill':
        return 'global'
    elif actionType == 'instantSkill':
        return 'instant'

def getConditionValue(state, condition) :
    if condition['type'] == 'buffPresent':
        return condition['name'] in [ bf[0]['name'] for bf in state['player']['buff'] ]
    elif condition['type'] == 'buffAtMaxStacks':
        return condition['name'] in [ bf[0]['name'] for bf in state['player']['buff'] if 'maxStacks' in b()[bf[0]['name']] and bf[1] == b()[bf[0]['name']]['maxStacks'] ]
    elif condition['type'] == 'buffTimeLeft':
        timers = [ na[0] - state['timeline']['timestamp'] for na in state['timeline']['nextActions'] if na[1] == { 'type': 'removeBuff', 'name': condition['name'] } ]
        if len(timers) == 0:
            return 0
        return min(timers)
    elif condition['type'] == 'debuffPresent':
        return condition['name'] in [ d['name'] for d in state['enemy']['debuff'] ]
    elif condition['type'] == 'debuffTimeLeft':
        timers = [ na[0] - state['timeline']['timestamp'] for na in state['timeline']['nextActions'] if na[1] == { 'type': 'removeDebuff', 'name': condition['name'] } ]
        if len(timers) == 0:
            return 0
        return min(timers)
    elif condition['type'] == 'cooldownPresent':
        return condition['name'] in state['player']['cooldown']
    elif condition['type'] == 'cooldownTimeLeft':
        timers = [ na[0] - state['timeline']['timestamp'] for na in state['timeline']['nextActions'] if na[1] == { 'type': 'removeCooldown', 'name': condition['name'] } ]
        if len(timers) == 0:
            return 0
        return min(timers)
    elif condition['type'] == 'gcdType':
        return actionToGcdType(state['timeline']['currentAction']['type'])
    elif condition['type'] == 'gcdDelay':
        if state['timeline']['currentAction']['type'] == 'gcdSkill':
            return condition['delay']
        nextGcdTimestamp = min( na[0] for na in state['timeline']['nextActions'] if na[1]['type'] == 'gcdSkill' )
        return max(0, state['timeline']['timestamp'] + condition['delay'] - nextGcdTimestamp)

def testCondition(state, condition) :
    val = getConditionValue(state, condition)
    return operatorToFunction(condition['comparison'])(val, condition['value'])

def reduceConditions(state, conditions) :
    if 'logic' in conditions:
        return reduce(operatorToFunction(conditions['logic']), [ reduceConditions(state, cond) for cond in conditions['list'] ])
    return testCondition(state, conditions)