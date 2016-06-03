# -*- coding: utf-8 -*-
"""
Created on Thu Jun 02 17:04:31 2016

@author: rmondoncancel
"""

import re

def isFloat(value) :
    try :
        float(value)
        return True
    except ValueError :
        return False

def parseValue(value) :
    if value == 'True':
        return True
    elif value == 'False':
        return False
    elif isFloat(value):
        return float(value)
    else:
        return value
        
def closingParentheseIndex(string) :
    if string[0] != '(' :
        return -1
    cnt = 0
    for i in range(len(string)) :
        t = string[i]            
        if t == '(' :
            cnt += 1
        elif t == ')' :
            cnt -= 1
        if cnt == 0 :
            return i
    return -1

def unfoldConditions(cLine, single = True) :
    cLine = cLine.strip()
    if single :
        if cLine[0] == '(' and closingParentheseIndex(cLine) + 1 == len(cLine) :
            (cList, logic) = unfoldConditions(cLine[1:-1], False)
            return { 'logic': logic, 'list': cList }
        else :
            [ condition, operator, value ] = cLine.split(' ')
            [ cType, name ] = condition.split('.')
            return {
                'type': cType,
                'name': name,
                'comparison': operator,
                'value': parseValue(value),
            }
    else :
        if cLine[0] == '(' :
            cFirst = unfoldConditions(cLine[:closingParentheseIndex(cLine)+1], True)
            cRest = cLine[closingParentheseIndex(cLine)+1:].strip()
            if cRest.find(' ') == -1:
                return ([cFirst], 'and')
            operator = cRest.split(' ')[0]
            cRest = cRest[len(operator):].strip()
            (cRestList, cRestLogic) = unfoldConditions(cRest, False)
            return ([cFirst] + cRestList, operator)
        else :
            condition = cLine[:cLine.find(' ')]
            cLine = cLine[cLine.find(' '):].strip()
            [ cType, name ] = condition.split('.')
            operator = cLine[:cLine.find(' ')]
            cLine = cLine[cLine.find(' '):].strip()
            if cLine.find(' ') == -1 :
                value = cLine
                cLine = ''
            else :
                value = cLine[:cLine.find(' ')]
                cLine = cLine[cLine.find(' '):].strip()
            pCond = {
                'type': cType,
                'name': name,
                'comparison': operator,
                'value': parseValue(value),
            }
            if cLine.find(' ') == -1:
                return ([pCond], 'and')
            operator = cLine.split(' ')[0]
            cLine = cLine[len(operator):].strip()
            (cRestList, cRestLogic) = unfoldConditions(cLine, False)
            return ([pCond] + cRestList, operator)

def priorityParser(plFile, absolute = False) :
    if not absolute:    
        plFile = 'priorityLists/' + plFile
        if plFile[-6:] != '.plist':
            plFile = plFile + '.plist'
    with open(plFile, 'r') as f:
        pLines = [ re.sub(' +', ' ', l.rstrip('\n').strip()) for l in f.readlines() if l != '\n' and l[0] != '#' ]
    pList = []
    for pLine in pLines :
        pElement = {}
        if pLine[:7] == 'prepull':
            pElement['prepull'] = True
            pLine = pLine[8:]
        skill = pLine.split(' ')[0]
        pElement['group'] = skill.split('.')[0]
        pElement['name'] = skill.split('.')[1]
        pLine = pLine[len(skill):]
        if len(pLine) > 3 and pLine[1:3] == 'if':
            pLine = pLine[4:]
            pElement['condition'] = unfoldConditions(pLine)
        pList = pList + [pElement]
    return pList