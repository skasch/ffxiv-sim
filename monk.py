# -*- coding: utf-8 -*-
"""
Created on Thu May 19 15:30:35 2016

@author: rmondoncancel
"""
# imports
import copy

# Skills
s = {}
# Pugilist
s['pugilist'] = {}
s['pugilist']['bootshine'] = {
    'name': 'bootshine',
    'level': 1,
    'tpCost': 60,
    'gcdType': 'global',
    'cooldown': 0,
    'castTime': 0,
    'range': 3,
    'radius': 0,
    'potency': 150,
    'type': 'blunt',
    'skillBuff': ['bootshineCrit'],
    'removeBuff': ['opoOpoForm'],
    'addBuff': ['raptorForm'],
}
s['pugilist']['trueStrike'] = {
    'name': 'trueStrike',
    'level': 2,
    'tpCost': 50,
    'gcdType': 'global',
    'cooldown': 0,
    'castTime': 0,
    'range': 3,
    'radius': 0,
    'potency': 190,
    'type': 'blunt',
    'requiredBuff': ['raptorForm', 'perfectBalance'],
    'removeBuff': ['raptorForm'],
    'addBuff': ['coerlForm'],
}
s['pugilist']['snapPunch'] = {
    'name': 'snapPunch',
    'level': 6,
    'tpCost': 50,
    'gcdType': 'global',
    'cooldown': 0,
    'castTime': 0,
    'range': 3,
    'radius': 0,
    'potency': 180,
    'type': 'blunt',
    'requiredBuff': ['coerlForm', 'perfectBalance'],
    'removeBuff': ['coerlForm'],
    'addBuff': ['opoOpoForm', 'greasedLightning'],
}
s['pugilist']['internalRelease'] = {
    'name': 'internalRelease',
    'level': 12,
    'tpCost': 0,
    'gcdType': 'instant',
    'cooldown': 60,
    'castTime': 0,
    'addBuff': ['internalRelease'],
}
s['pugilist']['touchOfDeath'] = {
    'name': 'touchOfDeath',
    'level': 15,
    'tpCost': 80,
    'gcdType': 'global',
    'cooldown': 0,
    'castTime': 0,
    'range': 3,
    'radius': 0,
    'potency': 20,
    'type': 'blunt',
    'addDebuff': ['touchOfDeath'],
}
s['pugilist']['twinSnakes'] = {
    'name': 'twinSnakes',
    'level': 18,
    'tpCost': 60,
    'gcdType': 'global',
    'cooldown': 0,
    'castTime': 0,
    'range': 3,
    'radius': 0,
    'potency': 140,
    'type': 'blunt',
    'requiredBuff': ['raptorForm', 'perfectBalance'],
    'removeBuff': ['raptorForm'],
    'addBuff': ['coerlForm', 'twinSnakes'],
}
s['pugilist']['demolish'] = {
    'name': 'demolish',
    'level': 30,
    'tpCost': 130,
    'gcdType': 'global',
    'cooldown': 0,
    'castTime': 0,
    'range': 3,
    'radius': 0,
    'potency': 70,
    'type': 'blunt',
    'requiredBuff': ['coerlForm', 'perfectBalance'],
    'removeBuff': ['coerlForm'],
    'addBuff': ['opoOpoForm', 'greasedLightning'],
    'addDebuff': ['demolish'],
}
s['pugilist']['steelPeak'] = {
    'name': 'steelPeak',
    'level': 38,
    'tpCost': 0,
    'gcdType': 'instant',
    'cooldown': 40,
    'castTime': 0,
    'range': 3,
    'radius': 0,
    'potency': 150,
    'type': 'blunt',
}
s['pugilist']['howlingFist'] = {
    'name': 'howlingFist',
    'level': 46,
    'tpCost': 0,
    'gcdType': 'instant',
    'cooldown': 60,
    'castTime': 0,
    'range': 10,
    'radius': 10,
    'potency': 210,
    'type': 'blunt',
}
s['pugilist']['perfectBalance'] = {
    'name': 'perfectBalance',
    'level': 46,
    'tpCost': 0,
    'gcdType': 'instant',
    'cooldown': 60,
    'castTime': 0,
    'addBuff': ['perfectBalance'],
}

