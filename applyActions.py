# -*- coding: utf-8 -*-
"""
Created on Tue May 31 16:57:03 2016

@author: rmondoncancel
"""

from stateManagement import \
    getBuff, applyBuff, removeBuff, applyDebuff, getResistance, addAction, \
    nextAction, applyDamage, applyTpChange
from dpsCalculation import \
    baseDamage, basePotency, critChance, critBonus, gcdTick, dotTick, \
    strBonus, buffedPotency
from priorityManagement import actionToGcdType
from buffs import b
from debuffs import d
import random

import copy
TIME_EPSILON = 0.000000001

def comboBonus(state, skill) :
    newSkill = copy.deepcopy(skill)
    if 'combo' in newSkill and state['timeline']['lastGCD'] == newSkill['combo'][0] :
        for bonus in newSkill['combo'][1] :
            newSkill[bonus] = newSkill['combo'][1][bonus]
    return newSkill

def specialAction(state, skill) :
    """Modify the state if the skill has a 'special' property
    The special property contains a key, and this function modifies the state
    according to what is supposed to happen when this specific key is found.
    """
    newState = copy.deepcopy(state)
    # Returns the state is no special property is present
    if 'special' not in skill :
        return newState
    # MNK
    # Add an action to remove all forms at the end of perfectBalance
    if skill['special'] == 'removeForms' :
        newState = addAction(newState, b(state['player']['class'])[skill['addBuff'][0]]['duration'], { 'type': 'special', 'name': skill['special'] })
    # Switch to next form when using formShift
    elif skill['special'] == 'nextForm' :
        forms = [ 'opoOpoForm', 'raptorForm', 'coerlForm' ]
        if forms[0] in [ pb[0]['name'] for pb in newState['player']['buff'] ] :
            newState = removeBuff(newState, forms)
            newState = applyBuff(newState, b(state['player']['class'])[forms[1]])
        elif forms[1] in [ pb[0]['name'] for pb in newState['player']['buff'] ] :
            newState = removeBuff(newState, forms)
            newState = applyBuff(newState, b(state['player']['class'])[forms[2]])
        elif forms[2] in [ pb[0]['name'] for pb in newState['player']['buff'] ] :
            newState = removeBuff(newState, forms)
            newState = applyBuff(newState, b(state['player']['class'])[forms[0]])
        else :
            newState = applyBuff(newState, b(state['player']['class'])[forms[0]])
    # Add skill buff for bootshine to have 100% crit chance if in opoOpoForm
    elif skill['special'] == 'bootshineCrit' :
        if 'opoOpoForm' in [ pb[0]['name'] for pb in newState['player']['buff'] ] or 'perfectBalance' in [ pb[0]['name'] for pb in newState['player']['buff'] ] :
            newState = applyBuff(newState, b(state['player']['class'])[skill['special']])
    # Apply dragonKick debuff at the end of the skill if in opoOpoForm
    elif skill['special'] == 'dragonKick' :
        if 'opoOpoForm' in [ pb[0]['name'] for pb in newState['player']['buff'] ] or 'perfectBalance' in [ pb[0]['name'] for pb in newState['player']['buff'] ] :
            newState = addAction(newState, 0, { 'type': 'special', 'name': skill['special'] })
    # DGN
    elif skill['special'] == 'procBloodOfTheDragon' :
        if 'bloodOfTheDragon' in [ pb[0]['name'] for pb in newState['player']['buff'] ] :
            if random.random() < 0.5 :
                newState = addAction(newState, 0, { 'type': 'special', 'name': 'sharperFangAndClaw' })
            else :
                newState = addAction(newState, 0, { 'type': 'special', 'name': 'enhancedWheelingThrust' })
    elif skill['special'] == 'surgeBonus' :
        if 'powerSurge' in [ pb[0]['name'] for pb in newState['player']['buff'] ] :
            newState = applyBuff(newState, b(state['player']['class'])['surgeBonus'])
    elif skill['special'] == 'extendBloodOfTheDragon' :
        if 'bloodOfTheDragon' in [ pb[0]['name'] for pb in newState['player']['buff'] ] :
            currentTimestamp = min( na[0] for na in newState['timeline']['nextActions'] if na[1] == { 'name': 'bloodOfTheDragon', 'type': 'removeBuff' } )
            newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1] != { 'name': 'bloodOfTheDragon', 'type': 'removeBuff' } ]
            newState = addAction(newState, min(30, currentTimestamp + 15), { 'name': 'bloodOfTheDragon', 'type': 'removeBuff' })
    elif skill['special'] == 'reduceBloodOfTheDragon' :
        if 'bloodOfTheDragon' in [ pb[0]['name'] for pb in newState['player']['buff'] ] :
            currentTimestamp = min( na[0] for na in newState['timeline']['nextActions'] if na[1] == { 'name': 'bloodOfTheDragon', 'type': 'removeBuff' } )
            newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1] != { 'name': 'bloodOfTheDragon', 'type': 'removeBuff' } ]
            newState = addAction(newState, max(0, currentTimestamp - 10), { 'name': 'bloodOfTheDragon', 'type': 'removeBuff' })
    return newState

