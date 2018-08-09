import requests
import json
from collections import namedtuple

class Player(object):
    nhlId = 0
    draftId = 0
    firstName = ""
    lastName = ""
    fullName = ""
    age = 0
    position = "N/A"
    team = "N/A"

    def getPlayerFromNhl(self, id):
        response = requests.get("https://statsapi.web.nhl.com/api/v1/people/8475222")
        data = response.json()
        player = namedtuple("People", data.keys())(*data.values())