# Monk
s['monk'] = {}
s['monk']['shoulderTackle'] = {
    'name': 'shoulderTackle',
    'level': 35,
    'tpCost': 0,
    'gcdType': 'instant',
    'cooldown': 30,
    'castTime': 0,
    'range': 20,
    'radius': 0,
    'potency': 100,
    'type': 'blunt',
}
s['monk']['fistOfFire'] = {
    'name': 'fistOfFire',
    'level': 40,
    'gcdType': 'instant',
    'cooldown': 3,
    'castTime': 0,
    'addBuff': ['fistOfFire'],
}
s['monk']['dragonKick'] = {
    'name': 'dragonKick',
    'level': 50,
    'tpCost': 60,
    'gcdType': 'global',
    'cooldown': 0,
    'castTime': 0,
    'range': 3,
    'radius': 0,
    'potency': 150,
    'type': 'blunt',
    'requiredBuff': ['opoOpoForm', 'perfectBalance'],
    'removeBuff': ['opoOpoForm'],
    'addBuff': ['raptorForm'],
    'addDebuff': ['dragonKick'],
}
s['monk']['meditation'] = {
    'name': 'meditation',
    'level': 54,
    'tpCost': 0,
    'gcdType': 'global',
    'cooldown': 0,
    'castTime': 0,
    'addBuff': ['chakra'],
}
s['monk']['forbiddenChakra'] = {
    'name': 'forbiddenChakra',
    'level': 54,
    'tpCost': 0,
    'gcdType': 'instant',
    'cooldown': 5,
    'castTime': 0,
    'range': 3,
    'radius': 0,
    'potency': 320,
    'type': 'blunt',
    'requiredBuff': ['chakra'],
    'removeBuff': ['chakra'],
}
s['monk']['elixirField'] = {
    'name': 'elixirField',
    'level': 56,
    'tpCost': 0,
    'gcdType': 'instant',
    'cooldown': 30,
    'castTime': 0,
    'range': 0,
    'radius': 5,
    'potency': 220,
    'type': 'blunt',
}
s['monk']['tornadoKick'] = {
    'name': 'tornadoKick',
    'level': 60,
    'tpCost': 0,
    'gcdType': 'instant',
    'cooldown': 40,
    'castTime': 0,
    'range': 3,
    'radius': 0,
    'potency': 330,
    'type': 'blunt',
    'requiredBuff': ['greasedLightning'],
    'removeBuff': ['greasedLightning'],
}

# Lancer
s['lancer'] = {}
s['lancer']['bloodForBlood'] = {
    'name': 'bloodForBlood',
    'level': 34,
    'tpCost': 0,
    'gcdType': 'instant',
    'cooldown': 80,
    'castTime': 0,
    'addBuff': ['bloodForBlood'],
}

# Marauder
s['marauder'] = {}
s['marauder']['fracture'] = {
    'name': 'fracture',
    'level': 6,
    'tpCost': 80,
    'gcdType': 'global',
    'cooldown': 0,
    'castTime': 0,
    'range': 3,
    'radius': 0,
    'potency': 100,
    'type': 'slashing',
    'addDebuff': ['fracture'],
}
s['marauder']['mercyStroke'] = {
    'name': 'mercyStroke',
    'level': 26,
    'tpCost': 0,
    'gcdType': 'instant',
    'cooldown': 90,
    'castTime': 0,
    'range': 3,
    'radius': 0,
    'potency': 200,
    'type': 'slashing',
    'requiredDebuff': ['lowLife'],
}

# Buffs
b = {}
b['opoOpoForm'] = {
    'name': 'opoOpoForm',
    'duration': 10,
    'buff': {},
}
b['raptorForm'] = {
    'name': 'raptorForm',
    'duration': 10,
    'buff': {},
}
b['coerlForm'] = {
    'name': 'coerlForm',
    'duration': 10,
    'buff': {},
}
b['bootshineCrit'] = {
    'name': 'bootshineCrit',
    'duration': 0,
    'buff': {
        'critChance': 1,
    },
}
b['greasedLightning'] = {
    'name': 'greasedLightning',
    'duration': 14,
    'maxStacks': 3,
    'buff': {
        'damage': 0.1,
        'speed': -0.05,
    },
}
b['internalRelease'] = {
    'name': 'internalRelease',
    'duration': 15,
    'buff': {
        'critChance': 0.3,    
    },
}
b['twinSnakes'] = {
    'name': 'twinSnakes',
    'duration': 15,
    'buff': {
        'damage': 0.1,
    },
}
b['perfectBalance'] = {
    'name': 'perfectBalance',
    'duration': 10,
    'buff': {},
}
b['fistOfFire'] = {
    'name': 'fistOfFire',
    'buff': {
        'damage': 0.05,
    },
}
b['chakra'] = {
    'name': 'chakra',
    'maxStack': 5,
    'buff': {},
}
b['bloodForBlood'] = {
    'name': 'bloodForBlood',
    'duration': 20,
    'buff': {
        'damage': 0.1,    
    },
}

