#!/usr/bin/env python

"""Generate a visual representation of a social network"""

from itertools import combinations, chain
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

def acquainted(relationship):
    return not raw_input("Hit enter if these people know each other {}, anything else otherwise".format(relationship))

def rankRelationships(relationships):
    ranking, unacquainted = loadSaved(relationships)
    if not ranking:
        while (True):
            first = relationships.pop()
            if acquainted(first):
                ranking.append([first])
                break
    while (relationships):
        current = relationships.pop()
        if acquainted(current):
            placeRelationship(current, ranking, 0, len(ranking) - 1)
        else:
            unacquainted.append(current)
    return ranking, unacquainted

def loadSaved(relationships):
    inputPath = 'ranking.txt'
    with open(inputPath, 'r') as inputFile:
        ranking = eval(inputFile.read())
    for relationship in chain.from_iterable(ranking):# For each ranked relationship
        relationships.remove(relationship) # Since it's already in the ranking

    unacquaintedPath = 'unacquainted.txt'
    with open(unacquaintedPath, 'r') as unacquaintedFile:
        unacquainted = eval(unacquaintedFile.read())
    for relationship in unacquainted:
        relationships.remove(relationship)

    return ranking, unacquainted

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

def makeLinks(people, ranking, unacquainted):
    index = dict(zip(people, range(len(people))))

    result = [{'source': index[relationship[0]], 'target': index[relationship[1]], 'value': 0} \
                for relationship in unacquainted]
    for value, relationships in enumerate(reversed(ranking), start=1):
        for relationship in relationships:
            result.append({'source': index[relationship[0]], 'target': index[relationship[1]], 'value': value})
    return result

if __name__ == '__main__':
    people = loadPeople()
    print people, '\n'
    relationships = loadRelationships(people)
    ranking, unacquainted = rankRelationships(relationships)
    print 'ranking:\n', ranking, '\n'
    print 'unacquainted:\n', unacquainted, '\n'

    output = {}
    output['nodes'] = map(nodify, people)
    output['links'] = makeLinks(people, ranking, unacquainted)
    print 'json:\n', json.dumps(output)
