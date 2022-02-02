from player import Player
from PyPDF2 import PdfFileReader
import os
import re
import sys

from PyPDF2.generic import TextStringObject

def extractAvailableRecruits(pdf_path, pageStart, pageEnd):
    fullText = ""
    playerList = []
    outputFile = "./availableRecruits.txt"
    open(outputFile, 'w').close()

    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        #number_of_pages = pdf.getNumPages()
        #for page in pdf.pages((pageStart - 1), (pageEnd - 1)):
        for x in range((pageStart - 1), (pageEnd - 1)):
            page = pdf.getPage(x)
            text = page.extractText()
            fullText += text
    
    headerPart1 = "[ \\n\s\-]+Rule Your Pool!  [ \\n\s\-]+www\.dobberhockey\.com[ \\n\s\-]+Page [ \\n\s\-]+[0-9]+[ \\n\s\-]+of[ \\n\s\-]+[0-9]+[ \\n\s\-]+"
    fullText = re.sub(headerPart1, "", fullText)
    

    '''
    Le seul empêchement pour ne pas enlever tous les \n au début est le article By whoever.
    Autre option : lister tous les auteurs pour trouver le début des article, ça serait p-e plus simple.
    '''
    yearRegex = "\([\\n]*2[\\n]*0[\\n]*2[\\n]*[0-1][\\n]*:[\\n\s0-9D]*\)" #(2021: 34) , on permet aussi (2020: 34) parce qu'il y a des erreur dans le rapport
    articleByRegex = "[\\n\s]+b[\\n]*y[\\n\s]+[A-Z][a-z]+[\\n]*\s[\\n]*[A-Z][a-z]+"
    articleByDobberRegex = "[\\n\s]+[bB][\\n]*y[\\n\s]+Dobber"
    draftAdviceRegex = "Draft Advice:[\-\,\\n\sA-Za-z()']*\." 
    keepScanning = True
    while(keepScanning == True):
        keepScanning = False
        isGoalie = False
        rankingStart = sys.maxsize
        rankingEnd = sys.maxsize
        instances = re.finditer(yearRegex, fullText)
        for result in instances:
            rankingStart = result.start()
            rankingEnd = result.end()
            break
        
        articleByOthersEnd = sys.maxsize
        instances = re.finditer(articleByRegex, fullText)
        for result in instances:
            articleByOthersEnd = result.end()
            break
        
        articleByDobberEnd = sys.maxsize
        instances = re.finditer(articleByDobberRegex, fullText)
        for result in instances:
            articleByDobberEnd = result.end()
            break
        
        draftAdviceStart = sys.maxsize
        draftAdviceEnd = sys.maxsize
        instances = re.finditer(draftAdviceRegex, fullText)
        for result in instances:
            draftAdviceStart = result.start()
            draftAdviceEnd = result.end()
            draftAdvice = fullText[draftAdviceStart:draftAdviceEnd]
            keepScanning = True #as long as there is draft advice there are players
            break
        
        if(draftAdviceEnd < rankingStart):
            #found a goalie
            goalie = fullText.replace("\n","").find(", G ")
            playerDetail = fullText[0:goalie + 4] + ", G "
            isGoalie = True
        else:
            #if not a goalie do your usual stuff
            articleByEnd = min(articleByOthersEnd, articleByDobberEnd)
            if(articleByEnd < rankingStart):
                playerDetail = fullText[articleByEnd:rankingEnd]
            else:
                playerDetail = fullText[0:rankingEnd]

        #goalie pas de ranking... on skip jusqu'au prochain article by
        #if(articleByEnd < rankingStart):

        #instances = re.finditer(goalie, fullText)
        #goalie = playerDetail.replace("\n","").find(", G ")
        #if(goalie > -1):
        #    playerDetail = fullText[0:goalie + 4]
        
  
        if(playerDetail.replace("\n","").find("Radim Zohorna") > -1):
            print("for debug")

        fullText = fullText[draftAdviceEnd:len(fullText) - 1]
        playerText = (playerDetail
                        .replace("\n", "")
                        .replace("Draft in late rounds (if you can afford to wait a few years).", "") 
                        .replace("Wait until next year to consider drafting.","")
                        .replace("Don't draft, this year or next.","")
                        .replace("Do not draft this year or next.","")
                        .replace("Draft ASAP.", "")
                        .replace("Don't draft, this year or next", "")
                        + " " + draftAdvice.replace("\n", "")
                        ).strip(" ")
        print(playerText)

        if(isGoalie == False):
            player = GetPlayerFromText(playerText)
            playerList.append(player)

    f = open(outputFile, "a")
    f.writelines("Name\tPosition\tRanking\tage\tAdvice\tDrafted\tInFullList\n")
    for p in playerList:
        playerInfo = str(p.name) + "\t" + \
                    str(p.position) + "\t" + \
                    str(p.ranking) + "\t" + \
                    str(p.age) + "\t" + \
                    str(p.draftAdvice) + "\t" + \
                    str(p.drafted) + "\t" + \
                    str(p.inFullList) + "\n"
        f = open(outputFile, "a")
        f.writelines(playerInfo)

def GetPlayerFromText(text): #form of text should be :  Brendan Guhle, LD (2021: 72D) Draft Advice: Do not draft.
    fullName = text.split(", ")[0].strip(" ")
    position = text.split(", ")[1][0:2].strip(" ")
    ranking = text.split(": ")[1].split(")")[0].strip(" ")
    draftAdvice = text[text.index(")") + 1:len(text)].strip(" ")
    age = "n/a"
    with open("./playerList.txt", "r") as file: #must run player list generator first
        data = file.read()
        pos = data.lower().find(fullName.lower())
        if(pos == -1):
            inFullList = False
        else:
            restOfData = data[pos:len(data)]
            age = restOfData.split("\t")[3]
            inFullList = True

    with open("./available-recruit-generator/draftedPlayerList.txt", "r") as file:
        data = file.read()
        if(data.lower().find(fullName.lower()) == -1):
            drafted = False
        else:
            drafted = True

    return Player(fullName, position, ranking, draftAdvice, age, inFullList, drafted)

def clean_text(rgx_list, text):
    new_text = text
    for rgx_match in rgx_list:
        new_text = re.sub(rgx_match, '', new_text)
    return new_text

scriptDir = os.path.dirname(os.path.realpath(__file__))
dobberReportPath = os.path.join(scriptDir, "dobberhockey2021fantasyprospectsreport.pdf")

extractAvailableRecruits(dobberReportPath, 16, 191) #191 ??
#extractAvailableRecruits(dobberReportPath, 16, 42) #191 ??
#concat toutes les pages

#entre "Draft Advice:" et "\n \n \n" --> draft advice


#cleanup
#--------------------------------------------------------------------------------\n---------------\n--\n   \nRule Your Pool!  \n-------------------------------------\n---------------------------\n-------\n--------------------\n \nwww.dobberhockey.com\n \n \nPage \n43\n \nof \n236\n \n

#si on trouve
#\n \n \nby --> inclut l'espace
#skip au prochin \n \n \n %nom du joueur%,%position% (2021:%position%)

#start : Jacob Perreault, RW (2021: 146) (2020: N/A)
#end : DH Draft Advice:
#Final-round option. 
#Long-term prospect. Don't draft, this year or next.
#Too soon. Wait until next year to consider drafting.
#Blue chip prospect, draft ASAP


#Passe à travers la liste
#extract ceux qui sont pas pris
#ajoute une note à ceux qui sont dans le concensus

#extract la page des missing in action