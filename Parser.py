from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support.expected_conditions import presence_of_element_located
from Matchups import*

class Parser :
    def __init__(self):
        url = "https://mtgmeta.io/metagame"
        with webdriver.Chrome() as driver:
            wait = WebDriverWait(driver, 10)
            driver.get(url)
            decksFromSite = driver.find_elements(By.CLASS_NAME, "name")
            matchupsFromSite = driver.find_elements(By.CLASS_NAME, "dperf")
            intervalsFromSite = driver.find_elements(By.CLASS_NAME, "dmatchr")
            nbMatchesFromSite = driver.find_elements(By.CLASS_NAME, "dmatch")
            deckList = []
            matchupsTable = []
            count = 1
            for i in range(13):
                deckList.append(decksFromSite[i].text)
                matchup=[]
                for j in range(13):
                    if matchupsFromSite[count].text == '' :
                        dperf = None
                        dmatch = None
                        dmatchr = None
                    else :
                        dperf = float(matchupsFromSite[count].text)
                        dmatch = float(nbMatchesFromSite[count].text)
                        a = ''.join(x for x in intervalsFromSite[count].text if x not in '%')
                        dmatchr = a.split('-')
                        for k in range (len(dmatchr)):
                            dmatchr[k] = float(dmatchr[k])
                    values = Matchups(dperf, dmatchr, dmatch)
                    matchup.append(values)
                    count +=1
                matchupsTable.append(matchup)
            self.matchupsTable = matchupsTable
            self.deckList = deckList
            print (deckList)
            print (matchupsTable[10][11])

    def getTable(self) :
        return [self.deckList, self.matchupsTable]
