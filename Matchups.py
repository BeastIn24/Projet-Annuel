class Matchups :
    def __init__(self, winrate, interval, nbMatches):
        self.winrate = winrate
        self.interval = interval
        self.nbMatches = nbMatches

    def __str__(self):
        return f'{self.winrate}, {self.interval}, {self.nbMatches}'
    
    def getWinrate(self):
        return self.winrate

    def getInterval(self):
        return self.interval

    def getNbMatches(self):
        return self.nbMatches