# Debuffs
d = {}
d['touchOfDeath'] = {
    'name': 'touchOfDeath',
    'duration': 30,
    'type': 'DoT',
    'props': {
        'potency': 25
    },
}
d['demolish'] = {
    'name': 'demolish',
    'duration': 21,
    'type': 'DoT',
    'props': {
        'potency': 50
    },
}
d['dragonKick'] = {
    'name': 'dragonKick',
    'duration': 15,
    'type': 'debuff',
    'props': {
        'blunt': 0.1,
    },
}
d['fracture'] = {
    'name': 'fracture',
    'duration': 18,
    'type': 'DoT',
    'props': {
        'potency': 20,
    },
}
d['lowLife'] = {
    'name': 'lowLife',
    'type': 'debuff',
}

# Initialize State
state = {}
state['player'] = {
    'buff': [],
    'baseStats': {},
    'cooldown': [],
}
state['enemy'] = {
    'debuff': [],
    'resistance': {
        'slashing': 1,
        'piercing': 1,
        'blunt': 1,
    }
}
state['timeline'] = {
    'timestamp': 0,
    'currentAction': {'type': 'gcdSkill'},
    'nextActions': [ (0.5, {'type': 'autoAttack' }), (1, {'type': 'dotTick' }) ],
}

# Player stats
state['player']['baseStats'] = {
    'strength': 484,
    'criticalHitRate': 393,
    'determination': 282,
    'attackPower': 484,
    'skillSpeed': 413,
    'weaponDamage': 46,
    'weaponDelay': 2.64,
    'weaponType': 'blunt',
}

# Damage formula
# ((Potency/100)*(1+WD*0.0432544)*(STR*0.1027246)*(1+DET/7290)*BUFFS)-2
def baseDamage(pot, wd, st, det, buf) :
    potW = 1./100.
    wdW = 0.0432544
    stW = 0.1027246
    detW = 1./7290.
    bufF = reduce(lambda x, y: x + y, buf, 1)
    return (pot * potW) * (st * stW) * (1. + wd * wdW) * (1. + det * detW) * bufF - 2.

def basePotency(pot, buf) :
    bufF = reduce(lambda x, y: x + y, buf, 1)
    return pot * bufF
    
def critChance(crt, buf) :
    bufF = reduce(lambda x, y: x + y, buf, 0)
    return min(1, ((crt - 354.) / (858. * 5.)) + 0.05 + bufF)

def critBonus(crt) :
    return ((crt - 354.) / (858. * 5.)) + 0.45

def gcdTick(ss, buf) :
    bufF = reduce(lambda x, y: x + y, buf, 1)
    return (2.50245 - ((ss - 354.) * 0.0003776)) * bufF

def dotTick(ss) :
    return ((ss - 354.) / 7722. + 1)
    
def getBuff(state, buffType) :
    return [ b[0]['buff'][buffType] * b[1] for b in state['player']['buff'] if buffType in b[0]['buff'] ]

def sign(a) :
    return (a>0) - (a<0)

def addAction(state, timeDifference, newAction) :
    newState = copy.deepcopy(state)
    newState['timeline']['nextActions'] = sorted(
        newState['timeline']['nextActions'] + [(newState['timeline']['timestamp'] + timeDifference, newAction)],
        lambda x, y: sign(x[0] - y[0])
    )
    return newState

def applyBuff(state, buf) :
    newState = copy.deepcopy(state)
    bufList = newState['player']['buff']
    bufNames = [ b[0]['name'] for b in bufList ]
    if buf['name'] in bufNames :
        if 'maxStacks' in buf :
            newState['player']['buff'] = [ b if b[0]['name'] != buf['name'] else (b[0], min(b[1] + 1, b[0]['maxStacks'])) for b in bufList ]
            newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1] != { 'type': 'removeBuff', 'name': buf['name'] } ]
            newState = addAction(newState, buf['duration'], { 'type': 'removeBuff', 'name': buf['name'] })
        else :
            newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1] != { 'type': 'removeBuff', 'name': buf['name'] } ]
            newState = addAction(newState, buf['duration'], { 'type': 'removeBuff', 'name': buf['name'] })
    else :
        newState['player']['buff'] = newState['player']['buff'] + [ (buf, 1) ]
        newState = addAction(newState, buf['duration'], { 'type': 'removeBuff', 'name': buf['name'] })
    return newState

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
    
