# -*- coding: utf-8 -*-
"""
Created on Tue May 31 16:57:03 2016

@author: rmondoncancel
"""

from stateManagement import \
    getBuff, applyBuff, removeBuff, applyDebuff, getResistance, addAction, \
    nextAction
from dpsCalculation import \
    baseDamage, basePotency, critChance, critBonus, gcdTick, dotTick
from priorityManagement import actionToGcdType
from buffs import b
from debuffs import d
import copy
TIME_EPSILON = 0.000000001

def applyAutoAttack(state) :
    newState = copy.deepcopy(state)
    if any(state['timeline']['prepull'].values()) :
        autoAttackDelay = newState['player']['baseStats']['weaponDelay']
        newState = addAction(newState, autoAttackDelay, { 'type': 'autoAttack' })
        return(nextAction(newState), {})
    pot = 100 * newState['player']['baseStats']['weaponDelay'] / 3
    wd = newState['player']['baseStats']['weaponDamage']
    st = newState['player']['baseStats']['strength']
    det = newState['player']['baseStats']['determination']
    crt = newState['player']['baseStats']['criticalHitRate']
    dmgBuf = getBuff(newState, 'damage')
    crtBuf = getBuff(newState, 'critChance')
    stBuff = getBuff(newState, 'strength')
    buffedSt = reduce(lambda x, y: min(x * (1 + y[0]), x + y[1]), stBuff, st)
    baseDmg = baseDamage(pot, wd, buffedSt, det, dmgBuf) 
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
    newState = copy.deepcopy(state)
    if skill == None:
        if any(newState['timeline']['prepull'].values()) :
            newState['timeline']['prepull'][actionToGcdType(newState['timeline']['currentAction']['type'])] = False
        if newState['timeline']['currentAction']['type'] == 'gcdSkill':
            newState = addAction(newState, 0, { 'type': 'instantSkill' })
            newState = addAction(newState, TIME_EPSILON, { 'type': 'gcdSkill' })
        newState = nextAction(newState)
        return (newState, {})
    newState = specialAction(newState, skill)
    if 'skillBuff' in skill :
        for bufName in skill['skillBuff'] :
            newState = applyBuff(newState, b()[bufName])
    if 'potency' in skill and not any(newState['timeline']['prepull'].values()) :
        pot = skill['potency']
        wd = newState['player']['baseStats']['weaponDamage']
        st = newState['player']['baseStats']['strength']
        det = newState['player']['baseStats']['determination']
        crt = newState['player']['baseStats']['criticalHitRate']
        dmgBuf = getBuff(newState, 'damage')
        crtBuf = getBuff(newState, 'critChance')
        stBuff = getBuff(newState, 'strength')
        buffedSt = reduce(lambda x, y: min(x * (1 + y[0]), x + y[1]), stBuff, st)
        baseDmg = baseDamage(pot, wd, buffedSt, det, dmgBuf) 
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
            newState = applyBuff(newState, b()[bufName])
    if 'addDebuff' in skill :
        for debufName in skill['addDebuff'] :
            newState = applyDebuff(newState, d()[debufName])
    if skill['cooldown'] > 0 :
        newState = addAction(newState, skill['cooldown'], { 'type': 'removeCooldown', 'name': skill['name'] })
        newState['player']['cooldown'] = newState['player']['cooldown'] + [ skill['name'] ]
    ss = newState['player']['baseStats']['skillSpeed']
    ssBuf = getBuff(newState, 'speed')
    gcdDuration = gcdTick(ss, ssBuf)
    if any(newState['timeline']['prepull'].values()) :
        newState['timeline']['prepull']['global'] = True
        newState['timeline']['prepull']['instant'] = True
        newState['timeline']['prepullTimestamp'][skill['gcdType']] = newState['timeline']['timestamp'] + skill['animationLock']
    if skill['gcdType'] == 'global' :
        newState = addAction(newState, skill['animationLock'], { 'type': 'instantSkill' })
        newState = addAction(newState, gcdDuration * (skill['gcdModifier'] if 'gcdModifier' in skill else 1), { 'type': 'gcdSkill' })
    if skill['gcdType'] == 'instant' :
        newState = addAction(newState, skill['animationLock'], { 'type': 'instantSkill' })
        nextGcdTimestamp = min( na[0] for na in newState['timeline']['nextActions'] if na[1]['type'] == 'gcdSkill' )
        if nextGcdTimestamp < newState['timeline']['timestamp'] + skill['animationLock']:
            newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1]['type'] != 'gcdSkill' ]
            newState = addAction(newState, skill['animationLock'] + TIME_EPSILON, { 'type': 'gcdSkill' })
    newState = nextAction(newState)
    return (newState, result)
    
def specialAction(state, skill) :
    newState = copy.deepcopy(state)
    if 'special' not in skill :
        return newState
    if skill['special'] == 'removeForms' :
        newState = addAction(newState, b()[skill['addBuff'][0]]['duration'], { 'type': 'special', 'name': skill['special'] })
    elif skill['special'] == 'nextForm' :
        forms = [ 'opoOpoForm', 'raptorForm', 'coerlForm' ]
        if forms[0] in [ pb[0]['name'] for pb in newState['player']['buff'] ] :
            newState = removeBuff(newState, forms)
            newState = applyBuff(newState, b()[forms[1]])
        elif forms[1] in [ pb[0]['name'] for pb in newState['player']['buff'] ] :
            newState = removeBuff(newState, forms)
            newState = applyBuff(newState, b()[forms[2]])
        elif forms[2] in [ pb[0]['name'] for pb in newState['player']['buff'] ] :
            newState = removeBuff(newState, forms)
            newState = applyBuff(newState, b()[forms[0]])
        else :
            newState = applyBuff(newState, b()[forms[0]])
    elif skill['special'] == 'bootshineCrit' :
        if 'opoOpoForm' in [ pb[0]['name'] for pb in newState['player']['buff'] ] or 'perfectBalance' in [ pb[0]['name'] for pb in newState['player']['buff'] ] :
            newState = applyBuff(newState, b()[skill['special']])
    elif skill['special'] == 'dragonKick' :
        if 'opoOpoForm' in [ pb[0]['name'] for pb in newState['player']['buff'] ] or 'perfectBalance' in [ pb[0]['name'] for pb in newState['player']['buff'] ] :
            newState = addAction(newState, 0, { 'type': 'special', 'name': skill['special'] })
    return newState

def applySpecialAction(state, name) :
    newState = copy.deepcopy(state)
    if name == 'removeForms' :
        forms = [ 'opoOpoForm', 'raptorForm', 'coerlForm' ]
        newState = removeBuff(newState, forms)
    elif name == 'dragonKick' :
        newState = applyDebuff(newState, d()[name])
    newState = nextAction(newState)
    return (newState, {})

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
    stBuff = getBuff(dot['snapshot'], 'strength')
    buffedSt = reduce(lambda x, y: min(x * (1 + y[0]), x + y[1]), stBuff, st)
    baseDmg = baseDamage(pot, wd, buffedSt, det, dmgBuf + [ ssBuf ]) 
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