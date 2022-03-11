from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Matchups import*

class Parser :
    def __init__(self):
        url = "https://mtgmeta.io/metagame?e=59"
        with webdriver.Chrome(ChromeDriverManager().install()) as driver:
            wait = WebDriverWait(driver, 10)
            driver.get(url)
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='tablestats']//div[@class='dmatch']"))
            )
            decksFromSite = driver.find_elements(By.XPATH, "//div[@id='tablestats']//div[@class='square name right']//div[@class='name']")
            matchupsFromSite = driver.find_elements(By.XPATH, "//div[@id='tablestats']//div[@class='dperf']")
            intervalsFromSite = driver.find_elements(By.XPATH, "//div[@id='tablestats']//div[@class='dmatchr']")
            nbMatchesFromSite = driver.find_elements(By.XPATH, "//div[@id='tablestats']//div[@class='dmatch']")
            nbTotalMatchesFromSite = driver.find_elements(By.XPATH, "//div[@id='tablestats']//div[@class='square name right']//div[@class='stats']//span")
            deckList = []
            matchupsTable = []
            totalMatchesTable = []
            count = 0
            taille = len(decksFromSite)
            for i in range(taille):
                deckList.append(decksFromSite[i].text)
                if i%2 == 0 :
                    totalMatchesTable.append(nbTotalMatchesFromSite[i].text)
                matchup=[]
                for j in range(taille):
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
            self.totalMatchesTable = totalMatchesTable

    def getTable(self) :
        return [self.deckList, self.matchupsTable, self.totalMatchesTable]
