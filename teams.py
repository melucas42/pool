import requests
import json
from collections import namedtuple
from team import Team

class Teams(object):
    teamList = []

    def __init__(self):
        response = requests.get("https://statsapi.web.nhl.com/api/v1/teams")
        data = response.json()
        for d in data['teams']:
            team = Team(d['id'], d['abbreviation'])
            self.teamList.append(team)
            #print(d['id'], d['abbreviation'])

        #d_named = namedtuple("Teams", data.keys())(*data.values())
        #print(d_named.teams[0])
        #teamList = d_named.teams
        #print(teamList[0].id)


    def getTeamFromId(self, id):
        return next((x for x in self.teamList if x.id == id), None)
