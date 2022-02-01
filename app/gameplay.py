#---------------------------------------------------------------------#
# File: https://github.com/A-Level-Personal-Code-Collab/PirateGame/gameplay.py
# Project: https://github.com/A-Level-Personal-Code-Collab/PirateGame
# Created Date: Monday, October 25th 2021, 7:27:52 pm
# Description: All of the functionality that deals with core gameplay functions
# Author: Will Hall
# Copyright (c) 2021 Lime Parallelogram
# -----
# Last Modified: Tue Feb 01 2022
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2022-02-01	WH	Added release date information to patch notes files
# 2022-02-01	WH	Fixed title now sent with patch notes text
# 2022-02-01	WH	Patch notes processor now has image facility
# 2022-02-01	WH	Patch notes processor now handles markdown formatted text
# 2022-02-01	WH	Created class for patch notes processor
# 2021-11-19	WH	Modified all functions that use the database to accept a session parameter
# 2021-11-15	WH	Results now stored in database as JSON object
# 2021-11-12	WH	Added functionality to extract patch notes overview from files
# 2021-11-08	AO	Added the text to html builder
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
from io import TextIOBase
import os
import time
from flask import Markup, request, redirect
import markdown
import re
from string import Template
import random

import database
import json
from functools import wraps

usersTBL = database.activeUsers
gamesTBL = database.activeGames

#---------------#
GAME_VERSION = "1.1.0"

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
    def getActiveUsersDictionary(self, session, gameID):
        self.allUsers = database.get_players(session,gameID)
        self.SIDNick = {} #Creates dictionary with key of SID and value of nickname
        for user in self.allUsers:
            self.SIDNick[user.user_id] = user.user_nickname

        return self.SIDNick
    
    #---------------#
    #Generates a random order for the gameplay grid
    def generate_playOrder(self,gridArea):
        self.playOrder = list(map(str,range(0,gridArea)))
        random.shuffle(self.playOrder)
        self.csvString = ",".join(self.playOrder)
        return self.csvString

    #---------------#
    #Generate a user sid that is guaranteed to be unique
    def generate_SID(self,session):
        ID_MAX = 99999999
        self.userSID = random.randint(0,ID_MAX)
        while database.get_user(session,self.userSID) != None: #Check if chosen SID already exists and keep regerating until it doesn't
            self.userSID = random.randint(0,ID_MAX)
        
        return self.userSID
    
    #---------------#
    #Generate random game ID guaranteed to be unique
    def generate_gameID(self,session):
        ID_MAX = 99999999
        self.gameID = random.randint(0,ID_MAX)
        while database.get_game(session,self.gameID) != None:
            self.gameID = random.randint(0,ID_MAX)
            
        return self.gameID


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
    def gameIDValidate(self,session,gameID,userID=None):
        MAX_USERS = 80
        try:
            self.matchingGame = database.get_game(session,gameID)
            if self.matchingGame != None: #Check game exists
                if self.matchingGame.is_open or validators().isFinished(session,gameID): #Check if game is open or finished - in either case anyone is allowed in
                    gamePlayers = database.get_players(session,gameID) #Check game isn't full
                    if len(gamePlayers) < MAX_USERS:
                        return True
                else: # If game isn't open
                    userLine = database.get_user(session,userID)
                    if userLine != None: #Check user info is provided
                        if userLine.user_game_id == int(gameID): #Check the user is connected to a game already
                            return True
            return False
        except TypeError or AttributeError: #Handles if a null or invalid gameID is submitted
            return False
    
    #---------------#
    #Checks if a given user SID is the host of a game
    def isHost(self,session,SID,gameID):
        self.qurRes = database.get_game(session,gameID)
        if self.qurRes:
            if self.qurRes.host_id == int(SID):
                return True

        return False
    
    #---------------#
    #Check if a user clarifies as being online or not
    def isOnline(self,session,userID):
        if database.get_user(session,userID).socketio_id != None:
            return True
        else:
            return False

    #---------------#
    #Check if a given game is over and that the results have been saved
    def isFinished(self, session, gameID):
        if database.get_game(session,gameID).results_json != None:
            return True
        
        return False

    #---------------#
    #Decorator to validate that a user is allowed to visit a page
    def pageControlValidate(func):
        @wraps(func)
        def function_wrapper(session, *args, **kwargs):
            try:
                userSID = request.cookies.get("SID") #Loads from client cookies
                gameID = request.args.get("gid") #Loads from URL bar
                if validators().gameIDValidate(session,gameID,userSID):
                    return func(session, *args, **kwargs)
                    
                return redirect("/error?code=GAMEINVALID")
            except TypeError:
                return redirect("/error?code=GAMEINVALID")
            except AttributeError:
                return redirect("/error?code=INVALIDSID")
        return function_wrapper

