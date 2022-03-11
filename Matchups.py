import json

class Matchups :
    def __init__(self, winrate, interval, nbMatches):
        self.winrate = winrate
        self.interval = interval
        self.nbMatches = nbMatches

    #Ensure that the class is JSON encodable, says how will the instance will be encoded
    def toJSON(self):
        #Just to put attributes in a dict automatically
        return dict(winrate=self.winrate, interval=self.interval, nbMatches = self.nbMatches)

    def __str__(self):
        return f'{self.winrate}, {self.interval}, {self.nbMatches}'

    def getWinrate(self):
        return self.winrate

    def getInterval(self):
        return self.interval

    def getNbMatches(self):
        return self.nbMatches

# matchup = Matchups(50, [45,55], 250)
# print("Encode into JSON formatted Data")
# with open("saved_matchup_tables/test.json", 'w') as fh:
#     json.dump(matchup.toJSON(), fh, indent=4)
#
# print("Decode JSON formatted Data")
# with open("saved_matchup_tables/test.json") as fh:
#     muJSON_str = json.load(fh)
#     muJSON_dict = json.loads(muJSON_str)
# print(Matchups(muJSON_dict["winrate"], muJSON_dict["interval"], muJSON_dict["nbMatches"]))
