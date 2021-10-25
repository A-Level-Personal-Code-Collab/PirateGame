#---------------------------------------------------------------------#
# File: https://github.com/A-Level-Personal-Code-Collab/PirateGame/gameplay.py
# Project: https://github.com/A-Level-Personal-Code-Collab/PirateGame
# Created Date: Monday, October 25th 2021, 7:27:52 pm
# Description: All of the functionality that deals with core gameplay functions
# Author: Will Hall
# Copyright (c) 2021 Lime Parallelogram
# -----
# Last Modified: Mon Oct 25 2021
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
#---------------------------------------------------------------------#
#=========================================================#
#^ Imports required modules ^#
from flask import Markup
from string import Template
import random
import json

#=========================================================#
#^ Game generaion systems ^#
class generators:
    def __init__(self):
        self.html = self.HTML()

    class HTML:
        #---------------#
        #Draws the grid but this time in the form of an uneditable play board
        def drawGameplayGrid(self,xSize,gridSerial,IMAGE_URLS):
            self.gridList = gridSerial.split(",")
            self.gridHTML = '<table id="tbl_playGrid">'
            self.gridSquareHTMLTemplate = Template('<td id="$id" class="gridSquare">$inner</td>') #Creates template strings for the individual HTML td elements
            self.gridImageTemplate = Template('<img class="gridItems" src="$url"/>') #Template string for the images that go inside the td elements
            
            #Calculated the y-size as only the X was provided
            if len(self.gridList) % xSize != 0:
                raise "GRID DIMENSION ERROR"
            ySize = int(len(self.gridList) / xSize)

            colLabels = [""] + list(map(chr, range(65,65+xSize))) #Creates a list of collum lables using capital letters
            self.gridHTML += "<tr>"

            #Creates the collum lables row
            for col in colLabels:
                self.gridHTML += self.gridSquareHTMLTemplate.substitute(id=None,inner=col)

            #Runs through all other rows
            counter = 0 #Allows for IDs to be named serially
            for y in range(ySize):
                self.gridHTML += "</tr><tr>"
                self.gridHTML += self.gridSquareHTMLTemplate.substitute(id=None, inner=str(y+1)) #Adds the row lable
                for x in range(xSize): #Runs through all other collums in that row
                    itemName = self.gridList[(x+y*xSize)] #Loads the item name from serial list corresponding to the coordinate in question
                    imageUrl = IMAGE_URLS[itemName]
                    self.gridHTML += self.gridSquareHTMLTemplate.substitute(id=f"square{counter}",inner=self.gridImageTemplate.substitute(url=imageUrl)) #Adds new td object based on template string
                    counter += 1

            self.gridHTML += "</tr></table>"
            return Markup(self.gridHTML)
        
        #---------------#
        #Builds the HTML syntax to draw the game grid - makes the grid easily exapandable + avoid typing repetative HTML code
        def buildEditableGrid(self,gridX,gridY):
        #Imports modules 
            #Local Constants
            CLASS_NAME = "gridSquare" #The name of the class that all td objects will share

            #Grid variable will acumulate the HTML table
            self.grid = "<table id=\"tbl_CoordinatesGrid\">"

            self.collums = [" "] #The lables on the X-Axis
            for l in range(gridX):
                self.collums.append(chr(65+l)) #Generate X axis labels using ASCII character integers
            self.rows = list(range(1,gridY+1)) #The Y-axis lables

            #Adds heading row
            self.grid += "<tr id=\"trw_gridHeading\">"
            for l in self.collums:
                self.grid += f"<td class=\"{CLASS_NAME}\" idng dynamic html=\"tdt_gridLabelCol{l}\">{l}</td>"
            self.grid += "</tr>"

            #Adds rest of grid
            for row in self.rows:
                self.grid += "<tr>"
                for col in self.collums:
                    if col == " ":
                        self.grid += f"<td class=\"{CLASS_NAME}\" id=\"tdt_gridLabelCol{row}\">{row}</td>"
                    else:
                        self.grid += f"<td class=\"{CLASS_NAME} dragReceptical\" id=\"tdt_grid{col}{row}\"></td>"
                self.grid += "</tr>"

            self.grid += "</table>"

            #Return finnished grid as Markdown and not plain text
            return Markup(self.grid)

    #---------------#
    #Returns the users that are currently part of a game 
    def getActiveUsersDictionary(self, gameID,userTBL):
        self.allUsers = userTBL.query.filter(userTBL.userGameID==gameID,userTBL.userGrid!=None,userTBL.socketioSID!=None).all()
        self.SIDNick = {} #Creates dictionary with key of SID and value of nickname
        for user in self.allUsers:
            self.SIDNick[user.userSID] = user.userNickname

        return self.SIDNick
    
    #---------------#
    #Generates a random order for the gameplay grid
    def generate_playOrder(self,gridArea):
        self.playOrder = list(map(str,range(0,gridArea)))
        random.shuffle(self.playOrder)
        self.csvString = ",".join(self.playOrder)
        return self.csvString

    #---------------#
    def generate_SID(self,usersTBL):
        ID_MAX = 99999999
        self.userSID = random.randint(0,ID_MAX)
        while usersTBL.query.get(self.userSID) != None: #Check if chosen SID already exists and keep regerating until it doesn't
            self.userSID = random.randint(0,ID_MAX)
        
        return self.userSID

