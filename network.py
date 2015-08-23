#!/usr/bin/env python

"""Generate a visual representation of a social network"""

from itertools import combinations
import random
from collections import deque
import json

def loadPeople():
    inputPath  = 'people.txt'#raw_input('The file with your people: ')
    with open(inputPath, 'r') as inputFile:
        return inputFile.read().splitlines()

def loadRelationships(people):
    relationships = list(combinations(people,2))
    random.shuffle(relationships)
    return relationships

def knowEachOther(relationship):
    return not raw_input("Hit enter if these people know each other {}, anything else otherwise".format(relationship))

def rankRelationships(relationships):
    ranking = []
    while (True):
        first = relationships.pop()
        if knowEachOther(first):
            ranking.append([first])
            break
    while (relationships):
        current = relationships.pop()
        if knowEachOther(current):
            placeRelationship(current, ranking, 0, len(ranking) - 1)
    return ranking

def placeRelationship(current, ranking, strongest, weakest):
    comparisonIndex = (strongest + weakest) / 2
    comparison = random.choice(ranking[comparisonIndex])
    prompt = 'Which relationship is closer: {} (f) or {} (j), or are they equal (just enter)?'.format(current, comparison)
    choice = raw_input(prompt)
    if (choice == ''): # Equal
        ranking[comparisonIndex].append(current)
    elif (choice == 'f'):
        if (strongest == comparisonIndex): # Stronger than strongest
            ranking.insert(strongest, [current])
        else:
            placeRelationship(current, ranking, strongest, comparisonIndex - 1)
    elif (choice == 'j'):
        if (comparisonIndex == weakest): # Weaker than weakest
            ranking.insert(weakest + 1, [current])
        else:
            placeRelationship(current, ranking, comparisonIndex + 1, weakest)

def nodify(person):
    return {'name': person}

def makeLinks(people, ranking):
    result = []
    index = dict(zip(people, range(len(people))))
    for value, relationships in enumerate(reversed(ranking), start=1):
        for relationship in relationships:
            result.append({'source': index[relationship[0]], 'target': index[relationship[1]], 'value': value})
    return result

if __name__ == '__main__':
    people = loadPeople()
    print people
    relationships = loadRelationships(people)
    ranking = rankRelationships(relationships)
    print ranking

    output = {}
    output['nodes'] = map(nodify, people)
    output['links'] = makeLinks(people, ranking)
    print json.dumps(output)
