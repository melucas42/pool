from player import Player
from player import Players
from teamroster import TeamRoster
from draft import Draft
from team import Teams

minYear = 2007
maxYear = 2017

playerList = Players()
teamRoster = TeamRoster()
draftPick = Draft()
teams = Teams()

# should get season 2017-2018 to 2008-2009
# should get draft 2008
for currentYear in range(maxYear, minYear, -1):
    season = str(currentYear) + "" + str(currentYear + 1)
    print("Season : " + season + "   draft: " + str(currentYear))
    teamRoster.getTeamRoster(season, playerList)
    draftPick.getDraftPlayers(currentYear, teams, playerList)

playerListFile = "C:\\playerList.txt"
open(playerListFile, 'w').close()
playerList.writePlayerList(playerListFile)
print("Done")
