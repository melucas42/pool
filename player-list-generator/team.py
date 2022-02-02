import requests
from collections import namedtuple


class Team(object):
    id = 0
    name = ""
    abbreviation = ""

    def __init__(self, id, name, abbreviation):
        self.id = id
        self.name = name
        self.abbreviation = abbreviation


class Teams(object):
    teamList = []

    def __init__(self):
        response = requests.get("https://statsapi.web.nhl.com/api/v1/teams")
        data = response.json()
        for d in data['teams']:
            team = Team(d['id'], d['name'], d['abbreviation'])
            self.teamList.append(team)
        
        arizona = Team(0, "Phoenix Coyotes", "ARI")
        atlanta = Team(0, "Atlanta Thrashers", "ATL")
        self.teamList.append(arizona)
        self.teamList.append(atlanta)

    def getTeamFromName(self, name):
        return next((x for x in self.teamList if x.name == name), None)

    def getTeamFromId(self, id):
        return next((x for x in self.teamList if x.id == id), None)
