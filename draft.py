import requests
import json
from team import Team
from player import Player
from player import Players


class Draft(object):

    def getDraftPlayers(self, draftYear, teams, playerList):
        print("Getting draft " + str(draftYear))
        self.players = playerList

        url = "https://statsapi.web.nhl.com/api/v1/draft/" + str(draftYear)
        response = requests.get(url)
        data = response.json()

        for round in data['drafts'][0]['rounds']:
            for pick in round['picks']:
                try:
                    id = pick['prospect']['id']
                except:
                    id = "0"

                isProspect = True
                player = Player(id, isProspect)
                team = teams.getTeamFromName(pick['team']['name'])

                if team is None:
                    if(pick['team']['name'] == "Phoenix Coyotes"):
                        player.team = "ARI"
                else:
                    player.team = team.abbreviation

                if id == "0":
                    player.fullName = pick['prospect']['fullName']

                playerList.add(player)
