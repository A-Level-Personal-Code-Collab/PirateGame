#---------------------------------------------------------------------#
# File: https://github.com/A-Level-Personal-Code-Collab/PirateGame/gameplay.py
# Project: https://github.com/A-Level-Personal-Code-Collab/PirateGame
# Created Date: Monday, October 25th 2021, 7:27:52 pm
# Description: All of the functionality that deals with core gameplay functions
# Author: Will Hall
# Copyright (c) 2021 Lime Parallelogram
# -----
# Last Modified: Sun Oct 31 2021
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2021-10-31	WH	Spelling corrections
# 2021-10-30	WH	Added checks to gameIDValidate to allow no-sid access to results page
# 2021-10-30	WH	Handler for null or invalid gameID in validation routine
# 2021-10-29	WH	Added deletion scheduling to game end routine
# 2021-10-29	WH	Added check for if a game is complete or not
# 2021-10-29	WH	Implemented a hard cap on the number of users per game (80 persons) Issue #105
# 2021-10-27	WH	Added an isOnline function to check if a user is online
# 2021-10-27	WH	Added error generator routine
# 2021-10-27	WH	Modified GameIDVerify to allow reconnecting users to a closed game
# 2021-10-27	WH	Added decorator routine to verify requested information when a user connects to a game
# 2021-10-27	WH	Modified gameID validator
# 2021-10-27	WH	Added is online validator
# 2021-10-27	WH	Added class loggers and disconnect logger
# 2021-10-25	WH	Moved all subroutines and classes from main file
#---------------------------------------------------------------------#
#=========================================================#
#^ Imports required modules ^#
import time
from flask import Markup, request, redirect
from string import Template
import random
import json
from functools import wraps

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

            colLabels = [""] + list(map(chr, range(65,65+xSize))) #Creates a list of column lables using capital letters
            self.gridHTML += "<tr>"

            #Creates the column lables row
            for col in colLabels:
                self.gridHTML += self.gridSquareHTMLTemplate.substitute(id=None,inner=col)

            #Runs through all other rows
            counter = 0 #Allows for IDs to be named serially
            for y in range(ySize):
                self.gridHTML += "</tr><tr>"
                self.gridHTML += self.gridSquareHTMLTemplate.substitute(id=None, inner=str(y+1)) #Adds the row label
                for x in range(xSize): #Runs through all other columns in that row
                    itemName = self.gridList[(x+y*xSize)] #Loads the item name from serial list corresponding to the coordinate in question
                    imageUrl = IMAGE_URLS[itemName]
                    self.gridHTML += self.gridSquareHTMLTemplate.substitute(id=f"square{counter}",inner=self.gridImageTemplate.substitute(url=imageUrl)) #Adds new td object based on template string
                    counter += 1

            self.gridHTML += "</tr></table>"
            return Markup(self.gridHTML)
        
        #---------------#
        #Builds the HTML syntax to draw the game grid - makes the grid easily expandable + avoid typing repetitive HTML code
        def buildEditableGrid(self,gridX,gridY):
        #Imports modules 
            #Local Constants
            CLASS_NAME = "gridSquare" #The name of the class that all td objects will share

            #Grid variable will accumulate the HTML table
            self.grid = "<table id=\"tbl_CoordinatesGrid\">"

            self.columns = [" "] #The lables on the X-Axis
            for l in range(gridX):
                self.columns.append(chr(65+l)) #Generate X axis labels using ASCII character integers
            self.rows = list(range(1,gridY+1)) #The Y-axis lables

            #Adds heading row
            self.grid += "<tr id=\"trw_gridHeading\">"
            for l in self.columns:
                self.grid += f"<td class=\"{CLASS_NAME}\" dynamic html=\"tdt_gridLabelCol{l}\">{l}</td>"
            self.grid += "</tr>"

            #Adds rest of grid
            for row in self.rows:
                self.grid += "<tr>"
                for col in self.columns:
                    if col == " ":
                        self.grid += f"<td class=\"{CLASS_NAME}\" id=\"tdt_gridLabelCol{row}\">{row}</td>"
                    else:
                        self.grid += f"<td class=\"{CLASS_NAME} dragReceptacle\" id=\"tdt_grid{col}{row}\"></td>"
                self.grid += "</tr>"

            self.grid += "</table>"

            #Return finished grid as Markdown and not plain text
            return Markup(self.grid)

    #---------------#
    #Returns the users that are currently part of a game 
    def getActiveUsersDictionary(self, gameID,userTBL):
        self.allUsers = userTBL.query.filter(userTBL.userGameID==gameID,userTBL.userGrid!=None).all()
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
        #Simple length check (seconds javascript check)
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
    #Checks that the provided game ID exists and is open to join
    def gameIDValidate(self,gameID,gameTBL,usersTBL=None,userID=None):
        MAX_USERS = 80
        try:
            self.matchingGame = gameTBL.query.filter(gameTBL.gameID==int(gameID)).first()
            if self.matchingGame != None: #Check game exists
                if self.matchingGame.isOpen or validators().isFinished(gameID,gameTBL): #Check if game is open or finished - in either case anyone is allowed in
                    if usersTBL != None: #Check user info is provided
                        gamePlayers = usersTBL.query.filter(usersTBL.userGameID==gameID).all() #Check game isn't full
                        if len(gamePlayers) < MAX_USERS:
                            return True
                    else:
                        return True
                else: # If game isn't open
                    userLine = usersTBL.query.filter(usersTBL.userSID==userID).first()
                    if userLine != None: #Check user info is provided
                        if int(userLine.userGameID) == int(gameID): #Check the user is connected to a game already
                            return True
            return False
        except TypeError or AttributeError: #Handles if a null or invalid gameID is submitted
            return False
    
    #---------------#
    #Checks if a given user SID is the host of a game
    def isHost(self,SID,gameID,gameTBL):
        self.qurRes = gameTBL.query.filter(gameTBL.hostSID==SID,gameTBL.gameID==gameID).all()
        if self.qurRes:
            return True
        else:
            return False
    
    #---------------#
    #Check if a user clarifies as being online or not
    def isOnline(self,userID,usersTBL):
        if usersTBL.query.get(userID).socketioSID != None:
            return True
        else:
            return False

    #---------------#
    #Check if a given game is over and that the results have been saved
    def isFinished(self, gameID,gamesTBL):
        if gamesTBL.query.get(gameID).resultsScores != None:
            return True
        
        return False

    #---------------#
    #Decorator to validate that a user is allowed to visit a page
    def pageControlValidate(usersTBL,gamesTBL):
        def decorator(func):
            @wraps(func)
            def function_wrapper(*args, **kwargs):
                try:
                    userSID = request.cookies.get("SID") #Loads from client cookies
                    gameID = request.args.get("gid") #Loads from URL bar
                    userLine = usersTBL.query.filter(usersTBL.userSID==userSID,usersTBL.userGameID==gameID).first()
                    if validators().gameIDValidate(gameID,gamesTBL,usersTBL,userSID):
                        if userLine == None: #If the gameIDValidator has allowed a non type sid then allow it
                            return func(*args, **kwargs)
                        elif userLine.userGameID == int(gameID):
                            return func(*args, **kwargs)
                    
                    return redirect("/error?code=GAMEINVALID")
                except TypeError:
                    return redirect("/error?code=GAMEINVALID")
                except AttributeError:
                    return redirect("/error?code=INVALIDSID")
            return function_wrapper
        return decorator

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

        #Substitute numbers in to expression to replace variables in order to make latter replacement easier (e.g. {vCash} to 0)
        expression = expression.format(vCash=self.vCash,vBank=self.vBank,pCash=self.pCash,pBank=self.pBank)

        #Calculate each part of the formula individually (e.g. self.pCah=300+1000 is one)
        for e in expression.split(":"):
            exec(e) #Executes the string expression
        
        return self.vCash, self.vBank, self.pCash, self.pBank
    
    #---------------#
    #Get the error message from a given code
    def getERROR(self,code):
        ERRORS = { #Available error messages and their corresponding code
            "GAMEINVALID" : "The game page you requested is unavailable. <br> This may be because the game does not exist or is already in progress.",
            "NOSID" : "Your user has not been assigned an SID. Join a game or create one to get a SID cookie.",
            "GAMEONGOING" : "You have attempted to visit the results page however the game has not yet finished",
            "INVALIDSID" : "The SID value provided by your client is not permitted to access this game information. This may be because no SID was provided"
        }
        try:
            self.message = ERRORS[code.upper()] + f"<br><b>ERROR CODE : {code.upper()}</b>" #Append code to message
        except:
            self.message = "Error code not found!"
        return Markup(self.message)

