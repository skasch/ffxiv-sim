# -*- coding: utf-8 -*-
"""
Created on Tue May 31 17:03:56 2016

@author: rmondoncancel
"""

import copy

def sign(a) :
    return (a>0) - (a<0)

def nextAction(state) :
    newState = copy.deepcopy(state)
    newState['timeline'] = {
        'currentAction': newState['timeline']['nextActions'][0][1],
        'timestamp': newState['timeline']['nextActions'][0][0],
        'prepull': newState['timeline']['prepull'],
        'prepullTimestamp': newState['timeline']['prepullTimestamp'],
        'nextActions': newState['timeline']['nextActions'][1::],
    }
    return newState

def addAction(state, timeDifference, newAction) :
    newState = copy.deepcopy(state)
    newState['timeline']['nextActions'] = sorted(
        newState['timeline']['nextActions'] + [(newState['timeline']['timestamp'] + timeDifference, newAction)],
        lambda x, y: sign(x[0] - y[0])
    )
    return newState
    
def getBuff(state, buffType) :
    return [ b[0]['buff'][buffType] * b[1] for b in state['player']['buff'] if buffType in b[0]['buff'] ]

def applyBuff(state, buf) :
    newState = copy.deepcopy(state)
    bufList = newState['player']['buff']
    bufNames = [ b[0]['name'] for b in bufList ]
    if buf['name'] in bufNames :
        if 'maxStacks' in buf :
            newState['player']['buff'] = [ b if b[0]['name'] != buf['name'] else (b[0], min(b[1] + 1, b[0]['maxStacks'])) for b in bufList ]
            newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1] != { 'type': 'removeBuff', 'name': buf['name'] } ]
            if 'duration' in buf:
                newState = addAction(newState, buf['duration'], { 'type': 'removeBuff', 'name': buf['name'] })
        else :
            newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1] != { 'type': 'removeBuff', 'name': buf['name'] } ]
            if 'duration' in buf:
                newState = addAction(newState, buf['duration'], { 'type': 'removeBuff', 'name': buf['name'] })
    else :
        newState['player']['buff'] = newState['player']['buff'] + [ (buf, 1) ]
        if 'duration' in buf:
            newState = addAction(newState, buf['duration'], { 'type': 'removeBuff', 'name': buf['name'] })
    return newState
    
def removeBuff(state, remBuff) :
    newState = copy.deepcopy(state)
    newState['player']['buff'] = [ b for b in newState['player']['buff'] if b[0]['name'] not in remBuff ]
    newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1] not in [ { 'type': 'removeBuff', 'name': bn } for bn in remBuff ] ]
    return newState
    
def getDebuff(state, debuffType) :
    return [ b['props'][debuffType] for b in state['enemy']['debuff'] if debuffType in b['props'] ]

def applyDebuff(state, debuf) :
    newState = copy.deepcopy(state)
    snapDebuf = copy.deepcopy(debuf)
    if snapDebuf['type'] == 'DoT':
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
    if debuf['name'] in debufNames :
        newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1] != { 'type': 'removeDebuff', 'name': debuf['name'] } ]
        newState['enemy']['debuff'] = [ d for d in newState['enemy']['debuff'] if d['name'] != debuf['name'] ]
    newState['enemy']['debuff'] = newState['enemy']['debuff'] + [ snapDebuf ]
    newState = addAction(newState, debuf['duration'], { 'type': 'removeDebuff', 'name': debuf['name'] })
    return newState
    
def removeDebuff(state, remDebuff) :
    newState = copy.deepcopy(state)
    newState['enemy']['debuff'] = [ d for d in newState['enemy']['debuff'] if d['name'] not in remDebuff ]
    newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1] not in [ { 'type': 'removeDebuff', 'name': dn } for dn in remDebuff ] ]
    return newState
    
def removeCooldown(state, remCooldown) :
    newState = copy.deepcopy(state)
    newState['player']['cooldown'] = [ c for c in newState['player']['cooldown'] if c not in remCooldown ]
    newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1] not in [ { 'type': 'removeCooldown', 'name': cn } for cn in remCooldown ] ]
    return newState

def getResistance(state, resType) :
    debufF = reduce(lambda x, y: x + y, getDebuff(state, resType), 0)
    return state['enemy']['resistance'][resType] + debufF