def applySpecialAction(state, name) :
    """Resolve special actions created by special mechanics in the 
    specialAction function if the said mechanic require an application delay
    """
    newState = copy.deepcopy(state)
    # MNK
    # Remove all forms at the end on perfectBalance
    if name == 'removeForms' :
        forms = [ 'opoOpoForm', 'raptorForm', 'coerlForm' ]
        newState = removeBuff(newState, forms)
    # Apply dragonKick debuff right after dragonKick is cast
    elif name == 'dragonKick' :
        newState = applyDebuff(newState, d(state['player']['class'])[name])
    # DRG
    elif name == 'sharperFangAndClaw' :
        newState = applyBuff(newState, b(state['player']['class'])[name])
    elif name == 'enhancedWheelingThrust' :
        newState = applyBuff(newState, b(state['player']['class'])[name])
    newState = nextAction(newState)
    return (newState, {})
    
def computeDamage(state, src, value = None) :
    """Calculates the damage for a given source src
    From a certain state, gives the damage output of an auto-attack, a direct
    skill or a DoT tick.
    src value is either 'autoAttack', 'skill' or 'DoT'.
    value is the applied skill or DoT if applicable.
    """
    if src == 'autoAttack' :
        pot = 100 * state['player']['baseStats']['weaponDelay'] / 3
        dtype = state['player']['baseStats']['weaponType']
    elif src == 'skill' :
        pot = value['potency']
        dtype = state['player']['baseStats']['weaponType']
    elif src == 'DoT':
        pot = value['potency']
        dtype = 'DoT'
    wd = state['player']['baseStats']['weaponDamage']
    st = state['player']['baseStats']['strength']
    det = state['player']['baseStats']['determination']
    crt = state['player']['baseStats']['criticalHitRate']
    # Get buffs
    potBuf = getBuff(state, 'potency')
    dmgBuf = getBuff(state, 'damage')
    crtBuf = getBuff(state, 'critChance')
    stBuff = getBuff(state, 'strength')
    buffedSt = strBonus(stBuff, st)
    pot = buffedPotency(pot, potBuf)
    # Base damage and crit
    if src == 'DoT' :
        # Add skill speed bonus to damage if DoT
        ss = state['player']['baseStats']['skillSpeed']
        ssBuf = dotTick(ss)
        baseDmg = baseDamage(pot, wd, buffedSt, det, dmgBuf + [ ssBuf ]) 
        basePot = basePotency(pot, dmgBuf + [ ssBuf ])
    else :
        baseDmg = baseDamage(pot, wd, buffedSt, det, dmgBuf) 
        basePot = basePotency(pot, dmgBuf)
    crtChc = critChance(crt, crtBuf)
    crtBonF = critBonus(crt)
    # Average damage with crit
    crtDmg = baseDmg * (1 + crtChc * crtBonF)
    crtPot = basePot * (1 + crtChc * crtBonF)
    # Apply resistance
    if dtype == 'DoT':
        dmgRes = 1
    else :
        dmgRes = getResistance(state, dtype)
    effDmg = crtDmg * dmgRes
    effPot = crtPot * dmgRes
    # Calculates hit and crit damages
    hitDmg = baseDmg * dmgRes
    critDmg = baseDmg * (1 + crtBonF) * dmgRes
    hitPot = basePot * dmgRes
    critPot = basePot * (1 + crtBonF) * dmgRes
    return (effDmg, effPot, hitDmg, hitPot, critDmg, critPot, crtChc, crtBonF)

