# -*- coding: utf-8 -*-
"""
Created on Tue May 31 17:03:56 2016

@author: rmondoncancel
"""

import copy

def sign(a) :
    """Helper returning the sign of a
    """
    return (a>0) - (a<0)

def nextAction(state) :
    """Returns the state at the next action
    """
    newState = copy.deepcopy(state)
    # Updates the timeline to be at the next action, i.e. the action with the 
    # lowest timestamp in the list of next actions
    newState['timeline']['currentAction'] = newState['timeline']['nextActions'][0][1]
    newState['timeline']['timestamp'] = newState['timeline']['nextActions'][0][0]
    newState['timeline']['nextActions'] = newState['timeline']['nextActions'][1::]
    return newState

def applyTpChange(state, tpDiff) :
    newState = copy.deepcopy(state)
    if 'tp' in newState['player'] :
        newState['player']['tp'] = max(min(newState['player']['tp'] + tpDiff, 1000), 0)
    return newState

def tpTick(state) :
    newState = applyTpChange(state, 60)
    newState = addAction(newState, 3, { 'type': 'tpTick' })
    newState = nextAction(newState)
    return newState

def addAction(state, timeDifference, newAction) :
    """Adds an newAction to a state atfter timeDifference s after the current
    state timestamp
    """
    newState = copy.deepcopy(state)
    # Sorts the nextActions array with the newAction added by their respective
    # Timestamps; adds the newAction at its relevant position
    newTs = newState['timeline']['timestamp'] + timeDifference
    nas = newState['timeline']['nextActions']
    newState['timeline']['nextActions'] = [ na for na in nas if na[0] <= newTs ] + [( newTs, newAction )] + [ na for na in nas if na[0] > newTs ]
    return newState

def applyDamage(state, damage) :
    """Apply damage to the state by reducing the HP of the enemy by the damage
    received
    """
    newState = copy.deepcopy(state)
    # If the enemy does not have HP information, returns the same state
    if 'hp' not in state['enemy'] :
        return newState
    # Reduces HP by damage, min HP being 0
    newState['enemy']['hp'] = max(newState['enemy']['hp'] - damage, 0)
    return newState
    
def getBuff(state, buffType) :
    """Get the lists of buff modifiers for a specific buff type: damage, 
    crit etc...
    """
    return [ b[0]['buff'][buffType] * b[1] for b in state['player']['buff'] if buffType in b[0]['buff'] ]
    
def getDebuff(state, debuffType) :
    """Get the lists of debuff modifiers for a specific debuff type
    """
    return [ b['props'][debuffType] for b in state['enemy']['debuff'] if debuffType in b['props'] ]

def getResistance(state, resType) :
    """Get the resistance ratio for a specific resistance type
    """
    debufF = reduce(lambda x, y: x + y, getDebuff(state, resType), 0)
    return state['enemy']['resistance'][resType] + debufF

def applyBuff(state, buf) :
    """Apply a buff to the state
    """
    newState = copy.deepcopy(state)
    bufList = newState['player']['buff']
    bufNames = [ b[0]['name'] for b in bufList ]
    # If buff already applied
    if buf['name'] in bufNames :
        # If buff has stacks
        if 'maxStacks' in buf :
            # Updates the buff to add a new stack, max being maxStacks
            newState['player']['buff'] = [ b if b[0]['name'] != buf['name'] else (b[0], min(b[1] + 1, b[0]['maxStacks'])) for b in bufList ]
        # Remove the already existing action of the buff falling down
        newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1] != { 'type': 'removeBuff', 'name': buf['name'] } ]
    # If buff not applied
    else :
        # Add the new buff to the buff list
        newState['player']['buff'] = newState['player']['buff'] + [ (buf, 1) ]
    # If the buff has a duration
    if 'duration' in buf:
        # Add an action to make the buff fall down after this duration
        newState = addAction(newState, buf['duration'], { 'type': 'removeBuff', 'name': buf['name'] })
    return newState
    
def removeBuff(state, remBuff) :
    """Remove a buff to the state
    """
    newState = copy.deepcopy(state)
    # Removes the buff from the list of buffs
    newState['player']['buff'] = [ b for b in newState['player']['buff'] if b[0]['name'] not in remBuff ]
    # Removes the potential remaining actions to make the buff fall down, for
    # example if a skill removes a buff with a duration
    newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1] not in [ { 'type': 'removeBuff', 'name': bn } for bn in remBuff ] ]
    return newState

def applyDebuff(state, debuf) :
    """Apply a debuff to a state
    """
    newState = copy.deepcopy(state)
    snapDebuf = copy.deepcopy(debuf)
    # If the debuff is a DoT
    if snapDebuf['type'] == 'DoT':
        # Snapshots the current state for buffs and debuffs to ensure correct
        # resolution of DoT ticks damages
        # Gets the stats, buffs and debuffs currently active
        snapDebuf['snapshot'] = {
            'player': { 
                'baseStats': state['player']['baseStats'],
                'buff': state['player']['buff'],
            },
            'enemy': { 
                'debuff': [ d for d in state['enemy']['debuff'] if d['type'] != 'DoT' ],
            },
        }
    debufList = newState['enemy']['debuff']
    debufNames = [ d['name'] for d in debufList ]
    # If the buff is already applied
    if debuf['name'] in debufNames :
        # Removes the previous applied buff to ensure the correct snapshot is
        # saved
        newState['enemy']['debuff'] = [ d for d in newState['enemy']['debuff'] if d['name'] != debuf['name'] ]
        # Removes the potential debuff falling down actions
        newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1] != { 'type': 'removeDebuff', 'name': debuf['name'] } ]
    # Add the current debuff to the debuff list with the potential snapshot
    newState['enemy']['debuff'] = newState['enemy']['debuff'] + [ snapDebuf ]
    # Add an action to make the debuff fall down after its duration
    newState = addAction(newState, debuf['duration'], { 'type': 'removeDebuff', 'name': debuf['name'] })
    return newState
    
def removeDebuff(state, remDebuff) :
    """Removes a debuff from a state
    """
    newState = copy.deepcopy(state)
    # Removes the debuff from the list of debuffs
    newState['enemy']['debuff'] = [ d for d in newState['enemy']['debuff'] if d['name'] not in remDebuff ]
    # Removes the potential remaining actions to make the debuff fall down
    newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1] not in [ { 'type': 'removeDebuff', 'name': dn } for dn in remDebuff ] ]
    return newState
    
def removeCooldown(state, remCooldown) :
    """Removes a cooldown from a state when the skill is newly available
    """
    newState = copy.deepcopy(state)
    # Removes the cooldown from the list of cooldowns
    newState['player']['cooldown'] = [ c for c in newState['player']['cooldown'] if c not in remCooldown ]
    # Removes the potential remaining actions to make the cooldown end
    newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1] not in [ { 'type': 'removeCooldown', 'name': cn } for cn in remCooldown ] ]
    return newState