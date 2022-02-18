from Game import *

class DeterministGame(Game):

    def __init__ (self, matchupTable, epsilon = 0):
        super().__init__(matchupTable, epsilon)

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
        deckTier = 0
        for t in range(len(tierlist)) :
            for d in range(len(tierlist[t])) :
                if tierlist[t][d] == deck:
                    deckTier = t
        for i in range (deckTier, len(tierlist)):
            for j in range(len(tierlist[i])):
                if deck != tierlist[i][j]:
                    if self.matchupTable.isMatchupPositive(deck, tierlist[i][j]) == 1:
                        utility += 1
                    elif self.matchupTable.isMatchupPositive(deck, tierlist[i][j]) == 0:
                        utility -= 1
        return utility