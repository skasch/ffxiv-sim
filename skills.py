# -*- coding: utf-8 -*-
"""
Created on Tue May 31 16:23:07 2016

@author: rmondoncancel
"""

from skillManagement import prepareGroup

def s(pClass):
    """Returns the list of skills
    name: name of the buff
    level: level necessary to unlock the skill
    tpCost: TP cost of the skill
    gcdType: global or instant, if the skill is on GCD or not
    cooldown: cooldown duration for the skill
    castTime: cast time of the skill; not implemented yet
    animationLock: animation lock of the skill, duration when using another 
        skill is impossible
    [range]: skill range of the skill; useless so far
    [radius]: radius of the skill; useless so far
    [potency]: base potency of the skill
    [type]: type of the attack [blunt/slashing/piercing]
    [gcdModifier]: ratio of next GCD duration; for example, Meditation halves
        the next GCD duration
    [requiedBuff]: array of buffs requied to use the skill; at least one should
        be present and at max stacks if the buff has stacks
    [removeBuff]: array of buffs removed when the skill is used
    [addBuff]: array of buffs added when the skill is used; when the buff has
        stacks, adds one stack
    [addDebuff]: array of debuffs added when the skill is used
    [special]: special action to be resolved when the skill is used
    [condition]: special condition to be added to the hidden conditions of the
        skill
    """
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
        'animationLock': 0.75,
        'type': 'blunt',
        'removeBuff': ['opoOpoForm'],
        'addBuff': ['raptorForm'],
        'special': 'bootshineCrit',
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
        'animationLock': 0.75,
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
        'animationLock': 0.75,
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
        'animationLock': 0.75,
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
        'animationLock': 0.75,
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
        'animationLock': 0.75,
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
        'animationLock': 0.75,
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
        'cooldown': 60,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 150,
        'animationLock': 0.75,
        'type': 'blunt',
        'traitBonus': {
            'class': 'pugilist', 
            'level': 44, 
            'bonus': {
                'cooldown': 40,
            }
        }
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
        'animationLock': 0.75,
        'type': 'blunt',
    }
    s['pugilist']['perfectBalance'] = {
        'name': 'perfectBalance',
        'level': 46,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 240,
        'castTime': 0,
        'animationLock': 0.75,
        'addBuff': ['perfectBalance'],
        'special': 'removeForms',
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
        'animationLock': 0.75,
        'type': 'blunt',
    }
    s['monk']['fistOfFire'] = {
        'name': 'fistOfFire',
        'level': 40,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 3,
        'castTime': 0,
        'animationLock': 0.75,
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
        'animationLock': 0.75,
        'type': 'blunt',
        'removeBuff': ['opoOpoForm'],
        'addBuff': ['raptorForm'],
        'special': 'dragonKick',
    }
    s['monk']['formShift'] = {
        'name': 'formShift',
        'level': 52,
        'tpCost': 0,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'animationLock': 0.75,
        'special': 'nextForm'
    }
    s['monk']['meditation'] = {
        'name': 'meditation',
        'level': 54,
        'tpCost': 0,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'animationLock': 0.75,
        'gcdModifier': 0.5,
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
        'animationLock': 0.75,
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
        'animationLock': 0.75,
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
        'animationLock': 0.75,
        'type': 'blunt',
        'requiredBuff': ['greasedLightning'],
        'removeBuff': ['greasedLightning'],
    }
    
    # Lancer
    s['lancer'] = {}
    s['lancer']['trueThrust'] = {
        'name': 'trueThrust',
        'level': 1,
        'tpCost': 70,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 150,
        'animationLock': 0.75,
        'type': 'piercing',
    }
    s['lancer']['vorpalThrust'] = {
        'name': 'vorpalThrust',
        'level': 4,
        'tpCost': 60,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 100,
        'animationLock': 0.75,
        'type': 'piercing',
        'combo': ('trueThrust', {
            'potency': 200,
        }),
    }
    s['lancer']['impulseDrive'] = {
        'name': 'impulseDrive',
        'level': 8,
        'tpCost': 70,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 180,
        'animationLock': 0.75,
        'type': 'piercing',
    }
    s['lancer']['legSweep'] = {
        'name': 'legSweep',
        'level': 10,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 30,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 130,
        'animationLock': 0.75,
        'type': 'piercing',
        'traitBonus': {
            'class': 'lancer', 
            'level': 28, 
            'bonus': {
                'cooldown': 20,
            }
        }
    }
    s['lancer']['heavyThrust'] = {
        'name': 'heavyThrust',
        'level': 12,
        'tpCost': 70,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 170,
        'animationLock': 0.75,
        'type': 'piercing',
        'addBuff': ['heavyThrust'],
    }
    s['lancer']['piercingTalon'] = {
        'name': 'piercingTalon',
        'level': 15,
        'tpCost': 130,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 15,
        'radius': 0,
        'potency': 120,
        'animationLock': 0.75,
        'type': 'piercing',
    }
    s['lancer']['lifeSurge'] = {
        'name': 'lifeSurge',
        'level': 18,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 90,
        'castTime': 0,
        'animationLock': 0.75,
        'addBuff': ['lifeSurge'],
        'traitBonus': {
            'class': 'lancer', 
            'level': 32, 
            'bonus': {
                'cooldown': 50,
            }
        }
    }
    s['lancer']['fullThrust'] = {
        'name': 'fullThrust',
        'level': 26,
        'tpCost': 60,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 100,
        'animationLock': 0.75,
        'type': 'piercing',
        'combo': ('vorpalThrust', {
            'potency': 360,
            'special': 'procBloodOfTheDragon',
        }),
    }
    s['lancer']['phlebotomize'] = {
        'name': 'phlebotomize',
        'level': 30,
        'tpCost': 90,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 170,
        'animationLock': 0.75,
        'type': 'piercing',
        'addDebuff': ['phlebotomize'],
    }
    s['lancer']['bloodForBlood'] = {
        'name': 'bloodForBlood',
        'level': 34,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 80,
        'castTime': 0,
        'animationLock': 0.75,
        'addBuff': ['bloodForBlood'],
    }
    s['lancer']['disembowel'] = {
        'name': 'disembowel',
        'level': 38,
        'tpCost': 60,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 100,
        'animationLock': 0.75,
        'type': 'piercing',
        'combo': ('impulseDrive', {
            'potency': 220,
            'addDebuff': ['disembowel'],
        }),
    }
    s['lancer']['doomSpike'] = {
        'name': 'doomSpike',
        'level': 42,
        'tpCost': 160,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 10,
        'radius': 10,
        'potency': 160,
        'animationLock': 0.75,
        'type': 'piercing',
    }
    s['lancer']['ringOfThorns'] = {
        'name': 'ringOfThorns',
        'level': 46,
        'tpCost': 120,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 0,
        'radius': 5,
        'potency': 100,
        'animationLock': 0.75,
        'type': 'piercing',
        'combo': ('heavyThrust', {
            'potency': 150,
        }),
    }
    s['lancer']['chaosThrust'] = {
        'name': 'chaosThrust',
        'level': 50,
        'tpCost': 60,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 100,
        'animationLock': 0.75,
        'type': 'piercing',
        'combo': ('disembowel', {
            'potency': 250,
            'addDebuff': ['chaosThrust'],
            'special': 'procBloodOfTheDragon',
        }),
    }
    
    #Dragoon
    s['dragoon'] = {}
    s['dragoon']['jump'] = {
        'name': 'jump',
        'level': 30,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 30,
        'castTime': 0,
        'range': 20,
        'radius': 0,
        'potency': 200,
        'animationLock': 0.75,
        'type': 'piercing',
        'removeBuff': ['powerSurge'],
        'special': 'surgeBonus',
    }
    s['dragoon']['spineshatterDrive'] = {
        'name': 'spineshatterDrive',
        'level': 40,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 60,
        'castTime': 0,
        'range': 20,
        'radius': 0,
        'potency': 170,
        'animationLock': 0.75,
        'type': 'piercing',
        'removeBuff': ['powerSurge'],
        'special': 'surgeBonus',
    }
    s['dragoon']['powerSurge'] = {
        'name': 'powerSurge',
        'level': 45,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 60,
        'castTime': 0,
        'animationLock': 0.75,
        'addBuff': ['powerSurge'],
    }
    s['dragoon']['dragonfireDive'] = {
        'name': 'dragonfireDive',
        'level': 50,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 120,
        'castTime': 0,
        'range': 20,
        'radius': 5,
        'potency': 250,
        'animationLock': 0.75,
        'type': 'piercing',
    }
    s['dragoon']['battleLitany'] = {
        'name': 'battleLitany',
        'level': 52,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 180,
        'castTime': 0,
        'range': 0,
        'radius': 15,
        'animationLock': 0.75,
        'addBuff': ['battleLitany'],
    }
    s['dragoon']['bloodOfTheDragon'] = {
        'name': 'bloodOfTheDragon',
        'level': 54,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 60,
        'castTime': 0,
        'animationLock': 0.75,
        'addBuff': ['bloodOfTheDragon'],
        'removeBuff': ['sharperFangAndClaw', 'enhancedWheelingThrust'],
    }
    s['dragoon']['fangAndClaw'] = {
        'name': 'fangAndClaw',
        'level': 56,
        'tpCost': 60,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 290,
        'animationLock': 0.75,
        'type': 'piercing',
        'requiredBuff': ['sharperFangAndClaw'],
        'special': 'extendBloodOfTheDragon',
    }
    s['dragoon']['wheelingThrust'] = {
        'name': 'wheelingThrust',
        'level': 58,
        'tpCost': 60,
        'gcdType': 'global',
        'cooldown': 0,
        'castTime': 0,
        'range': 3,
        'radius': 0,
        'potency': 290,
        'animationLock': 0.75,
        'type': 'piercing',
        'requiredBuff': ['enhancedWheelingThrust'],
        'special': 'extendBloodOfTheDragon',
    }
    s['dragoon']['geirskogul'] = {
        'name': 'geirskogul',
        'level': 60,
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 10,
        'castTime': 0,
        'range': 15,
        'radius': 15,
        'potency': 200,
        'animationLock': 0.75,
        'requiredBuff': ['bloodOfTheDragon'],
        'special': 'reduceBloodOfTheDragon',
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
        'animationLock': 0.75,
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
        'animationLock': 0.75,
        'type': 'slashing',
        'condition': {
            'comparison': '<=',
            'type': 'state',
            'name': 'enemyLifePercent',
            'value': 20,
        }
    }
    
    # Items
    s['item'] = {}
    s['item']['potionOfStrength'] = {
        'name': 'potionOfStrength',
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 300,
        'castTime': 0,
        'animationLock': 0.75,
        'addBuff': ['potionOfStrength'],
    }
    s['item']['potionOfStrengthHQ'] = {
        'name': 'potionOfStrengthHQ',
        'tpCost': 0,
        'gcdType': 'instant',
        'cooldown': 300,
        'castTime': 0,
        'animationLock': 0.75,
        'addBuff': ['potionOfStrengthHQ'],
    }
    return prepareGroup(s, pClass, skill = True)