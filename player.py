import requests
import json
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from datetime import datetime


class Players(object):
    playerList = []
    nextId = 1

    def add(self, player):
        existingPlayer = list(filter(lambda p: p.fullName.lower() ==
                                     player.fullName.lower() and p.birthDate == player.birthDate, self.playerList))
        if len(existingPlayer) == 0:
            player.draftId = self.nextId
            self.nextId += 1
            self.playerList.append(player)

    def writePlayerList(self, path):
        self.playerList.sort(key=lambda p:p.fullName)
        #ut.sort(key=lambda x: x.count, reverse=True)
        for player in self.playerList:
            playerInfo = str(player.draftId) + "\t" + player.fullName + "\t" + \
                player.team + "\t" + player.position + \
                "\t" + str(player.age) + "\n"
            f = open(path, "a")
            f.writelines(playerInfo)


class Player(object):
    nhlId = 0
    draftId = 0
    fullName = ""
    birthDate = ""
    age = 0
    position = "N/A"
    team = "N/A"
    isProspect = False

    def __init__(self, id, isProspect=False):

        self.nhlId = id
        if isProspect:
            if id != "0":
                self.setPropsectDetail(id)
        else:
            self.setPlayerDetail(id)

    def setPropsectDetail(self, id):
        # url sample :https://statsapi.web.nhl.com//api/v1/draft/prospects/65242
        url = "https://statsapi.web.nhl.com//api/v1/draft/prospects/" + str(id)
        response = requests.get(url)
        data = response.json()
        player = data['prospects'][0]
        self.fullName = player['fullName']
        self.birthDate = player['birthDate']
        self.age = self.getAgeAtDraft(player['birthDate'], "2018-09-23")
        self.position = player['primaryPosition']['type']
        self.isProspect = True

    def setPlayerDetail(self, id):
        # url sample : https://statsapi.web.nhl.com//api/v1/people/8470619
        url = "https://statsapi.web.nhl.com/api/v1/people/" + str(id)
        response = requests.get(url)
        data = response.json()
        player = data['people'][0]
        self.fullName = player['fullName']
        self.birthDate = player['birthDate']
        self.age = self.getAgeAtDraft(player['birthDate'], "2018-09-23")
        self.position = player['primaryPosition']['type']

    def getAgeAtDraft(self, birthDate, draftDate):
        birthDateOject = datetime.strptime(birthDate, '%Y-%M-%d')
        draftDateObject = datetime.strptime(draftDate, '%Y-%M-%d')
        ageInYears = relativedelta(
            draftDateObject, birthDateOject).years
        return ageInYears