def applyAutoAttack(state) :
    """Apply auto attack to a state.
    This function takes a given state that should have an autoAttack current
    action and calculates damage output of the attack.
    Then the function creates the next autoAttack action and returns the couple
    (newState, result) with newState the state at the following action.
    """
    newState = copy.deepcopy(state)
    # Prevents auto-attack from happening if on prepull
    if any(state['timeline']['prepull'].values()) :
        autoAttackDelay = newState['player']['baseStats']['weaponDelay']
        newState = addAction(newState, autoAttackDelay, { 'type': 'autoAttack' })
        return(nextAction(newState), {})
    # Computes auto-attack damage
    (effDmg, effPot, hitDmg, hitPot, critDmg, critPot, crtChc, crtBonF) = computeDamage(newState, 'autoAttack')
    result = {
        'damage': effDmg,
        'potency': effPot, 
        'hitDamage': hitDmg,
        'critDamage': critDmg,
        'hitPotency': hitPot,
        'critPotency': critPot,
        'critChance': crtChc,
        'critBonus': crtBonF,
        'type': 'autoAttack',
        'timestamp': newState['timeline']['timestamp'],
    }
    # Reduce HP of target
    newState = applyDamage(newState, effDmg)
    # Add next auto-attck
    autoAttackDelay = newState['player']['baseStats']['weaponDelay']
    newState = addAction(newState, autoAttackDelay, { 'type': 'autoAttack' })
    newState = nextAction(newState)
    return (newState, result)

def applySkill(state, skill) :
    """Apply instant or gcd skill to a state.
    This function takes a given state that should have a gcdSkill or 
    instantSkill current action and calculates the new state after the skill
    is casted.
    Then the function creates the next skill actions and returns the couple
    (newState, result) with newState the state at the following action.
    """
    newState = copy.deepcopy(state)
    # Solve the state if the priority list does not return any possible skill
    # for the current state
    if skill == None:
        # If still in prepull, add to the state that the prepull does not 
        # require any addition gcd/instant skill at the current state
        if any(newState['timeline']['prepull'].values()) :
            newState['timeline']['prepull'][actionToGcdType(newState['timeline']['currentAction']['type'])] = False
            # If instant is still to try for prepull but a GCD has jsut been used,
            # Add an instant to try just after
            if newState['timeline']['prepull']['instant'] and newState['timeline']['currentAction']['type'] == 'gcdSkill':
                newState = addAction(newState, 0, { 'type': 'instantSkill' })
                newState = addAction(newState, TIME_EPSILON, { 'type': 'gcdSkill' })
            # If at the end of the prepull, add a new gcdSkill to start the 
            # rotation
            if not any(newState['timeline']['prepull'].values()) and newState['timeline']['currentAction']['type'] == 'gcdSkill':
                newState = addAction(newState, 0, { 'type': 'gcdSkill' })
        elif newState['timeline']['currentAction']['type'] == 'gcdSkill' :
            nextTpTick = min( na[0] for na in newState['timeline']['nextActions'] if na[1]['type'] == 'tpTick' ) - state['timeline']['timestamp']
            newState = addAction(newState, 0, { 'type': 'instantSkill' })
            newState = addAction(newState, nextTpTick + TIME_EPSILON, { 'type': 'gcdSkill' })
        newState = nextAction(newState)
        return (newState, {})
    # Apply combo bonus if applicable
    skill = comboBonus(newState, skill)
    # Resolve special action of the current skill if applicable
    newState = specialAction(newState, skill)
    
    newState = applyTpChange(newState, - skill['tpCost'])
    # Get result if skill is a damaging skill and we are not in prepull
    if 'potency' in skill and not any(newState['timeline']['prepull'].values()) :
        (effDmg, effPot, hitDmg, hitPot, critDmg, critPot, crtChc, crtBonF) = computeDamage(newState, 'skill', skill)
        result = {
            'damage': effDmg,
            'potency': effPot, 
            'hitDamage': hitDmg,
            'critDamage': critDmg,
            'hitPotency': hitPot,
            'critPotency': critPot,
            'critChance': crtChc,
            'critBonus': crtBonF,
            'source': skill['name'],
            'type': 'skill',
            'timestamp': newState['timeline']['timestamp'],
            'tpSpent': skill['tpCost'],
        }
        # Reduce HP of target
        newState = applyDamage(newState, effDmg)
    # Get result if skill is not a damaging skill
    else :
        result = {
            'source': skill['name'],
            'type': 'skill',
            'timestamp': newState['timeline']['timestamp'],
            'tpSpent': skill['tpCost'],
        }
    # Apply buff/debuff modifications for the current skill
    if 'removeBuff' in skill :
        newState = removeBuff(newState, skill['removeBuff'])
    if 'addBuff' in skill :
        for bufName in skill['addBuff'] :
            newState = applyBuff(newState, b(state['player']['class'])[bufName])
    if 'addDebuff' in skill :
        for debufName in skill['addDebuff'] :
            newState = applyDebuff(newState, d(state['player']['class'])[debufName])
    # Set the current skill on cooldown if applicable
    if skill['cooldown'] > 0 :
        newState = addAction(newState, skill['cooldown'], { 'type': 'removeCooldown', 'name': skill['name'] })
        newState['player']['cooldown'] = newState['player']['cooldown'] + [ skill['name'] ]
    # Get gcd duration for next GCD
    ss = newState['player']['baseStats']['skillSpeed']
    ssBuf = getBuff(newState, 'speed')
    gcdDuration = gcdTick(ss, ssBuf)
    # Continue prepull if on prepull and a valid skill is found
    if any(newState['timeline']['prepull'].values()) :
        newState['timeline']['prepull']['global'] = True
        newState['timeline']['prepull']['instant'] = True
        newState['timeline']['prepullTimestamp'][skill['gcdType']] = newState['timeline']['timestamp'] + skill['animationLock']
    # Add an instant skill and a GCD skill if current skill is a GCD skill
    if skill['gcdType'] == 'global' :
        # Saves last GCD skill for combos
        newState['timeline']['lastGCD'] = skill['name']
        # Remove next gcdSkills and instantSkills to avoid overlaps
        newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1]['type'] != 'gcdSkill' and na[1]['type'] != 'instantSkill' ]
        newState = addAction(newState, skill['animationLock'], { 'type': 'instantSkill' })
        newState = addAction(newState, gcdDuration * (skill['gcdModifier'] if 'gcdModifier' in skill else 1), { 'type': 'gcdSkill' })
    # Add following actions if skill is an instant skill
    if skill['gcdType'] == 'instant' :
        # Remove next instantSkills to avoid overlaps
        newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1]['type'] != 'instantSkill' ]
        newState = addAction(newState, skill['animationLock'], { 'type': 'instantSkill' })
        # Delay next GCD skill if animation lock pushes it
        nextGcdTimestamp = min( na[0] for na in newState['timeline']['nextActions'] if na[1]['type'] == 'gcdSkill' )
        if nextGcdTimestamp < newState['timeline']['timestamp'] + skill['animationLock']:
            newState['timeline']['nextActions'] = [ na for na in newState['timeline']['nextActions'] if na[1]['type'] != 'gcdSkill' ]
            newState = addAction(newState, skill['animationLock'] + TIME_EPSILON, { 'type': 'gcdSkill' })
    newState = nextAction(newState)
    return (newState, result)

