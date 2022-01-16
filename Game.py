from MatchupsTable import *
import math
from itertools import chain, combinations
import sys

class Game :
    def __init__ (self, matchupTable):
        self.matchupTable = matchupTable

    def deckUtility (self, deck, tierlist):
        p = tierlist.index(deck)
        utility = 0
        for i in range (p+1, len(tierlist)):
            if self.matchupTable.isMatchupPositive(deck, tierlist[i]) == 1:
                utility += 1
            elif self.matchupTable.isMatchupPositive(deck, tierlist[i]) == 0:
                utility -= 1
        return utility

    def siler (self, tierlist):
        maxUtilityTierList = tierlist.copy()
        change = True
        while change :
            change = False
            for deck in tierlist:
                max = self.deckUtility(deck, tierlist)
                for i in range (1, len(tierlist)):
                    potentialTierList = tierlist.copy()
                    potentialTierList.remove(deck)
                    potentialTierList.insert(i, deck)
                    u = self.deckUtility(deck, potentialTierList)
                    if u > max :
                        max = u
                        maxUtilityTierList = potentialTierList.copy()
                        change = True
                tierlist = maxUtilityTierList.copy()
        return tierlist

    def firstTest (self, tierlist):
        for i in range(0, len(tierlist)-1):
            if self.matchupTable.isMatchupPositive(tierlist[i], tierlist[i+1]) < 1 :
                return False
        return True

    # Tester si aucun changement individuel n'est possible (augmenterait l'utilité d'un deck)
    def isNashStable (self, tierlist):
        for i in range(0, len(tierlist)):
            deck = tierlist[i]
            initUtility = self.deckUtility(deck, tierlist)
            j = 0
            while (j < len(tierlist)) :
                if (j != i):
                    potentialTierList = tierlist.copy()
                    potentialTierList.remove(deck)
                    potentialTierList.insert(j, deck)
                    potentialUtility = self.deckUtility(deck, potentialTierList)
                    if(potentialUtility > initUtility):
                        return False
                j += 1
        return True

    def powerSet(self, string):
        subSets = []
        n = len(string)
        for i in range(0,n+1):
            for element in combinations(string,i):
                subSets.append(element)
        return subSets

    def isCoreStable (self, tierlist):
        subSets = self.powerSet(tierlist)
        for subSet in subSets :
            listInitUtility = []
            for deck in subSet :
                listInitUtility.append(self.deckUtility(deck, tierlist))
            j = 0
            listPotentialUtility = []
            while (j < len(tierlist)) :
                potentialTierList = tierlist.copy()
                for i in range (len(subSet), 0) :
                    potentialTierList.remove(deck)
                    potentialTierList.insert(j, deck)
                for k in range(len(subSet)) :
                    if(self.deckUtility(subSet[k], potentialTierList) > listInitUtility[k]):
                        return False
                j += 1
        return True

# Main pour vérifier le fonctionnement des tests
# sys.setrecursionlimit(100000)
# parser = Parser()
# list = parser.getTable()
# matchupTable = MatchupsTable(list[0], list[1])
# G = Game(matchupTable)
# tlist = G.siler(matchupTable.getDeckList())
# print(tlist)
# print("1st test : ", G.firstTest(tlist))
# print("Nash Stable :", G.isNashStable(tlist))
# print("Core Stable :", G.isCoreStable(tlist))

# Avec parsing de la matchupTable
# parser = Parser()
# list = parser.getTable()
# matchupTable = MatchupsTable(list[0], list[1])
# matchupTable.serialize()
# G = Game(matchupTable)

# Avec deserialisation de la matchupTable
# sys.setrecursionlimit(100000)
# matchupTable = MatchupsTable("saved_matchup_tables/test.json")
# G = Game(matchupTable)
# # print(G.matchupTable)
# tlist = G.siler(matchupTable.getDeckList())
# print(tlist)
# print("1st test : ", G.firstTest(tlist))
# print("Nash Stable :", G.isNashStable(tlist))
# print("Core Stable :", G.isCoreStable(tlist))
