import requests
import json
from collections import namedtuple
from player import Player
from dateutil.relativedelta import relativedelta
from datetime import datetime

minYear = 2015
maxYear = 2018

dateObject = datetime.strptime('2018-01-17', '%Y-%M-%d')

playerList = []

player1 = Player()
player1.fullName = "le gros"
player1.age = 3
player1.draftId = 1
player1.getPlayerFromNhl(123)

player2 = Player()
player2.fullName = "le chef"
player2.age = 2
player2.draftId = 1


playerList.append(player1)
playerList.append(player2)
#playerList.sort(key=lambda x: x.age)
playerList.sort(key=lambda x: x.age, reverse=False)
for p in playerList:
    print(p.fullName)
    print(p.age)


#response = requests.get("https://statsapi.web.nhl.com/api/v1/draft/prospects/")
#data = response.json()
#f= open("prospects.json","w+")
# json.dump(data,f)

#response = requests.get("https://statsapi.web.nhl.com/api/v1/draft/2018")
#data = response.json()
#f= open("draft-2018.json","w+")
# json.dump(data,f)

#response = requests.get("https://statsapi.web.nhl.com/api/v1/draft/2017")
#data = response.json()
#f= open("draft-2017.json","w+")
# json.dump(data,f)


#response = requests.get("https://statsapi.web.nhl.com/api/v1/draft/prospects/72816")
#data = response.json()
#f= open("DennisBusby.json","w+")
# json.dump(data,f)


response = requests.get("https://statsapi.web.nhl.com/api/v1/teams")
data = response.json()
#f = open("teams.json","w+")
# json.dump(data,f)
d_named = namedtuple("Teams", data.keys())(*data.values())
# print(data.get("teams"))
print(d_named.teams[0])

#response = requests.get("https://statsapi.web.nhl.com/api/v1/teams?expand=team.roster&season=20142015")
#data = response.json()
#f= open("teams20172018.json","w+")
# json.dump(data,f)

# sami vatanen


#response = requests.get("https://statsapi.web.nhl.com/api/v1/people/8475222")
#data = response.json()
#f= open("vatanen.json","w+")
# json.dump(data,f)

# with open('data.json', 'w') as outfile:
#    json.dump(request.content, outfile)

# https://statsapi.web.nhl.com/api/v1/draft/prospects/ID

a = 1
b = 2

print(a+b)