#=========================================================#
#^ Parsing system ^#
class parsers:
    #---------------#
    #Takes the money expression and calculates actual values with it
    def parse_money(self,expression,victim,perpetrator=None):
        self.vCash = victim.user_cash
        self.vBank = victim.user_bank
        self.pCash = perpetrator.user_cash if perpetrator else 0
        self.pBank = perpetrator.user_bank if perpetrator else 0

        #Substitute numbers in to expression to replace variables in order to make latter replacement easier (e.g. {vCash} to 0)
        expression = expression.format(vCash=self.vCash,vBank=self.vBank,pCash=self.pCash,pBank=self.pBank)

        #Calculate each part of the formula individually (e.g. self.pCah=300+1000 is one)
        for e in expression.split(":"):
            exec(e) #Executes the string expression
        
        return self.vCash, self.vBank, self.pCash, self.pBank
    
    #---------------#
    # Handles patch notes for a specified version
    class patchNotes:
        def __init__(self,version=GAME_VERSION): #Reads patch notes file (Default version = current version)
            self.gamefile = "static/patchnotes/" + version.replace(".","-") + ".md"
            self.releaseURL = "/about/patch_notes/release/" + version.replace(".","-")

            with open(self.gamefile, 'r') as file:
                self.releaseTitle = file.readline()[3:]
                self.releaseDate = file.readline()[5:]
                self.releaseDate = self.releaseDate if "Release Date" in self.releaseDate else "" #Validate release date line
                self.filedat = "##### " + self.releaseDate + file.read()

        #---------------#
        #Converts patch notes text files to HTML pages
        def convertTxtToHtml(self):
            #Locate Issue numbers and add their links to markdown
            searchText = self.filedat
            allIssues = [m.start() for m in re.finditer('Issue #', self.filedat)] #Find all instances of issues in the page

            #Check all issues and fix them
            for issue in allIssues:
                issueText = searchText[issue:issue+11]
                issueNumber = issueText[-4:]
                while not issueNumber[len(issueNumber)-1].isdigit():
                    issueNumber = issueNumber[:-1]
                    issueText = issueText [:-1]

                self.filedat = self.filedat.replace(issueText,f"[{issueText}](https://github.com/A-Level-Personal-Code-Collab/PirateGame/issues/{issueNumber})")               

            #Convert modified markdown to issue page
            htmlText = markdown.markdown(self.filedat)
            return Markup(htmlText)

        #---------------#
        #Extract the overview information from the patch notes file
        def getReleaseOverview(self):
            self.overviewStart = self.filedat.find("## Overview") + 12
            self.overviewEnd = self.filedat[self.overviewStart:].find("##") - 1

            return self.filedat[self.overviewStart:self.overviewEnd+self.overviewStart]
    
        #---------------#
        #Extract version illustration image
        def getReleaseIllustration(self):
            self.imageStart = self.filedat.find("![Release Illustration](") + 24
            self.imageEnd = self.filedat[self.imageStart:].find(")")

            return self.filedat[self.imageStart:self.imageEnd+self.imageStart]

        #---------------#
        # Gets a compiled JSON with information about the release for the home page
        def getReleaseJSON(self):
            self.releaseDictionary = {"releaseTitle": self.releaseTitle, "releaseOverview": self.getReleaseOverview(), "releaseIllustration": self.getReleaseIllustration(), "releaseUrl": self.releaseURL}
            return self.releaseDictionary

        #---------------#
        #Returns the release title to
        def getReleaseTitle(self):
            return self.releaseTitle

        #---------------#
        #Returns the release title to
        def getReleaseDate(self):
            return self.releaseDate

    #---------------#
    #Returns a list of all version information to JINJA
    def getVersions():
        versions = []
        for version in os.listdir("static/patchnotes"):
            versionNumber = version[:-3].replace("-",".")
            versionObject = parsers.patchNotes(versionNumber)

            if versionNumber != "key": #Ignore key.md file
                versions.append({"versionId": versionNumber.replace(".",""),"versionUrl": "/about/patch_notes/release/"+version[:-3], "versionName": versionObject.getReleaseTitle(), "versionDate": versionObject.getReleaseDate(), "versionIllustration": versionObject.getReleaseIllustration(), "versionOverview": versionObject.getReleaseOverview()})
        
        versions.sort(key= lambda item: item.get("versionId"))
        versions.reverse()
        return versions

    #---------------#
    #Get the error message from a given code
    def getERROR(self,code):
        ERRORS = { #Available error messages and their corresponding code
            "GAMEINVALID" : "The game page you requested is unavailable. <br> This may be because the game does not exist or is already in progress.",
            "NOSID" : "Your user has not been assigned an SID. Join a game or create one to get a SID cookie.",
            "GAMEONGOING" : "You have attempted to visit the results page however the game has not yet finished",
            "INVALIDSID" : "The SID value provided by your client is not permitted to access this game information. This may be because no SID was provided",
            "VERSIONINVALID" : "This version's patch notes don't exist you muppet!"
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
    def gameEnd(self, session, gameID):
        DELETION_DELAY = 1000 #Time in seconds to wait before an old game is deleted from the database
        self.allUsers = database.get_players(session, gameID)
        self.gameOBJ = database.get_game(session, gameID)

        #collects users final cash amounts and sorts them in a dictionary
        userscore = {}
        for User in self.allUsers:
            userscore[User.user_nickname] = User.user_cash + User.user_bank

        self.gameOBJ.results_json = userscore
        self.gameOBJ.deletion_time = int(time.time()) + DELETION_DELAY
        database.delete_players(session, gameID) #Delete all users relating to that game from the database

        session.commit()

#=========================================================#
#^ Gampeplay Functions ^#
class functions:
    #---------------#
    #Runs when an action has been completed and checks whether a round has completed or not
    def actionComplete(self,gameLine):
        gameLine.round_remaining_actions -= 1
        if gameLine.round_remaining_actions == 0:
            return True


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