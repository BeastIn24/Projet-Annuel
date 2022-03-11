from MatchupsTable import *
import math
from itertools import chain, combinations
from copy import deepcopy
import sys

class Game:

    def __init__ (self, matchupTable, epsilon = 0):
        self.matchupTable = matchupTable
        self.epsilon = epsilon

    def goodTierList (self, tierlist):
        gtl = []
        for d in tierlist :
            gtl.append([d])
        return gtl

    def globalUtility (self, tierlist):
        if not any(isinstance(i, list) for i in tierlist):
            tierlist = self.goodTierList(tierlist)
        sum = 0
        for i in range(len(tierlist)) :
            for d in tierlist[i]:
                sum += self.deckUtility(d, tierlist)
        return sum

    def siler (self, tierlist, epsilon = 0):
        maxUtilityTierList = tierlist.copy()
        change = True
        while change:
            change = False
            for deck in tierlist:
                gUtility = self.globalUtility(tierlist)
                max = self.deckUtility(deck, tierlist)
                for i in range (1, len(tierlist)):
                    potentialTierList = tierlist.copy()
                    potentialTierList.remove(deck)
                    potentialTierList.insert(i, deck)
                    u = self.deckUtility(deck, potentialTierList)
                    if u > max-epsilon and gUtility < self.globalUtility(potentialTierList) :
                        max = u
                        maxUtilityTierList = potentialTierList.copy()
                        change = True
                tierlist = maxUtilityTierList.copy()
        return tierlist

    def firstTest (self, tierlist):
        for i in range(0, len(tierlist)-1):
            if self.matchupTable.isMatchupPositive(tierlist[i], tierlist[i+1], self.epsilon) < 1 :
                print(tierlist[i])
                return False
        return True

    # Tester si aucun changement individuel n'est possible (augmenterait l'utilité d'un deck)
    # Ne prend pas en compte le cas de l'agent idiot, nous ne sommes pas Nash Stable dans un tel cas
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



    # Vérifie la stabilité contractuelle individuelle.
    # Renvoie True si aucun deck de la tierlist ne peut changer de tier
    def CIS (self, tierlist):
        #Init du tab deck utilities
        initUtilities = []
        for i in range(len(tierlist)):
            tierUtilities = []
            for j in range(len(tierlist[i])):
                deck = tierlist[i][j]
                tierUtilities.append(self.deckUtility(deck, tierlist))
            initUtilities.append(tierUtilities)

        # i : indice du tier du deck à bouger
        for i in range(len(tierlist)):
            # j indice du deck à bouger dans la liste de départ
            for j in range(len(tierlist[i])):
                # deck : nom du deck à bouger
                deck = tierlist[i][j]
                # k : indice du tier d'arrivé
                for k in range(len(tierlist)):
                    # Pour ne pas replacer notre deck dans le même tier
                    #print("i avant : ", i)
                    #print("k avant : ", k)
                    if i != k :
                        potentialTierList = deepcopy(tierlist)
                        potentialTierList[i].remove(deck)
                        potentialTierList[k].append(deck)

                        #Modifie la matrice des utilités initiales.
                        #Modifie la position de l'utilité du deck déviant pour que les indices des deux matrices restes cohérents.
                        #Les valeurs restes inchangées.
                        potentialUtilities = deepcopy(initUtilities)
                        potentialUtilities[i].remove(initUtilities[i][j])
                        potentialUtilities[k].append(initUtilities[i][j])

                        #print("K : ", k)
                        #print("Apres swap du deck : ", deck)

                        # Si au moins une déviation est possible notre tierlist n'est pas CIS.
                        #print("Matrice des utilitées avant déviation : ",initUtilities)
                        #print("Matrice des utilitées apress déviation : ",potentialUtilities)
                        if(self.isDeviationPossible(potentialTierList, potentialUtilities, i, k)):
                            return False
        return True

    # La déviation est possible si AUCUN deck des tiers concernés ne perd en utilité.
    # potentialTierList => tierlist après déplacement de deck

    # i => indice du tier de départ
    # k => indice du tier d'arrivé
    def isDeviationPossible(self, potentialTierList, potentialUtilities, i, k):
        # l : indice des decks du tier de départ i dans potentialTierList
        for l in range(len(potentialTierList[i])):
            deck2 = potentialTierList[i][l]

            #print("Pour le tier",i," de départ : ")
            #print("deck2 : ", deck2, " pos : (",i,",",l,")")
            #print("initUtility : ", potentialUtilities[i][l])
            #print("newUtility : ", self.deckUtility(deck2, potentialTierList))
            #Si un des decks du tier de départ perd en utilité, la déviation n'est pas possible
            if self.deckUtility(deck2, potentialTierList) < potentialUtilities[i][l]:
                return False
        # m : indice des decks du tier d'arrivé k dans potentialTierList
        for m in range(len(potentialTierList[k])):
            deck2 = potentialTierList[k][m]
            #print("Pour le tier",k," d'arrivée : ")
            #print("deck2 : ", deck2, " pos : (",k,",",m,")")
            #print("initUtility : ", potentialUtilities[k][m])
            #print("newUtility : ", self.deckUtility(deck2, potentialTierList))
            #Si un des decks du tier d'arrivé perd en utilité la déviation n'est pas possible
            if self.deckUtility(deck2, potentialTierList) < potentialUtilities[k][m]:
                return False

        return True
