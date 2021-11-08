#---------------------------------------------------------------------#
# File: https://github.com/A-Level-Personal-Code-Collab/PirateGame/gameplay.py
# Project: https://github.com/A-Level-Personal-Code-Collab/PirateGame
# Created Date: Monday, October 25th 2021, 7:27:52 pm
# Description: All of the functionality that deals with core gameplay functions
# Author: Will Hall
# Copyright (c) 2021 Lime Parallelogram
# -----
# Last Modified: Mon Nov 08 2021
# Modified By: Adam O'Neill
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
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
from os import link
import time
from flask import Markup, request, redirect
from string import Template
import random

import database
import json
from functools import wraps

usersTBL = database.activeUsers
gamesTBL = database.activeGames
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
    def getActiveUsersDictionary(self, gameID):
        self.allUsers = database.get_players(gameID)
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
    def generate_SID(self):
        ID_MAX = 99999999
        self.userSID = random.randint(0,ID_MAX)
        while database.get_user(self.userSID) != None: #Check if chosen SID already exists and keep regerating until it doesn't
            self.userSID = random.randint(0,ID_MAX)
        
        return self.userSID
    
    #---------------#
    #Generate random game ID guaranteed to be unique
    def generate_gameID(self):
        ID_MAX = 99999999
        self.gameID = random.randint(0,ID_MAX)
        while database.get_game(self.gameID) != None:
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
    def gameIDValidate(self,gameID,userID=None):
        MAX_USERS = 80
        try:
            self.matchingGame = database.get_game(gameID)
            if self.matchingGame != None: #Check game exists
                if self.matchingGame.is_open or validators().isFinished(gameID): #Check if game is open or finished - in either case anyone is allowed in
                    if usersTBL != None: #Check user info is provided
                        gamePlayers = database.get_players(gameID) #Check game isn't full
                        if len(gamePlayers) < MAX_USERS:
                            return True
                    else:
                        return True
                else: # If game isn't open
                    userLine = database.get_user(userID)
                    if userLine != None: #Check user info is provided
                        if userLine.user_game_id == int(gameID): #Check the user is connected to a game already
                            return True
            return False
        except TypeError or AttributeError: #Handles if a null or invalid gameID is submitted
            return False
    
    #---------------#
    #Checks if a given user SID is the host of a game
    def isHost(self,SID,gameID):
        self.qurRes = database.get_game(gameID)
        if self.qurRes:
            if self.qurRes.host_id == int(SID):
                return True

        return False
    
    #---------------#
    #Check if a user clarifies as being online or not
    def isOnline(self,userID):
        if database.get_user(userID).socketio_id != None:
            return True
        else:
            return False

    #---------------#
    #Check if a given game is over and that the results have been saved
    def isFinished(self, gameID):
        if database.get_game(gameID).results_json != None:
            return True
        
        return False

    #---------------#
    #Decorator to validate that a user is allowed to visit a page
    def pageControlValidate():
        def decorator(func):
            @wraps(func)
            def function_wrapper(*args, **kwargs):
                try:
                    userSID = request.cookies.get("SID") #Loads from client cookies
                    gameID = request.args.get("gid") #Loads from URL bar
                    userLine = database.get_user(userSID)
                    if validators().gameIDValidate(gameID,userSID):
                        if userLine == None: #If the gameIDValidator has allowed a non type sid then allow it
                            return func(*args, **kwargs)
                        elif userLine.user_game_id == int(gameID):
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

    def convertTxtToHtml(file):
        title = file.readline().strip()#works
        body = file.readlines()
        htmltext = ""
        htmltext = htmltext + '<div class="header">' + title + "</div>"
        htmltext = htmltext + "<div class=notes_container>"
        for line in body:
            # check if it starts with a ~ # or -
            if line[0] == "^": # checks if header
                htmltext = htmltext + "<br>"
                htmltext = htmltext + "<h3>" + line[1:] + "</h3>" # [1:] is used to slice the first letter off

            elif line[0] == "~": # description
                htmltext = htmltext + "<p>" + line[1:] + "</p>"

            elif line[0] == "-": # Bullet point
                htmltext = htmltext + "<li>" + line[1:] + "</li>"

            if "#" in line: # github issue
                hash = line.find("#")
                linkstr = line[hash+1:]
                for character in linkstr:
                    if character.isdigit() != True:
                        notint = linkstr.find(character)
                        break
                issueref = linkstr[:notint]


                htmltext = htmltext.replace("#"+issueref , f"<a href=https://github.com/A-Level-Personal-Code-Collab/PirateGame/issues/{issueref}>#{issueref}</a>")

        htmltext = htmltext + "</div>" 
        
        return Markup(htmltext)
    
    #---------------#
    #Get the error message from a given code
    def getERROR(self,code):
        ERRORS = { #Available error messages and their corresponding code
            "GAMEINVALID" : "The game page you requested is unavailable. <br> This may be because the game does not exist or is already in progress.",
            "NOSID" : "Your user has not been assigned an SID. Join a game or create one to get a SID cookie.",
            "GAMEONGOING" : "You have attempted to visit the results page however the game has not yet finished",
            "INVALIDSID" : "The SID value provided by your client is not permitted to access this game information. This may be because no SID was provided",
            "VERSIONINVALID" : "This version's patch notes dont exist you muppet!"
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
    def gameEnd(self, gameID):
        DELETION_DELAY = 1000 #Time in seconds to wait before an old game is deleted from the database
        self.allUsers = database.get_players(gameID)
        self.gameOBJ = database.get_game(gameID)

        #collects users final cash amounts and sorts them in a dictionary
        userscore = {}
        for User in self.allUsers:
            userscore[User.user_nickname] = User.user_cash + User.user_bank

        self.gameOBJ.results_json = json.dumps(userscore)
        self.gameOBJ.deletion_time = int(time.time()) + DELETION_DELAY
        database.delete_players(gameID) #Delete all users relating to that game from the database

        database.gameDB.commit()

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
#^ Information Fabricators ^#
class information:
    #---------------#
    #Get information about the number of currently active games
    def calcActiveGames(self):
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