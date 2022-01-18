from MatchupsTable import *
import math
from itertools import chain, combinations
import sys

class Game :
    def __init__ (self, matchupTable):
        self.matchupTable = matchupTable

    def deckUtilitySingleton (self, deck, tierlist):
        p = tierlist.index(deck)
        utility = 0
        for i in range (p+1, len(tierlist)):
            if self.matchupTable.isMatchupPositive(deck, tierlist[i]) == 1:
                utility += 1
            elif self.matchupTable.isMatchupPositive(deck, tierlist[i]) == 0:
                utility -= 1
        return utility

    def deckUtility (self,deck, tierlist):
        utility = 0
        for t in range(len(tierlist)-1) :
            for d in range(len(tierlist[t])-1) :
                if tierlist[t][d] == deck:
                    deckTier = t
        for i in range (deckTier, len(tierlist)-1):
            for j in range(len(tierlist[i])-1):
                if deck != tierlist[i][j]:
                    if self.matchupTable.isMatchupPositive(deck, tierlist[i][j]) == 1:
                        utility += 1
                    elif self.matchupTable.isMatchupPositive(deck, tierlist[i][j]) == 0:
                        utility -= 1
        return utility

    def siler (self, tierlist):
        maxUtilityTierList = tierlist.copy()
        change = True
        while change :
            change = False
            for deck in tierlist:
                max = self.deckUtilitySingleton(deck, tierlist)
                for i in range (1, len(tierlist)):
                    potentialTierList = tierlist.copy()
                    potentialTierList.remove(deck)
                    potentialTierList.insert(i, deck)
                    u = self.deckUtilitySingleton(deck, potentialTierList)
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
            initUtility = self.deckUtilitySingleton(deck, tierlist)
            j = 0
            while (j < len(tierlist)) :
                if (j != i):
                    potentialTierList = tierlist.copy()
                    potentialTierList.remove(deck)
                    potentialTierList.insert(j, deck)
                    potentialUtility = self.deckUtilitySingleton(deck, potentialTierList)
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
                listInitUtility.append(self.deckUtilitySingleton(deck, tierlist))
            j = 0
            listPotentialUtility = []
            while (j < len(tierlist)) :
                potentialTierList = tierlist.copy()
                for i in range (len(subSet), 0) :
                    potentialTierList.remove(deck)
                    potentialTierList.insert(j, deck)
                for k in range(len(subSet)) :
                    if(self.deckUtilitySingleton(subSet[k], potentialTierList) > listInitUtility[k]):
                        return False
                j += 1
        return True

    def arnold(self, tierlist):
        tierQueue = []
        siler = self.siler(tierlist)
        i = len(tierlist)-1
        c = 0
        while i > 1:
            if self.matchupTable.isMatchupPositive(siler[i], siler[i-2]):
                nouveauTier = [siler[i], siler[i-1], siler[i-2]]
                tierQueue.insert(0, nouveauTier)
                i -= 3
                c += 3
            else :
                tierQueue.insert(0, [siler[i]])
                i -= 1
                c += 1
        if len(tierlist) - c == 2 :
            tierQueue.insert(0, [siler[1]])
            tierQueue.insert(0, [siler[0]])
        if len(tierlist) - c == 1 :
            tierQueue.insert(0, [siler[0]])

        change = True
        while change:
            change = False
            j = len(tierQueue)-1
            while j > 1 :
                potentialTier = []
                potentialTier.extend(tierQueue[j])
                potentialTier.extend(tierQueue[j-1])
                potentialTier.extend(tierQueue[j-2])
                ok = True
                for deck1 in potentialTier :
                    nbMuPos = 0
                    for deck2 in potentialTier :
                        if deck1 != deck2 :
                            if self.matchupTable.isMatchupPositive(deck1, deck2):
                                nbMuPos += 1
                    if not (float(nbMuPos)/len(potentialTier)) >= 0.5 :
                         ok = False
                if ok :
                    tierQueue.remove(tierQueue[j])
                    tierQueue.remove(tierQueue[j-1])
                    tierQueue.remove(tierQueue[j-2])
                    tierQueue.insert(j-2, potentialTier)
                    change = True
                    j -= 3
                else :
                    j -= 1
                #Que faut il retourner ? comment obtient on la tierlist finale ?
            return tierQueue

    def CIS (self, tierlist):
        #Init du tab deck utilities
        initUtilities = []
        for i in range(len(tierlist)-1):
            tierUtilities = []
            for j in range(len(tierlist[i])-1):
                deck = tierlist[i][j]
                tierUtilities.append(self.deckUtility(deck, tierlist))
            initUtilities.append(tierUtilities)

        #Pour chaque mvt de deck
        for i in range(len(tierlist)-1):
            for j in range(len(tierlist[i])-1):
                deck = tierlist[i][j]
                #Calcule et comparaison des utilities des decks dans les tier de départ et d'arrivés
                for k in range(len(tierlist)-1):

                    # Pour pas bouger notre deck dans le même tier
                    if i != k :
                        potentialTierList = tierlist.copy()
                        print(deck)
                        print(tierlist)
                        potentialTierList[i].remove(deck)
                        potentialTierList[k].append(deck)

                        potentialUtilities = initUtilities.copy()
                        potentialUtilities[i].remove(initUtilities[i][j])
                        potentialUtilities[k].append(initUtilities[i][j])

                        #Pour le tier de départ
                        for l in range(len(tierlist[i])-1):
                            deck2 = tierlist[i][l]
                            if self.deckUtility(deck2, potentialTierList) > potentialUtilities[i][l]:
                                return False
                        #Pour le tier d'arrivé
                        for m in range(len(tierlist[k])-1):
                            deck2 = tierlist[k][m]
                            if self.deckUtility(deck2, potentialTierList) > potentialUtilities[k][m]:
                                return False
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
