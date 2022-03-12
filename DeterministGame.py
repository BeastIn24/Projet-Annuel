from Game import *

class DeterministGame(Game):

    def __init__ (self, matchupTable, epsilon = 0):
        super().__init__(matchupTable, epsilon)

    def deckUtility (self,deck, tierlist):
        if not any(isinstance(i, list) for i in tierlist):
            tierlist = self.goodTierList(tierlist)
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

    def arnold(self, tierlist):
        tierQueue = []
        siler = self.siler(tierlist)
        i = len(tierlist)-1
        c = 0
        while i > 1:
            if self.matchupTable.isMatchupPositive(siler[i], siler[i-2], self.epsilon):
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
                            if self.matchupTable.isMatchupPositive(deck1, deck2, self.epsilon):
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
        return tierQueue
