from player import Player
from player import Players
from teamroster import TeamRoster
from draft import Draft
from team import Teams

#max year should be current -1
minYear = 2010
maxYear = 2020
keeperDraftDate = "2021-09-19"

playerList = Players()
teamRoster = TeamRoster()
draftPick = Draft()
#teams = Teams()

#min 2007, max 2017
# should get season 2017-2018 to 2008-2009
# should get draft 2008
for currentYear in range(maxYear, minYear, -1):
    season = str(currentYear) + "" + str(currentYear + 1)
    draft = str(currentYear + 1)
    print("Season : " + season + "   draft: " + str(draft))
    teamRoster.getTeamRoster(season, keeperDraftDate, playerList)
    draftPick.getDraftPlayers(draft, keeperDraftDate, playerList)

playerListFile = ".\playerList.txt"
open(playerListFile, 'w').close()
playerList.writePlayerList(playerListFile)
print("Done")
