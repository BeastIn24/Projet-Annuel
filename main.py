from sys import argv
from Parser import *
from ProbabilistGame import *
from DeterministGame import *
import json

#Loading of matchupTable (different depending on how the script was called)
if(len(argv) == 3):
    #case "Python3 main.py"
    parser = Parser()
    list = parser.getTable()
    matchupTable = MatchupsTable(list[0], list[1])
elif(len(argv) == 5):
    if(argv[1] == "save"):
        #case "Python3 main.py save "file_path" "
        parser = Parser()
        list = parser.getTable()
        matchupTable = MatchupsTable(list[0], list[1])
        matchupTable.serialize(argv[2])

    elif(argv[1] == "load"):
        #case "Python3 main.py load "file_path" "
        matchupTable = MatchupsTable(argv[2])
    else:
        raise Exception("First arg can only be \"save\" or \"load\"")
else:
    raise Exception("To use this script, \n  1. add no argument to load the matchupTable from https://mtgmeta.io/metagame. \n  2. add \" save \" or \" load \" + the path to a correct JSON file to save/load the matchup table to/from.")

# computations
sys.setrecursionlimit(100000)
if argv[3] == 'd' :
    G = DeterministGame(matchupTable, int(argv[4]))
else :
    G = ProbabilistGame(matchupTable, int(argv[4]))

print("\nListe de départ :\n" ,  matchupTable.getDeckList(), "\n")
tlist = G.siler(matchupTable.getDeckList())
print("Coalition obtenue avec Siler : \n",  tlist)
print("Utilité globale : ", G.globalUtility(tlist))
if G.isNashStable(tlist) :
    print ("La coalition est stable au sens de Nash.")
else :
    print ("La coalition n'est pas stable au sens de Nash.")
"""
if G.isCoreStable(tlist) :
    print ("La coalition est stable au sens du coeur.")
else :
    print ("La coalition n'est pas stable au sens du coeur.")
"""
tlist2 = G.arnold(matchupTable.getDeckList())
print("\nCoalition obtenue avec Arnold : \n",  tlist2)
print("Utilité globale : ", G.globalUtility(tlist2))
if G.CIS(tlist2) :
    print ("La coalition est contractuellement individuellement stable.")
else :
    print ("La coalition n'est pas contractuellement individuellement stable.")