def removeBuff(state, remBuff) :
    newState = copy.deepcopy(state)
    newState['player']['buff'] = [ b for b in newState['player']['buff'] if b[0]['name'] not in remBuff ]
    newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1] not in [ { 'type': 'removeBuff', 'name': bn } for bn in remBuff ] ]
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
    
def getDebuff(state, debuffType) :
    return [ b['props'][debuffType] for b in state['enemy']['debuff'] if debuffType in b['props'] ]

def getResistance(state, resType) :
    debufF = reduce(lambda x, y: x + y, getDebuff(state, resType), 0)
    return state['enemy']['resistance'][resType] + debufF

def nextAction(state) :
    newState = copy.deepcopy(state)
    newState['timeline'] = {
        'currentAction': newState['timeline']['nextActions'][0][1],
        'timestamp': newState['timeline']['nextActions'][0][0],
        'nextActions': newState['timeline']['nextActions'][1::],
    }
    return newState

def applyAutoAttack(state) :
    newState = copy.deepcopy(state)
    pot = 100 * newState['player']['baseStats']['weaponDelay'] / 3
    wd = newState['player']['baseStats']['weaponDamage']
    st = newState['player']['baseStats']['strength']
    det = newState['player']['baseStats']['determination']
    crt = newState['player']['baseStats']['criticalHitRate']
    dmgBuf = getBuff(newState, 'damage')
    crtBuf = getBuff(newState, 'critChance')
    baseDmg = baseDamage(pot, wd, st, det, dmgBuf) 
    basePot = basePotency(pot, dmgBuf)
    crtChc = critChance(crt, crtBuf)
    crtBonF = critBonus(crt)
    crtDmg = baseDmg * (1 + crtChc * crtBonF)
    crtPot = basePot * (1 + crtChc * crtBonF)
    dmgRes = getResistance(newState, newState['player']['baseStats']['weaponType'])
    effDmg = crtDmg * dmgRes
    effPot = crtPot * dmgRes
    result = {
        'damage': effDmg,
        'potency': effPot, 
        'type': 'autoAttack',
        'timestamp': newState['timeline']['timestamp'],
    }
    autoAttackDelay = newState['player']['baseStats']['weaponDelay']
    newState = addAction(newState, autoAttackDelay, { 'type': 'autoAttack' })
    newState = nextAction(newState)
    return (newState, result)

def applySkill(state, skill) :
    if skill == None:
        newState = nextAction(state)
        return (newState, {})
    newState = copy.deepcopy(state)
    if 'skillBuff' in skill :
        for bufName in skill['skillBuff'] :
            newState = applyBuff(newState, b[bufName])
    if 'potency' in skill :
        pot = skill['potency']
        wd = newState['player']['baseStats']['weaponDamage']
        st = newState['player']['baseStats']['strength']
        det = newState['player']['baseStats']['determination']
        crt = newState['player']['baseStats']['criticalHitRate']
        dmgBuf = getBuff(newState, 'damage')
        crtBuf = getBuff(newState, 'critChance')
        baseDmg = baseDamage(pot, wd, st, det, dmgBuf) 
        basePot = basePotency(pot, dmgBuf)
        crtChc = critChance(crt, crtBuf)
        crtBonF = critBonus(crt)
        crtDmg = baseDmg * (1 + crtChc * crtBonF)
        crtPot = basePot * (1 + crtChc * crtBonF)
        dmgRes = getResistance(newState, skill['type'])
        effDmg = crtDmg * dmgRes
        effPot = crtPot * dmgRes
        result = {
            'damage': effDmg,
            'potency': effPot, 
            'source': skill['name'],
            'type': 'skill',
            'timestamp': newState['timeline']['timestamp'],
            'tpSpent': skill['tpCost'],
        }
    else :
        result = {
            'source': skill['name'],
            'type': 'skill',
            'timestamp': newState['timeline']['timestamp'],
            'tpSpent': skill['tpCost'],
        }
    if 'removeBuff' in skill :
        newState = removeBuff(newState, skill['removeBuff'])
    if 'addBuff' in skill :
        for bufName in skill['addBuff'] :
            newState = applyBuff(newState, b[bufName])
    if 'addDebuff' in skill :
        for debufName in skill['addDebuff'] :
            newState = applyDebuff(newState, d[debufName])
    if skill['cooldown'] > 0 :
        newState = addAction(newState, skill['cooldown'], { 'type': 'removeCooldown', 'name': skill['name'] })
        newState['player']['cooldown'] = newState['player']['cooldown'] + [ skill['name'] ]
    ss = newState['player']['baseStats']['skillSpeed']
    ssBuf = getBuff(newState, 'speed')
    gcdDuration = gcdTick(ss, ssBuf)
    if skill['gcdType'] == 'global' :
        newState = addAction(newState, gcdDuration / 2, { 'type': 'instantSkill' })
        newState = addAction(newState, gcdDuration, { 'type': 'gcdSkill' })
    newState = nextAction(newState)
    return (newState, result)

