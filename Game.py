from MatchupsTable import *
import math

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
        for i in range(0, len(tierlist - 1)):
            if self.matchupTable.isMatchupPositive(tierlist[i], tierlist[i+1]) < 1 :
                return False
        return True

    # Tester si aucun changement individuel n'est possible (augmenterait l'utilité d'un deck)
    def isNashStable (self, tierlist):
        for i in range(0, len(tierlist)):
            deck = tierlist[i]
            initUtility = deckUtility (deck, tierlist)
            while (j < len(tierlist)) :
                if (j != i):
                    potentialTierList = tierlist.copy()
                    potentialTierList.remove(deck)
                    potentialTierList.insert(j, deck)
                    potentialUtility = deckUtility(deck, potentialTierList)
                    if(potentialUtility < initUtility):
                        return False
                j += 1
        return True

parser = Parser()
list = parser.getTable()
matchupTable = MatchupsTable(list[0], list[1])
G = Game(matchupTable)
tlist = G.siler(matchupTable.getDeckList())
print(tlist)
print(G.firstTest(tlist))
print(G.isNashStable(tlist))
