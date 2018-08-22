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
                    player = Player(id, True)
                    team = teams.getTeamFromName(pick['team']['name'])
                    player.team = team.abbreviation

                except:
                    id = "0"
                    player = Player(id, True)
                    player.fullName = pick['prospect']['fullName']

                playerList.add(player)