def applySingleDot(state, dot) :
    pot = dot['props']['potency']
    wd = dot['snapshot']['player']['baseStats']['weaponDamage']
    st = dot['snapshot']['player']['baseStats']['strength']
    det = dot['snapshot']['player']['baseStats']['determination']
    crt = dot['snapshot']['player']['baseStats']['criticalHitRate']
    ss = dot['snapshot']['player']['baseStats']['skillSpeed']
    dmgBuf = getBuff(dot['snapshot'], 'damage')
    crtBuf = getBuff(dot['snapshot'], 'critChance')
    ssBuf = dotTick(ss)
    baseDmg = baseDamage(pot, wd, st, det, dmgBuf + [ ssBuf ]) 
    basePot = basePotency(pot, dmgBuf + [ ssBuf ])
    crtChc = critChance(crt, crtBuf)
    crtBonF = critBonus(crt)
    crtDmg = baseDmg * (1 + crtChc * crtBonF)
    crtPot = basePot * (1 + crtChc * crtBonF)
    result = {
        'damage': crtDmg,
        'potency': crtPot,
        'source': dot['name'],
        'type': 'DoT',
        'timestamp': state['timeline']['timestamp'],
    }
    newState = nextAction(state)
    return (newState, result)

def applyDot(state) :
    dotList = [ d for d in state['enemy']['debuff'] if d['type'] == 'DoT' ]
    newState = copy.deepcopy(state)
    for d in dotList :
        newState = addAction(newState, 0, { 'type': 'dot', 'name': d['name'] })
    newState = addAction(newState, 3, { 'type': 'dotTick' })
    newState = nextAction(newState)
    return newState

def formatPriorityList(priorityList) :
    return [ addHiddenConditions(pe) for pe in priorityList ]
    