#=========================================================#
#^ Data validation routines ^#
class validators:
    #---------------#
    #Checks that the inputted nickname is valied
    def nicknameValidate(self,nickname):
        NICKNAME_MAX_LEN = 15
        NICKNAME_MIN_LEN = 3
        BLACKLIST_FILE = "static/nickname-word-blacklist.csv"

        nickname = nickname.lower().replace(" ","")

        #---------------#
        #Simple length check (secconds javascript check)
        self.nicknameLen = len(nickname)
        if self.nicknameLen > NICKNAME_MAX_LEN or self.nicknameLen < NICKNAME_MIN_LEN:
            return False
        
        #---------------#
        #Checks banned words lists
        self.blacklist = open(BLACKLIST_FILE, 'r')
        self.rejectWords = self.blacklist.read().split(",")
        self.blacklist.close()

        #Loop through banned words and check them all
        for word in self.rejectWords:
            wordLen = len(word)
            if not wordLen > self.nicknameLen: #If word in question is longer than nickname then ignore it
                if word == nickname: #Check if word _is_ nickname
                    return False
                numSubstrings = self.nicknameLen - wordLen + 1 #Calculated how many possible substrings there are of any given word
                for i in range(numSubstrings): #Finds and checks all substrings of nickname to the length of the check word
                    substring = nickname[i:i+wordLen]
                    if substring == word:
                        return False
        return True
    
    #---------------#
    #Checks that the provided game ID exists
    def gameIDValidate(self,gameID,gameTBL):
        if gameTBL.query.get(int(gameID)):
            return True
        else:
            return False
    
    #---------------#
    #Checks if a given user SID is the host of a game
    def isHost(self,SID,gameID,gameTBL):
        self.qurRes = gameTBL.query.filter(gameTBL.hostSID==SID,gameTBL.gameID==gameID).all()
        if self.qurRes:
            return True
        else:
            return False

#=========================================================#
#^ Parsing system ^#
class parsers:
    #---------------#
    #Takes the money expression and calculates actual values with it
    def parse_money(self,expression,victim,perpetrator=None):
        self.vCash = victim.userCash
        self.vBank = victim.userBank
        self.pCash = perpetrator.userCash if perpetrator else 0
        self.pBank = perpetrator.userBank if perpetrator else 0

        #Substitute numbers in to expression to replace variables in order to make latter raplcement easier (e.g. {vCash} to 0)
        expression = expression.format(vCash=self.vCash,vBank=self.vBank,pCash=self.pCash,pBank=self.pBank)

        #Calculate each part of the formula individually (e.g. self.pCah=300+1000 is one)
        for e in expression.split(":"):
            exec(e) #Executes the string expression
        
        return self.vCash, self.vBank, self.pCash, self.pBank

#=========================================================#
#^ Gameplay Events ^#
class events:
    #---------------#
    #Ends the game just before the progression to the results page
    def gameEnd(self, gameID,gameTBL,usersTBL,gameDB):
        self.allUsers = usersTBL.query.filter(usersTBL.userGameID==int(gameID)).all()
        self.gameOBJ = gameTBL.query.get(int(gameID))

        #collects users final cash amounts and sorts them in a dictionary
        userscore = {}
        for User in self.allUsers:
            userscore[User.userNickname] = User.userCash + User.userBank

        self.gameOBJ.resultsScores = json.dumps(userscore)
        usersTBL.query.filter(usersTBL.userGameID==int(gameID)).delete()

        gameDB.session.commit()