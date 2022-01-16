from sys import argv
from Parser import *
from Game import *
import json

#Loading of matchupTable (different depending on how the script was called)
if(len(argv) == 1):
    #case "Python3 main.py"
    parser = Parser()
    list = parser.getTable()
    matchupTable = MatchupsTable(list[0], list[1])
elif(len(argv) == 3):
    print(argv[1])
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
G = Game(matchupTable)
tlist = G.siler(matchupTable.getDeckList())
print(tlist)
print("1st test : ", G.firstTest(tlist))
print("Nash Stable :", G.isNashStable(tlist))
print("Core Stable :", G.isCoreStable(tlist))