def applySingleDot(state, dot) :
    """Calculates the damage output of a single DoT
    Returns the couple (newState, result) with newState the state at the 
    following action.
    """
    # Calaculates the damage of the current DoT
    (effDmg, effPot, hitDmg, hitPot, critDmg, critPot, crtChc, crtBonF) = computeDamage(dot['snapshot'], 'DoT', dot['props'])
    result = {
        'damage': effDmg,
        'potency': effPot,
        'hitDamage': hitDmg,
        'critDamage': critDmg,
        'hitPotency': hitPot,
        'critPotency': critPot,
        'critChance': crtChc,
        'critBonus': crtBonF,
        'source': dot['name'],
        'type': 'DoT',
        'timestamp': state['timeline']['timestamp'],
    }
    # Reduce HP of target
    newState = applyDamage(state, effDmg)
    newState = nextAction(newState)
    return (newState, result)

def applyDot(state) :
    """Create actions for each DoT applied to the target
    Add a dot action for each currently applied DoT to the target when the
    global DoT tick happens
    Then creates the next global DoT tick and returns the couple 
    (newState, result) with newState the state at the following action.
    """
    # List of currently applied DoTs
    dotList = [ d for d in state['enemy']['debuff'] if d['type'] == 'DoT' ]
    newState = copy.deepcopy(state)
    # Add an action for each applied DoT
    for d in dotList :
        newState = addAction(newState, 0, { 'type': 'dot', 'name': d['name'] })
    # Add following global DoT tick
    newState = addAction(newState, 3, { 'type': 'dotTick' })
    newState = nextAction(newState)
    return newState