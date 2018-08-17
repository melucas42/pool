from player import Player
from player import Players
from teamroster import TeamRoster
from draft import Draft
from team import Teams

minYear = 2013
maxYear = 2017

playerList = Players()
teamRoster = TeamRoster()
draftPick = Draft()
teams = Teams()

for currentYear in range(maxYear, minYear, -1):
    season = str(currentYear) + "" + str(currentYear + 1)
    print("Getting rosters for year", season)
    teamRoster.getTeamRoster(season, playerList)
    draftPick.getDraftPlayers(currentYear, teams, playerList)

playerListFile = "C:\\playerList.txt"
open(playerListFile, 'w').close()
playerList.writePlayerList(playerListFile)
print("Done")
