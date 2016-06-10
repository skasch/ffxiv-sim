# -*- coding: utf-8 -*-
"""
Created on Thu Jun 02 17:04:31 2016

@author: rmondoncancel
"""

import re

def isFloat(value) :
    """Returns True if value can be converted to a float, else return False
    """
    try :
        float(value)
        return True
    except ValueError :
        return False
    except TypeError :
        return False

def parseValue(value) :
    """Convert values in priority list files to matching value if relevant 
    (boolean or float)
    """
    if value == 'True':
        return True
    elif value == 'False':
        return False
    elif isFloat(value):
        return float(value)
    else:
        return value
        
def closingParentheseIndex(string) :
    """Returns the index of the closing parenthese matching the opening 
    parenthese found at the first character; if first character is not an
    opening parenthese, returns -1
    """
    if string[0] != '(' :
        return -1
    # cnt is the number of open parentheses at current index
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
    """Transform a condition written as a string in a priority file to the
    condition object that should be written in the priority list
    Returns a dictionary that should be written in the 'condition' key of a
    priority element
    single tells if the condition is a simple condition or a complex condition
    with and/or
    Complex conditions must be written inside parentheses
    """
    # Remove trailing spaces to have proper formatting
    cLine = cLine.strip()
    # If condition is a single condition
    if single :
        # If first character is a (, then what's inside the parentheses is a
        # complex condition
        if cLine[0] == '(' and closingParentheseIndex(cLine) + 1 == len(cLine) :
            # If the condition is supposedly single, then the closing 
            # parenthese should be the last character
            (cList, logic) = unfoldConditions(cLine[1:-1], False)
            return { 'logic': logic, 'list': cList }
        else :
            # If the condition is a single condition, then the condition should
            # match the format `[type].[name] [operator] [value]`
            [ condition, operator, value ] = cLine.split(' ')
            [ cType, name ] = condition.split('.')
            return {
                'type': cType,
                'name': name,
                'comparison': operator,
                'value': parseValue(value),
            }
    # If condition is a complex condition, it should match the format
    # [sub-condition] [operator] [sub-condition] [operator] [sub-condition] ...
    # [operator] MUST ALWAYS be the same
    else :
        # This part recursively resolve the sub-conditions and catch the first
        # operator as the operator between all those sub-conditions (reason
        # why the operator should stay the same)
        # If the first element of the complex condition starts with a (, then
        # it is itself a comple sub-condition
        if cLine[0] == '(' :
            # Isolates the complex sub-condition group inside the parentheses
            cFirst = unfoldConditions(cLine[:closingParentheseIndex(cLine)+1], True)
            # Isolates the rest of the complex condition
            cRest = cLine[closingParentheseIndex(cLine)+1:].strip()
        # If the first element is a simple condition
        else :
            # Isolates the first sub-condition
            firstCond = ' '.join(cLine.split(' ')[:3])
            # Get the matching condition
            cFirst = unfoldConditions(firstCond)
            # Isolate the rest of the condition
            cRest = ' '.join(cLine.split(' ')[3:])
        # If the sub-condition is alone, returns the sub-condition
        if cRest.find(' ') == -1:
            return ([cFirst], 'and')
        # Isolates the operator from the sub-condition
        operator = cRest.split(' ')[0]
        # Isolate the rest of the sub-conditions
        cRest = cRest[len(operator):].strip()
        # Unfold the sub-conditions 2+
        (cRestList, cRestLogic) = unfoldConditions(cRest, False)
        # Returns the list of sub-conditions with matching operator for the
        # complex condition
        return ([cFirst] + cRestList, operator)

def priorityParser(plFile, absolute = False) :
    """Open a priority list file and convert it to a priority list object as
    used by the algorithm
    plFile should be the name of the file; priority list files end with .plist
    plFile can be with or without the extension (monk and monk.plist match the
    monk.plist file)
    A condition line should match the format
    `[prepull ]{group}.{skill}[ if {condition}]`
    """
    # Format the file name
    if not absolute:    
        plFile = 'priorityLists/' + plFile
        if plFile[-6:] != '.plist':
            plFile = plFile + '.plist'
    # Opens the file and gets the lines from the file
    with open(plFile, 'r') as f:
        pLines = [ re.sub(' +', ' ', l.rstrip('\n').strip()) for l in f.readlines() if l != '\n' and l[0] != '#' ]
    pList = []
    # Create a priority element for each line of the priority list file
    for pLine in pLines :
        pElement = {}
        # if the current line starts with prepull then add prepull = True to
        # the priority element
        if pLine[:7] == 'prepull':
            pElement['prepull'] = True
            pLine = pLine[8:]
        # Get the skill group and name for the given line
        skill = pLine.split(' ')[0]
        pElement['group'] = skill.split('.')[0]
        pElement['name'] = skill.split('.')[1]
        pLine = pLine[len(skill):]
        # Add conditions if the line has a if statement after the skill name
        if len(pLine) > 3 and pLine[1:3] == 'if':
            pLine = pLine[4:]
            pElement['condition'] = unfoldConditions(pLine)
        # Add priority element to the priority list
        pList = pList + [pElement]
    return pList

def foldConditions(condition) :
    """Fold conditions to convert the condition of a priority element to the
    formatted string of the priority file matching the condition
    """
    # If the condition is simple
    if 'comparison' in condition :
        return condition['type'] + '.' + condition['name'] + ' ' + condition['comparison'] + ' ' + str(condition['value'])
    # If the condition is complex
    else :
        return '(' + (' ' + condition['logic'] + ' ').join([ foldConditions(c) for c in condition['list'] ]) + ')'

def priorityDeparser(pList) :
    """Convert a priority list to a string formatted as in a priority list file
    """
    pLines = []
    for pElem in pList:
        pLine = ''
        # If the element is for prepull add prepull at the beginning of the 
        # line
        if 'prepull' in pElem:
            pLine = 'prepull '
        # Add the skill group and name to the line
        pLine = pLine + pElem['group'] + '.' + pElem['name']
        # Add the conditions to the line
        if 'condition' in pElem and pElem['condition'] != None:
            pLine = pLine + ' if ' + foldConditions(pElem['condition'])
        pLines = pLines + [pLine]
    return '\n'.join(pLines)