def addHiddenConditions(priorityElement) :
    skill = s[priorityElement['group']][priorityElement['name']]
    newPriorityElement = copy.deepcopy(priorityElement)
    if 'condition' not in newPriorityElement :
        newPriorityElement['condition'] = {
            'type': 'gcdType',
            'comparison': lambda x, y: x == y,
            'value': skill['gcdType']
        }
    else :
        newPriorityElement['condition'] = {
            'logic': lambda x, y: x and y,
            'list': [
                newPriorityElement['condition'],
                {
                    'type': 'gcdType',
                    'comparison': lambda x, y: x == y,
                    'value': skill['gcdType']
                },
            ],
        }
    if 'requiredBuff' in skill :
        reqBufList = []
        for bufName in skill['requiredBuff'] :
            if 'maxStacks' in b[bufName] :
                reqBufList = reqBufList + [ {
                    'type': 'buffAtMaxStacks', 
                    'name': bufName,
                    'comparison': lambda x, y: x == y,
                    'value': True,
                } ]
            else :
                reqBufList = reqBufList + [ {
                    'type': 'buffPresent', 
                    'name': bufName,
                    'comparison': lambda x, y: x == y,
                    'value': True,
                } ]
        newPriorityElement['condition'] = {
            'logic': lambda x, y: x and y,
            'list': [
                newPriorityElement['condition'],
                {
                    'logic': lambda x, y: x or y,
                    'list': reqBufList,
                },
            ],
        }
    if skill['cooldown'] > 0:
        newPriorityElement['condition'] = {
            'logic': lambda x, y: x and y,
            'list': [
                newPriorityElement['condition'],
                {
                    'type': 'cooldownPresent',
                    'name': skill['name'],
                    'comparison': lambda x, y: x == y,
                    'value': False,
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
        return condition['name'] in [ bf[0]['name'] for bf in state['player']['buff'] if 'maxStacks' in b[bf[0]['name']] and bf[1] == b[bf[0]['name']]['maxStacks'] ]
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

def testCondition(state, condition) :
    val = getConditionValue(state, condition)
    return condition['comparison'](val, condition['value'])

def reduceConditions(state, conditions) :
    if 'logic' in conditions:
        return reduce(conditions['logic'], [ reduceConditions(state, cond) for cond in conditions['list'] ])
    return testCondition(state, conditions)

def findBestSkill(state, priorityList) :
    skill = None
    for priorityElement in priorityList :
        if reduceConditions(state, priorityElement['condition']) :
            skill = s[priorityElement['group']][priorityElement['name']]
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
    elif actionType == 'gcdSkill' or actionType == 'instantSkill' :
        bestSkill = findBestSkill(state, priorityList)
        (newState, result) = applySkill(state, bestSkill)
    elif actionType == 'autoAttack' :
        (newState, result) = applyAutoAttack(state)
    return (newState, result)

priorityList = [
    {
        'name': 'internalRelease',
        'group': 'pugilist',
        'condition': {
            'logic': lambda x, y: x and y,
            'list': [
                {
                    'type': 'buffAtMaxStacks',
                    'name': 'greasedLightning',
                    'comparison': lambda x, y: x == y,
                    'value': True,
                },
                {
                    'type': 'cooldownTimeLeft',
                    'name': 'elixirField',
                    'comparison': lambda x, y: x <= y,
                    'value': 5,
                },
            ]
        }
    },
    {
        'name': 'howlingFist',
        'group': 'pugilist',
        'condition': {
            'type': 'buffPresent',
            'name': 'internalRelease',
            'comparison': lambda x, y: x == y,
            'value': True,
        }
    },
    {
        'name': 'elixirField',
        'group': 'monk',
        'condition': {
            'logic': lambda x, y: x or y,
            'list': [
                {
                    'type': 'buffPresent',
                    'name': 'internalRelease',
                    'comparison': lambda x, y: x == y,
                    'value': True,
                },
                {
                    'type': 'cooldownTimeLeft',
                    'name': 'internalRelease',
                    'comparison': lambda x, y: x >= y,
                    'value': 20,
                },
            ],
        }
    },
    {
        'name': 'steelPeak',
        'group': 'pugilist',
    },
    {
        'name': 'touchOfDeath',
        'group': 'pugilist',
        'condition': {
            'logic': lambda x, y: x and y,
            'list': [
                {
                    'type': 'debuffTimeLeft',
                    'name': 'touchOfDeath',
                    'comparison': lambda x, y: x <= y,
                    'value': 1.5,
                },
                {
                    'type': 'debuffPresent',
                    'name': 'dragonKick',
                    'comparison': lambda x, y: x == y,
                    'value': True,
                },
            ]
        }
    },
    {
        'name': 'demolish',
        'group': 'pugilist',
        'condition': {
            'type': 'debuffTimeLeft',
            'name': 'demolish',
            'comparison': lambda x, y: x <= y,
            'value': 4,
        },
    },
    {
        'name': 'twinSnakes',
        'group': 'pugilist',
        'condition': {
            'type': 'buffTimeLeft',
            'name': 'twinSnakes',
            'comparison': lambda x, y: x <= y,
            'value': 5,
        },
    },
    {
        'name': 'snapPunch',
        'group': 'pugilist',
    },
    {
        'name': 'trueStrike',
        'group': 'pugilist',
    },
    {
        'name': 'dragonKick',
        'group': 'monk',
        'condition': {
            'type': 'debuffTimeLeft',
            'name': 'dragonKick',
            'comparison': lambda x, y: x <= y,
            'value': 5,
        },
    },
    {
        'name': 'bootshine',
        'group': 'pugilist',
    },
]

plist = formatPriorityList(priorityList)

states = [state]
results = []
nextState = copy.deepcopy(state)
maxTime = 8 * 60
while nextState['timeline']['timestamp'] <= maxTime:
    (nextState, nextResult) = solveCurrentAction(nextState, plist)
    states = states + [nextState]
    results = results + [nextResult]
sum( r['damage'] for r in results if 'damage' in r ) / maxTime
sum( r['potency'] for r in results if 'potency' in r ) / maxTime
