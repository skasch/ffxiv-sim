# -*- coding: utf-8 -*-
"""
Created on Tue May 31 16:58:16 2016

@author: rmondoncancel
"""

import copy
from skills import s
from buffs import b

def operatorToFunction(operator) :
    """Transform a priority list operator as a string to the matching 
    comparison function for conditions
    """
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

def formatPriorityList(priorityList, pClass) :
    """Format a priority list to add hidden conditions for each skill
    See addHiddenConditions for more details
    """
    return [ addHiddenConditions(pe, pClass) for pe in priorityList ]
    
def addHiddenConditions(priorityElement, pClass) :
    """Add hidden conditions for a priority element
    * Add a condition on GCD type (global vs instant) to use the correct skills
      for a given action
    * Check for required buffs if skill require a given buff to be castable
    * Check if skill is on cooldown if skill has a cooldown
    * Prevent instant skills from delaying the GCD
    * Add additional conditions present in skill description
    """
    # Get the skill matching the priority element
    skill = s(pClass)[priorityElement['group']][priorityElement['name']]
    newPriorityElement = copy.deepcopy(priorityElement)
    # Add GCD type check to condition
    if 'condition' not in newPriorityElement :
        # Add a condition key if absent
        newPriorityElement['condition'] = {
            'type': 'gcdType',
            'comparison': 'is',
            'value': skill['gcdType']
        }
    else :
        # Add the GCD type check to the existing condition if it already exists
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
    # Add required buff condition; required buffs are on 'or', so it will match
    # if any of the requiredBuff property of skill is present
    # Also, if the buff has stacks, it will by default check if the buff is
    # at max stacks rather than just present
    if 'requiredBuff' in skill :
        reqBufList = []
        # Loop on required buffs
        for bufName in skill['requiredBuff'] :
            # Check if buffs has stacks
            if 'maxStacks' in b(pClass)[bufName] :
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
    # Add a condition to check if skill is on cooldown if it has one
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
    # Prevent instant skills from delaying GCD by default
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
    # Add skill specific skills if present
    if 'condition' in skill :
        newPriorityElement['condition'] = {
            'logic': 'and',
            'list': [
                newPriorityElement['condition'],
                skill['condition'],            
            ]
        }
    return newPriorityElement

def actionToGcdType(actionType) :
    """Returns the gcdType matching a given actionType
    """
    if actionType == 'gcdSkill':
        return 'global'
    elif actionType == 'instantSkill':
        return 'instant'

def getConditionValue(state, condition) :
    """Returns the value to check for a given single condition
    switch on the condition type to return the matching value in the state
    Current types are:
    * buffPresent: True if buff is present in state else False
    * buffAtMaxStacks: True if buff is at max stacks in state else False
    * buffTimeLeft: time left before the buff drops in state; 0 if absent
    * debuffPresent: True if debuff is present in state else False
    * debuffTimeLeft: time left before the debuff drops in state; 0 if absent
    * cooldownPresent: True if skill is on cooldown in state else False
    * cooldownTimeLeft: time left before the skill is available again in state; 
        0 if absent
    * gcdType: gcdType of current skill (global/instant)
    * gcdDelay: how much would the skill delay the next GCD if cast
    * enemy: enemy specific values
        * lifePercent: percent of life left on the enemy; 100% if time based 
          simulation
    """
    if condition['type'] == 'buffPresent':
        return condition['name'] in [ bf[0]['name'] for bf in state['player']['buff'] ]
    elif condition['type'] == 'buffAtMaxStacks':
        return condition['name'] in [ bf[0]['name'] for bf in state['player']['buff'] if 'maxStacks' in b(state['player']['class'])[bf[0]['name']] and bf[1] == b(state['player']['class'])[bf[0]['name']]['maxStacks'] ]
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
    elif condition['type'] == 'state':
        if condition['name'] == 'enemyLifePercent' :
            if 'hp' not in state['enemy'] or 'maxHp' not in state['enemy'] :
                return 100
            return 100 * state['enemy']['hp'] / state['enemy']['maxHp']
        elif condition['name'] == 'lastGCD' :
            return state['timeline']['lastGCD'] if 'lastGCD' in state['timeline'] else None

def testCondition(state, condition) :
    """Test a single condition
    Compares the value returned by getConditionalValue to the value of the
    condition with the comparison operation chosen
    """
    val = getConditionValue(state, condition)
    return operatorToFunction(condition['comparison'])(val, condition['value'])

def reduceConditions(state, conditions) :
    """Reduce the condition of a complex priority element condition
    applies testCondition if condition is single, else reduce the condition 
    list with the logic if the condition is complex (with and/or)
    """
    if 'logic' in conditions:
        return reduce(operatorToFunction(conditions['logic']), [ reduceConditions(state, cond) for cond in conditions['list'] ])
    return testCondition(state, conditions)