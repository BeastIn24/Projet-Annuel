from Matchups import*
from Parser import*

class MatchupsTable :
    def __init__(self, deckList, table):
        self.deckList = deckList
        self.table = table

    def __str__(self):
        print (self.deckList, '\n')
        for i in range(len(self.table)):
            for j in range(len(self.table)):
                print (self.table[i][j].getWinrate(), ' | ', end='')
            print('\n')

    def isMatchupPositive (self, deck1, deck2):
        i = self.deckList.index(deck1)
        j = self.deckList.index(deck2)
        if self.table[i][j].getWinrate() > 50:
            return 1
        elif self.table[i][j].getWinrate() == 50:
            return 2
        else :
            return 0

    def getDeckList(self):
        return self.deckList