#=========================================================#
#^ Gameplay Events ^#
class events:
    #---------------#
    #Ends the game just before the progression to the results page
    def gameEnd(self, gameID,gameTBL,usersTBL,gameDB):
        DELETION_DELAY = 1000 #Time in seconds to wait before an old game is deleted from the database
        self.allUsers = usersTBL.query.filter(usersTBL.userGameID==int(gameID)).all()
        self.gameOBJ = gameTBL.query.get(int(gameID))

        #collects users final cash amounts and sorts them in a dictionary
        userscore = {}
        for User in self.allUsers:
            userscore[User.userNickname] = User.userCash + User.userBank

        self.gameOBJ.resultsScores = json.dumps(userscore)
        self.gameOBJ.deletionTime = int(time.time()) + DELETION_DELAY
        usersTBL.query.filter(usersTBL.userGameID==int(gameID)).delete() #Delete all users relating to that game from the database

        gameDB.session.commit()

#=========================================================#
#^ Gampeplay Functions ^#
class functions:
    #---------------#
    #Runs when an action has been completed and checks whether a round has completed or not
    def actionComplete(self, gameOBJ):
        gameOBJ.remainingActions -= 1
        if gameOBJ.remainingActions == 0:
            return True

#=========================================================#
#^ Information Fabricators ^#
class information:
    #---------------#
    #Get information about the number of currently active games
    def calcActiveGames(self,gamesTBL):
        self.numActiveGames = 2
        return self.numActiveGames

    def getTotalGames(self):
        self.totalgamesfile = open("totalGames.txt","r")
        return self.totalgamesfile.read()

    def incrementTotalGames(self):
        totalgamesfile = open("totalGames.txt","r")
        totalgamescount = totalgamesfile.read()
        totalgamescount = int(totalgamescount) 
        totalgamescount += 1
        totalgamesfile.close()
        totalgamesfile = open("totalGames.txt","w")
        totalgamesfile.write(str(totalgamescount))
        

#=========================================================#
#^ Loggers ^#
class loggers:
    #---------------#
    #Defines how data should be logged for a user disconnect
    def userDisconnect(self, userNickname):
        LOG_FORMAT = "🚪 {user} has left the game 🚪"

        self.finalEntry = LOG_FORMAT.format(user=userNickname)

        return self.finalEntry
    #---------------#
    #Defines how data should be logged for a user connection
    def userConnect(self, userNickname):
        LOG_FORMAT = "👋 {user} joined the game 👋"

        self.finalEntry = LOG_FORMAT.format(user=userNickname)
        return self.finalEntry