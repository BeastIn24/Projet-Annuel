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

parser = Parser()
list = parser.getTable()
matchupsTable = MatchupsTable(list[0], list[1])
print(matchupsTable.__str__())