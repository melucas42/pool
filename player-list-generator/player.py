import requests
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from datetime import datetime


class Players(object):
    playerList = []
    nextId = 1

    def add(self, player):
        
        existingPlayer = list(filter(lambda p: p.nhlId ==
                                     player.nhlId, self.playerList))

        if len(existingPlayer) == 0:
            player.draftId = self.nextId
            self.nextId += 1
            self.playerList.append(player)

    def writePlayerList(self, path):
        self.playerList.sort(key=lambda p:p.fullName)
        #ut.sort(key=lambda x: x.count, reverse=True)
        header = "ID\tName\tTeam\tPosition\tAge\tnhlId\tBirthDate\n"
        f = open(path, "a")
        f.writelines(header)

        count = 1
        for player in self.playerList:
            playerInfo = str(count) + "\t" + \
                player.fullName + "\t" + \
                player.team + "\t" + player.position + \
                "\t" + str(player.age) + "\t" + str(player.nhlId)+ "\t" + str(player.birthDate) + "\n"
            count += 1
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
    keeperDraftDate = ""

    def __init__(self, id, keeperDraftDate, isProspect=False):
        self.keeperDraftDate = keeperDraftDate
        if isProspect:
            #if id != "0":
            self.setPropsectDetail(id)
        else:
            self.setPlayerDetail(id)

    def setPropsectDetail(self, id):
        # url sample :https://statsapi.web.nhl.com//api/v1/draft/prospects/65242
        url = "https://statsapi.web.nhl.com//api/v1/draft/prospects/" + str(id)
        response = requests.get(url)
        data = response.json()
        player = data['prospects'][0]
        nhlPlayerId = player['nhlPlayerId']
        if(nhlPlayerId != None):
            self.setPlayerDetail(nhlPlayerId)
        else:
            #pas très utile en ce moment, si jamais on décide de siphonner la liste complète des prospect ça pourrait servir
            self.nhlId = id
            self.fullName = player['fullName']
            self.birthDate = player['birthDate']
            self.age = self.getAgeAtDate(player['birthDate'], self.keeperDraftDate)
            self.position = player['primaryPosition']['type']
            self.nhl = False

    def setPlayerDetail(self, id):
        # url sample : https://statsapi.web.nhl.com//api/v1/people/8470619
        url = "https://statsapi.web.nhl.com/api/v1/people/" + str(id)
        response = requests.get(url)
        data = response.json()
        player = data['people'][0]
        self.nhlId = id
        self.fullName = player['fullName']
        self.birthDate = player['birthDate']
        self.age = self.getAgeAtDate(player['birthDate'], self.keeperDraftDate)
        self.position = player['primaryPosition']['type']
        if(player["active"]):
            self.team = player["currentTeam"]["name"]

    def getAgeAtDate(self, birthDate, draftDate):
        birthDateOject = datetime.strptime(birthDate, '%Y-%m-%d')
        draftDateObject = datetime.strptime(draftDate, '%Y-%m-%d')
        ageInYears = relativedelta(
            draftDateObject, birthDateOject).years
        return ageInYears
