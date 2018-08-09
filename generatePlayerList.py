import requests
import json
from collections import namedtuple
from player import Player
from teams import Teams

playerList = []
minYear = 2013
maxYear = 2017

for currentYear in range(minYear, maxYear):
    season = str(currentYear) + "" + str(currentYear + 1)
    print("Getting rosters for year", season)

teams = Teams()

myTeam = teams.getTeamFromId(4)

print(myTeam.name)


