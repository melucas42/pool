import requests
import json
from player import Player
from player import Players


class TeamRoster(object):

    def getTeamRoster(self, year, playerList):
        self.players = playerList
        # https://statsapi.web.nhl.com/api/v1/teams?expand=team.roster&season=20142015
        url = "https://statsapi.web.nhl.com/api/v1/teams?expand=team.roster&season=" + year
        response = requests.get(url)
        data = response.json()

        for team in data['teams']:
            print("Getting roster for team " +
                  team['abbreviation'] + " season " + year)
            for player in team['roster']['roster']:
                p = Player(player['person']['id'])
                p.team = team['abbreviation']
                playerList.add(p)
