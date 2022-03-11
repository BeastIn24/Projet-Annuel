from Matchups import*
from Parser import*

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'toJSON'):
            return obj.toJSON()
        else:
            return json.JSONEncoder.default(self, obj)

class MatchupsTable :
    def __init__(self, *args):
        #Case where decklist + match up table were given
        if(len(args) == 2):
            self.deckList = args[0]
            self.table = args[1]
        #Case where path to json file was given
        elif(len(args) == 1):
            with open(args[0]) as file_handler:
                mut_JSON = json.load(file_handler)
                self.deckList = mut_JSON["deckList"]
                self.table = []

                for mu_list in mut_JSON["table"]:
                    row = []
                    for mu in mu_list:
                        row.append(Matchups(mu["winrate"],mu["interval"],mu["nbMatches"]))
                    self.table.append(row)


    def __str__(self):
        print (self.deckList, '\n')
        for i in range(len(self.table)):
            for j in range(len(self.table)):
                print (self.table[i][j].getWinrate(), ' | ', end='')
            print('\n')

    def isMatchupPositive (self, deck1, deck2, epsilon = 0):
        i = self.deckList.index(deck1)
        j = self.deckList.index(deck2)
        # Arbitrairement on décide qu'un winrate de 50% correspond à un matchup positif pour les deux
        if self.table[i][j].getWinrate() >= (50 - epsilon):
            return 1
        else :
            return 0

    def getMatchup (self, deck1, deck2):
        i = self.deckList.index(deck1)
        j = self.deckList.index(deck2)
        return self.table[i][j].getWinrate()

    def matchupUtility (self, deck1, deck2):
        i = self.deckList.index(deck1)
        j = self.deckList.index(deck2)
        return 2*(self.table[i][j].getWinrate()/100)-1

    def getDeckList(self):
        return self.deckList

    #Serialize in a json file
    def serialize(self, file_path):
        with open(file_path, 'w') as fh:
            json.dump(self.toJSON(), fh, cls=ComplexEncoder, indent = True)

    #Save the table as JSON file in case we need it for later experiments
    def toJSON(self):
        #Just to put attributes in a dict automatically
        return dict(deckList=self.deckList, table=self.table)
