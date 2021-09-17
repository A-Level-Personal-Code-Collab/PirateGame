#---------------------------------------------------------------------#
# File: A-Level-Personal-Code-Collab/PirateGame/flask_main.py
# Project: A-Level-Personal-Code-Collab/PirateGame
# Created Date: Thursday, July 8th 2021, 4:38:56 pm
# Description: Main flask webserver root.
# Author: Will Hall
# Copyright (c) 2021 Lime Parallelogram
# -----
# Last Modified: Fri Sep 17 2021
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2021-09-17	WH	tandardised refrence to item names so, for example, kill is refrenced as itmKill everywhere
# 2021-09-17	WH	Changed perpetrate_<action> events to notify events as this makes more sense
# 2021-09-17	WH	Major overhaul of action definitions as they are now in data classes 
# 2021-09-02	WH	Now handles Kill, Gift, Swap and Steal
# 2021-09-02	WH	Added handling for special action declaration
# 2021-08-28	WH	Added handling for Money, Bank and Bomb items being selected
# 2021-08-28	WH	Added method to respond to the pushing of the NEXT-ROUND button
# 2021-08-28	WH	Added function to generate the squence of squares
# 2021-08-24	WH	Playing game draw-grid function now operates as inteded
# 2021-08-23	WH	Began work on online play draw grid function
# 2021-08-19	WH	Added pop-upto warn users if they are already signed in in another tab
# 2021-08-05	WH	Converted application to use sqlite in-memory database to track active games
# 2021-08-05	WH	Grid is addded to user database when sheet is submitted and user is redirected
# 2021-08-05	WH	Adds user to active users database when they join a game from the join game screen
# 2021-08-05	WH	Create system to query database when join game requested
# 2021-08-05	WH	Create link to MySQL database
# 2021-08-02	WH	Added nickname validator routine which, if sucessful, redirects user to /sheet_builder
# 2021-08-02	WH	Converted application to socketio application
# 2021-07-09	WH	Added code to generate and serve basic playing grid
# 2021-07-08	WH	Added very basic flask server structure
#---------------------------------------------------------------------#
from re import sub
import re
from flask import Flask, render_template, Markup, send_file, request
from flask_socketio import SocketIO, join_room, rooms, send, emit
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
import json
import random
from string import Template

from werkzeug.wrappers import response

app = Flask(__name__)
app.config['SECRET_KEY'] = '0nOxRU2ipDewLH1d'
socketio = SocketIO(app)

#---------------#
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

gameDB = SQLAlchemy(app)

#=========================================================#
#^ Database table models ^#in
#(these are required by SQL alchemy to interact with database so the variable names and info must correspond with your database)
#---------------#
#The table that stores a log of all currently active games
class activeGame(gameDB.Model):
    __tablename__ = 'activeGames'
    gameID = gameDB.Column(gameDB.Integer, primary_key=True)
    hostSID = gameDB.Column(gameDB.Integer)
    gridSettings = gameDB.Column(gameDB.String(100))
    itemSettings = gameDB.Column(gameDB.String(100))
    currentRound = gameDB.Column(gameDB.Integer)
    squareOrder = gameDB.Column(gameDB.String(300))

#---------------#
#The table that stores a log of all active users and their grids
class activeUsers(gameDB.Model):
    __tablename__ = 'activeUsers'
    userNickname = gameDB.Column(gameDB.String(15))
    userSID = gameDB.Column(gameDB.Integer, primary_key=True)
    socketioSID = gameDB.Column(gameDB.String(100))
    userGameID = gameDB.Column(gameDB.Integer)
    userGrid = gameDB.Column(gameDB.String(9999))
    isHost = gameDB.Column(gameDB.Boolean, default=False)
    userCash = gameDB.Column(gameDB.Integer, default=0)
    userCashPending = gameDB.Column(gameDB.Integer, default=-1)
    userBank = gameDB.Column(gameDB.Integer, default=0)
    userBankPending = gameDB.Column(gameDB.Integer, default=-1)
    hasShield = gameDB.Column(gameDB.Boolean, default=False)
    hasMirror = gameDB.Column(gameDB.Boolean, default=False)


#=========================================================#
#^ Data classes to define the action's model ^#
class actionItem():
    '''The base class for any action obejct that is created'''
    ACTION_EMOJI = "❔"
    ACTION_IDENTIFIER = "itmUNDEF"
    LOG_MESSAGE = "{emoji} {perpetrator} did undefined action on {victim} {emoji}"
    CAN_MIRROR = True
    CAN_SHIELD = True

    def get_log(self, perpetrator, victim):
        return self.LOG_MESSAGE.format(emoji=self.ACTION_EMOJI,perpetrator=perpetrator,victim=victim)

    def identify(self,test):
        if test == self.ACTION_IDENTIFIER:
            return True
        else:
            return False

    def get_itemNotify(self):
        return "itm_available", {"type": self.ACTION_IDENTIFIER}

#=========================================================#
#^ Action Data classes ^#
class itmKill(actionItem):
    '''Class for kill item (victim's money is set to 0)'''
    IMAGE_LOCATION = "../static/img/kill.png"
    ACTION_EMOJI = "⚔"
    ACTION_IDENTIFIER = "itmKill"
    LOG_MESSAGE = "{emoji} {perpetrator} killed {victim} {emoji}"
    CAN_MIRROR = True
    CAN_SHIELD = True
    TARGETTED = True

    def calculate_money(self, vCash, pCash, vBank, pBank):
        return 0, pCash, vBank, pBank

#---------------#
class itmSteal(actionItem):
    '''Class for steal item (victim's money is given to perpetrator)'''
    IMAGE_LOCATION = "../static/img/steal.png"
    ACTION_EMOJI = "💰"
    ACTION_IDENTIFIER = "itmSteal"
    LOG_MESSAGE = "{emoji} {perpetrator} has stolen from {victim} {emoji}"
    CAN_MIRROR = True
    CAN_SHIELD = True
    TARGETTED = True

    def calculate_money(self, vCash, pCash, vBank, pBank):
        return 0, pCash+vCash, vBank, pBank

#---------------#
class itmGift(actionItem):
    '''Class for gift item (victim recieves 1000M from nowhere)'''
    IMAGE_LOCATION = "../static/img/gift.png"
    ACTION_EMOJI = "🎁"
    ACTION_IDENTIFIER = "itmGift"
    LOG_MESSAGE = "{emoji} {perpetrator} gifted {victim} {emoji}"
    CAN_MIRROR = True
    CAN_SHIELD = True
    TARGETTED = True

    def calculate_money(self, vCash, pCash, vBank, pBank):
        return vCash+1000, pCash, vBank, pBank

#---------------#
class itmSwap(actionItem):
    '''Class for swap item (perpetrator and victim swap cash)'''
    IMAGE_LOCATION = "../static/img/swap.png"
    ACTION_EMOJI = "🤝"
    ACTION_IDENTIFIER = "itmSwap"
    LOG_MESSAGE = "{emoji} {perpetrator} has swapped with {victim} {emoji}"
    CAN_MIRROR = False
    CAN_SHIELD = True
    TARGETTED = True

    def calculate_money(self, vCash, pCash, vBank, pBank):
        return pCash, vCash, vBank, pBank

#---------------#
class itmBomb(actionItem):
    '''Class for bomb item'''
    IMAGE_LOCATION = "../static/img/bomb.png"
    ACTION_EMOJI = "💣"
    ACTION_IDENTIFIER = "itmBomb"
    LOG_MESSAGE = ""
    CAN_MIRROR = False
    CAN_SHIELD = False
    TARGETTED = False

    def calculate_money(self, vCash, vBank):
        return 0, vBank

#---------------#
class itmBank(actionItem):
    '''Class for bank item'''
    IMAGE_LOCATION = "../static/img/bank.png"
    ACTION_EMOJI = "🏦"
    ACTION_IDENTIFIER = "itmBank"
    LOG_MESSAGE = ""
    CAN_MIRROR = False
    CAN_SHIELD = False
    TARGETTED = False

    def calculate_money(self, vCash, vBank):
        return 0, vBank+vCash

#---------------#
class itmMirror:
    '''Class for mirror modifier item'''
    IMAGE_LOCATION = "../static/img/mirror.png"
    ACTION_EMOJI = "🪞"
    ACTION_IDENTIFIER = "itmMirror"
    LOG_MESSAGE = "{emoji} {victim} mirrored that {emoji}"

#---------------#
class itmShield:
    '''Class for shield modifier item'''
    IMAGE_LOCATION = "../static/img/shield.png"
    ACTION_EMOJI = "🛡"
    ACTION_IDENTIFIER = "itmShield"
    LOG_MESSAGE = "{emoji} {victim} blocked that {emoji}"

#=========================================================#
#^ Money Data Class ^#
class money:
    '''Class that defines the behavior of money items'''
    IMAGE_LOCATION = "../static/img/M{denom}.png"
    IDENTIFIER = "M{denom}"
    DENOMINATION = 200

    def __init__(self, denomination):
        self.DENOMINATION = denomination
        self.IDENTIFIER = self.IDENTIFIER.format(denom=str(denomination))
        self.IMAGE_LOCATION = self.IMAGE_LOCATION.format(denom=str(denomination))

    def identify(self,value):
        if value[0] == "M":
            return True
        else:
            return False

    def cash_update(self,old_cash):
        return old_cash + self.DENOMINATION


#=========================================================#
#^ Slave subs ^#
#---------------#
#Builds the HTML syntax to draw the game grid - makes the grid easily exapandable + avoid typing repetative HTML code
def buildGrid(gridX,gridY):
#Imports modules 
    #Local Constants
    CLASS_NAME = "gridSquare" #The name of the class that all td objects will share

    #Grid variable will acumulate the HTML table
    grid = "<table id=\"tbl_CoordinatesGrid\">"

    collums = [" "] #The lables on the X-Axis
    for l in range(gridX):
        collums.append(chr(65+l)) #Generate X axis labels using ASCII character integers
    rows = list(range(1,gridY+1)) #The Y-axis lables

    #Adds heading row
    grid += "<tr id=\"trw_gridHeading\">"
    for l in collums:
        grid += f"<td class=\"{CLASS_NAME}\" idng dynamic html=\"tdt_gridLabelCol{l}\">{l}</td>"
    grid += "</tr>"

    #Adds rest of grid
    for row in rows:
        grid += "<tr>"
        for col in collums:
            if col == " ":
                grid += f"<td class=\"{CLASS_NAME}\" id=\"tdt_gridLabelCol{row}\">{row}</td>"
            else:
                grid += f"<td class=\"{CLASS_NAME} dragReceptical\" id=\"tdt_grid{col}{row}\"></td>"
        grid += "</tr>"

    grid += "</table>"

    #Return finnished grid as Markdown and not plain text
    return Markup(grid)

#---------------#
#Checks that the inputted nickname is valied
def nicknameValidate(nickname):
    NICKNAME_MAX_LEN = 15
    NICKNAME_MIN_LEN = 3
    BLACKLIST_FILE = "static/nickname-word-blacklist.csv"

    nickname = nickname.lower()
    #---------------#
    #Simple length check (secconds javascript check)
    nicknameLen = len(nickname)
    if nicknameLen > NICKNAME_MAX_LEN or nicknameLen < NICKNAME_MIN_LEN:
        return False
    
    #---------------#
    #Checks banned words lists
    blacklist = open(BLACKLIST_FILE, 'r')
    rejectWords = blacklist.read().split(",")
    blacklist.close()

    #Loop through banned words and check them all
    for word in rejectWords:
        wordLen = len(word)
        if not wordLen > nicknameLen: #If word in question is longer than nickname then ignore it
            if word == nickname: #Check if word _is_ nickname
                return False
            numSubstrings = nicknameLen - wordLen + 1 #Calculated how many possible substrings there are of any given word
            for i in range(numSubstrings): #Finds and checks all substrings of nickname to the length of the check word
                substring = nickname[i:i+wordLen]
                if substring == word:
                    return False
    return True

#---------------#
#Checks that the provided game ID exists
def gameIDValidate(gameID):
    if activeGame.query.get(int(gameID)):
        return True
    else:
        return False

#---------------#
#Returns the users that are currently part of a game 
def getActiveUsersList(gameID):
    allUsers = activeUsers.query.filter(activeUsers.userGameID==gameID,activeUsers.userGrid!=None).all()
    listElement = "<list class=\"names_list\">"
    for user in allUsers:
        listElement += f"<li>{user.userNickname}</li>"
    listElement += "</list>"
    return listElement

#---------------#
#Checks if a given user SID is the host of a game
def isHost(SID,gameID):
    qurRes = activeGame.query.filter(activeGame.hostSID==SID,activeGame.gameID==gameID).all()
    print(qurRes)
    if qurRes:
        return True
    else:
        return False

#---------------#
#Draws the grid but this time in the form of an uneditable play board
def drawGameplayGrid(xSize,gridSerial):
    gridList = gridSerial.split(",")
    gridHTML = '<table id="tbl_playGrid">'
    gridSquareHTMLTemplate = Template('<td id="$id" class="gridSquare">$inner</td>') #Creates template strings for the individual HTML td elements
    gridImageTemplate = Template('<img class="gridItems" src="$url"/>') #Template string for the images that go inside the td elements
    IMAGE_URLS = { #Defines the locations of the images ascoiated with the following items
        "M5000" : money(5000).IMAGE_LOCATION,
        "M1000" : money(1000).IMAGE_LOCATION,
        "M500" : money(500).IMAGE_LOCATION,
        "M200" : money(200).IMAGE_LOCATION,
        "itmKill" : itmKill.IMAGE_LOCATION,
        "itmSwap" : itmSwap.IMAGE_LOCATION,
        "itmSteal" : itmSteal.IMAGE_LOCATION,
        "itmGift" : itmGift.IMAGE_LOCATION,
        "itmBank" : itmBank.IMAGE_LOCATION,
        "itmBomb" : itmBomb.IMAGE_LOCATION,
        "itmShield" : itmShield.IMAGE_LOCATION,
        "itmMirror" : itmMirror.IMAGE_LOCATION
    }

    #Calculated the y-size as only the X was provided
    if len(gridList) % xSize != 0:
        raise "GRID DIMENSION ERROR"
    ySize = int(len(gridList) / xSize)

    colLabels = [""] + list(map(chr, range(65,65+xSize))) #Creates a list of collum lables using capital letters
    gridHTML += "<tr>"

    #Creates the collum lables row
    for col in colLabels:
        gridHTML += gridSquareHTMLTemplate.substitute(id=None,inner=col)

    #Runs through all other rows
    counter = 0 #Allows for IDs to be named serially
    for y in range(ySize):
        gridHTML += "</tr><tr>"
        gridHTML += gridSquareHTMLTemplate.substitute(id=None, inner=str(y)) #Adds the row lable
        for x in range(xSize): #Runs through all other collums in that row
            itemName = gridList[(x+y*xSize)] #Loads the item name from serial list corresponding to the coordinate in question
            imageUrl = IMAGE_URLS[itemName]
            gridHTML += gridSquareHTMLTemplate.substitute(id=f"square{counter}",inner=gridImageTemplate.substitute(url=imageUrl)) #Adds new td object based on template string
            counter += 1

    gridHTML += "</tr></table>"
    return Markup(gridHTML)

#=========================================================#
#^ Gameplay Routines Class ^#
class gameplay:
    #---------------#
    #Generates a random order for the gameplay grid
    def generate_playOrder(self,gridArea):
        self.playOrder = list(map(str,range(0,gridArea)))
        random.shuffle(self.playOrder)
        self.csvString = ",".join(self.playOrder)
        return self.csvString

#=========================================================#
#URL routes
@app.route("/")
def index():
    return render_template("index.html")

#---------------#
@app.route("/play_game", methods=["GET","POST"])
def play_game():
    #Below variables should be set to match the error class in the event of an error
    nicknameError = ""
    IDError = ""
    popupHTML = ""

    #Get information from form
    nickname = request.form.get("ipt_nickname")
    gameID = request.form.get("ipt_game_ID")
    submitButton = request.form.get("submit_button") #The value on the submit button (changed if in answer to popup)

    if request.method == "POST":
        userSID = request.cookies.get("SID") #Loads from client cookies

        if submitButton == "Playing here instead": #Check if the user has answered that they wish to use a new SID (in which case delete all reference to old SID)
            queryData = activeUsers.query.filter(activeUsers.userSID==userSID).first()
            if queryData.isHost == True:
                activeGame.query.filter(activeGame.gameID==queryData.userGameID).delete()
            activeUsers.query.filter(activeUsers.userSID==userSID).delete()

        #Check if the SID stored in the user's cookies is still present in the active database
        if userSID != None:
            if activeUsers.query.get(userSID) != None:
                popupHTML = render_template("popups/user_still_active_popup.html")
                return render_template("pre_game.html", nicknameErrClass=nicknameError, gameIDErrClass=IDError, nickname=nickname, gameID=gameID, CSSPopup=Markup(popupHTML))

        #---------------#
        if gameIDValidate(gameID):
            if nicknameValidate(nickname):
                #Saves user details to database
                userSID = random.randint(0,999999)
                while activeGame.query.get(userSID) != None: #Check if chosen SID already exists and keep regerating until it doesn't
                    userSID = random.randint(0,999999)

                newUserActivate = activeUsers(userSID=userSID,userNickname=nickname,userGameID=gameID,isHost=False); #Build new database entry using base class
                gameDB.session.add(newUserActivate);
                gameDB.session.commit();

                #-#
                response =  redirect(f"/sheet_builder?gid={gameID}") #Move on to sheet builder page
                response.set_cookie("SID",str(userSID)) #Save SID for later use
                return response
            else:
                nicknameError="inputError"
        else:
            IDError = "inputError"
    else: #Ensure boxes are blank when page is loaded for the first time
        nickname = ""
        gameID = ""

    return render_template("pre_game.html", nicknameErrClass=nicknameError, gameIDErrClass=IDError, nickname=nickname, gameID=gameID, CSSPopup=Markup(popupHTML))

#---------------#
@app.route("/online_game")
def online_game():
    return render_template("online_game.hhtml")

#---------------#
@app.route('/new_game', methods=["GET","POST"])
def new_game():
    if request.method == "POST":
        # Colleting Item data from POST
        gameData = request.form.get("game_data")
        gameData = gameData.split("|")
        sliderData = gameData[0]
        print(sliderData)
        itemData = gameData[1]
        print(itemData)
        nickname = request.form.get("nickname")
        print(nickname)
        #Generate random ID
        gameID = ""
        for x in range(8):
            gameID = gameID + str(random.randint(0,9))
        while activeGame.query.get(int(gameID)) != None: #Check if chosen gameID already exists and keep regerating until it doesn't
                    gameID = ""
                    for x in range(8):
                        gameID = gameID + str(random.randint(0,9))
        gameID = int(gameID)
        print(gameID)
        userSID = random.randint(0,999999)
        while activeGame.query.get(userSID) != None: #Check if chosen SID already exists and keep regerating until it doesn't
            userSID = random.randint(0,999999)

        newGame = activeGame(gameID=gameID,hostSID=userSID,gridSettings=sliderData,itemSettings=itemData)
        newUser = activeUsers(userSID=userSID,userGameID=gameID,userNickname=nickname,isHost=True)

        gameDB.session.add(newGame)
        gameDB.session.add(newUser)
        gameDB.session.commit()

        response = redirect(f"/sheet_builder?gid={gameID}") # Redirects to sheet builder page
        response.set_cookie("SID",str(userSID)) #Save SID for later use

        return response

    return render_template("new_game.html")

#---------------#
@app.route("/sheet_builder", methods=["GET","POST"])
def game_sheet():
    #Load values from client provided info
    userSID = request.cookies.get("SID") #Loads from client cookies
    gameID = request.args.get("gid") #Loads from URL bar

    if userSID == None or gameID == None:
        return redirect("/new_game")

    #If a user's sheet is already full, move them on
    if activeUsers.query.filter(activeUsers.userGrid!=None,activeUsers.userSID==userSID).first() != None:
        return redirect(f"/playing_online/lobby?gid={gameID}")

    #-#
    #Queries and retries required data from database
    gameData = activeGame.query.get(int(gameID))

    if gameData == None: #If an attempt is made to access page without correct ID
        return "FATAL ERROR!"

    #Gets raw strings
    itemsString = gameData.itemSettings
    gridString = gameData.gridSettings

    #Converts strings to JSON form
    gridJSON = json.loads(gridString)
    itemsJSON = json.loads(itemsString)
    
    #Handles grid that gets sent back
    if request.method == "POST":
        retrievedGrid = request.form.get("grid")
        if gridJSON["GRID_X"] * gridJSON["GRID_Y"] == len(retrievedGrid.split(",")): #Checks that number of items in grid matches its size
            print(retrievedGrid)
            gameDB.session.execute(f"UPDATE activeUsers SET userGrid = \"{retrievedGrid}\" WHERE userSID = {userSID};") #Adds grid info to active user in database
            gameDB.session.commit()
            return redirect(f"/playing_online/lobby?gid={gameID}")

    gridHTML = buildGrid(gridJSON["GRID_X"],gridJSON["GRID_Y"]) #Builds grid using values from loaded JSON

    return render_template("game_sheet.html", grid = gridHTML, itemsMaxJSON=itemsJSON, gridSizeJSON=gridJSON)

#---------------#
@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")

#---------------#
@app.route("/about")
def about_page():
    return render_template("about_page.html")

#---------------#
@app.route("/playing_online/lobby")
def lobby():
    host_content = ""
    if isHost(request.cookies.get("SID"),request.args.get("gid")): #Renders host-only controls if the user is the host
        host_content = Markup(render_template("host_only_lobby.html"))

    return render_template("lobby.html",host_only_content=host_content)

#---------------#
@app.route("/playing_online/game")
def game():
    gameID = request.args.get("gid")
    userID = request.cookies.get("SID")
    hostSID = activeGame.query.get(gameID).hostSID
    hostNick = activeUsers.query.get(hostSID).userNickname
    myNick = activeUsers.query.get(userID).userNickname #Gets your own nickname and passes it to JS in order to replace it with 'YOU'

    #Gets grid information from relevant database
    gridSerial = activeUsers.query.get(userID).userGrid
    gridSettingsJSON = json.loads(activeGame.query.get(gameID).gridSettings)
    gridX = int(gridSettingsJSON["GRID_X"])
    
    usersGrid = drawGameplayGrid(gridX,gridSerial) #Gets the HTML for the grid to draw

    #-#
    #Gets list of all users from database and builds the target selector dropdown
    all_users = activeUsers.query.filter(activeUsers.userGameID==gameID).all()
    dropdown = '<select class="popupDropdown" id="sel_target">'
    for user in all_users:
        if not user.userSID == int(userID): #Excludes you from the list as you can't act on yourself
            nickname = user.userNickname
            dropdown += f'<option value="{nickname}">{nickname}</option>'
    dropdown += "</select>"
    dropdown = Markup(dropdown)

    #-#
    if isHost(userID,gameID):
        return render_template("playing_online_host.html", grid=usersGrid, hostNick=hostNick, target_dropdown=dropdown, myNick=myNick)
    else:
        return render_template("online_game.html", grid=usersGrid, hostNick=hostNick, target_dropdown=dropdown, myNick=myNick)

#=========================================================#
#^ Socketio Functions ^#
#---------------#
#When a user joins a game they get added to the game's room
@socketio.on("join")
def on_join(data):
    gameID = data["gameID"]
    userSID = data["userSID"]
    join_room(gameID)
    send(getActiveUsersList(gameID),room=gameID)

    #Stores user's current socketio SID in database 
    activeUsers.query.get(int(userSID)).socketioSID = request.sid
    gameDB.session.commit()

#---------------#
#When the host opts to start the game
@socketio.on("start")
def start_game(data):
    gameID = data["gameID"]
    userSID = data ["userSID"]

    if isHost(userSID,gameID): #Confirms if user is host and re-broadcasts start event
        emit("start",room=gameID)

        #Load grid data from database
        gameData = activeGame.query.get(int(gameID))
        gridJSON = json.loads(gameData.gridSettings)
        gridSize = int(gridJSON["GRID_X"])*int(gridJSON["GRID_Y"])

        #Generate grid order
        gpClass = gameplay()
        order = gpClass.generate_playOrder(gridSize)

        #Add selection order ro database
        gameData.squareOrder = order
        gameData.currentRound = 0
        gameDB.session.commit()

        

#---------------#
# When the host presses button to move on to next round
@socketio.on("next_round")
def next_round():
    requestSID = request.sid
    gameID = activeUsers.query.filter(activeUsers.socketioSID==requestSID).first().userGameID #Find game ID by querying based on sid
    gameIDString = str(gameID).zfill(8) #Adds leading zeros to gameID for the purpose of room function
    gameObject = activeGame.query.get(gameID) #Load game information from database
    currentRound = gameObject.currentRound +1
    square = gameObject.squareOrder.split(",")[currentRound-1]

    emit("new_square", square, room=gameIDString) #Send selected square to clients

    all_players = activeUsers.query.filter(activeUsers.userGameID==gameIDString).all()
    for player in all_players:
        playerGrid = player.userGrid.split(",")
        item = playerGrid[int(square)]

        #---------------#
        #This is the location in which it is decided what happens with each type of file
        if money(200).identify(item): #Handle money type items
            denomination = item[1:]
            note = money(int(denomination))
            player.userCash = note.cash_update(player.userCash)
            emit("cash_update", player.userCash, room=player.socketioSID)

        #Iterate through all action classes and process them
        for action in actionItem.__subclasses__():
            if action().identify(item):
                instance = action()
                if not action.TARGETTED:
                    player.userCash, player.userBank= instance.calculate_money(player.userCash, player.userBank)
                    emit("cash_update", player.userCash, room=player.socketioSID)
                    emit("bank_update", player.userBank, room=player.socketioSID)
                else:
                    event, data = instance.get_itemNotify()
                    emit(event, data,room=player.socketioSID)

    #Update values in database to newest
    gameObject.currentRound = currentRound
    gameDB.session.commit()

#---------------#
#Handles when somone declares their item
@socketio.on("action_declare")
def action_declared(data):
    requestSID = request.sid
    targetNickname = data["target"]
    actionIdentifier = data["action"]
    perpetrator = activeUsers.query.filter(activeUsers.socketioSID==requestSID).first() #Get a table row representing the perpetrator's information
    gameID = perpetrator.userGameID #Find game ID by querying based on sid
    gameIDString = str(gameID).zfill(8) #Adds leading zeros to gameID for the purpose of room function
    
    if targetNickname != "": #If the declaration includes the target
        target = activeUsers.query.filter(activeUsers.userNickname==targetNickname).first() #Gets a table object of the target

        for actionType in actionItem.__subclasses__():
            if actionType().identify(actionIdentifier):
                instance = actionType()
                target.userCashPending, perpetrator.userCashPending, target.userBankPending, perpetrator.userBankPending = instance.calculate_money(target.userCash, perpetrator.userCash, target.userBank, perpetrator.userBank)
                logEntry = instance.get_log(targetNickname,perpetrator.userNickname)
        
        gameDB.session.commit()

        #Updates the log
        emit('log_update', logEntry, room=gameIDString)

    emit('action_declare', {"target" : targetNickname, "action": actionIdentifier, "perpetrator": perpetrator.userNickname}, room=gameIDString) #Send event to enforce popup

#---------------#
#Handles commit event
@socketio.on("cash_commit")
def cash_commit():
    requestSID = request.sid
    gameID = activeUsers.query.filter(activeUsers.socketioSID==requestSID).first().userGameID #Find game ID by querying based on sid

    allUsers = activeUsers.query.filter(activeUsers.userGameID==gameID, activeUsers.userCashPending != -1).all()
    for user in allUsers:
        user.userCash = user.userCashPending
        user.userBank = user.userBankPending
        user.userCashPending = -1
        user.userBankPending = -1
        #Updates the cash boxes of both the perpetrator and victim
        emit("cash_update", user.userCash, room=user.socketioSID)
        emit("bank_update", user.userBank, room=user.socketioSID)

    gameDB.session.commit()

#---------------#
@socketio.on("use_mirror")
def use_mirror():
    requestSID = request.sid
    victim = activeUsers.query.filter(activeUsers.socketioSID==requestSID).first() #Get a table row representing the victim's information
    if victim.hasMirror:
        pass

#=========================================================#
#^ Main app execution ^#
if __name__ == "__main__":
    testGame = activeGame(gameID=1,hostSID=1,gridSettings='{"GRID_X": 5, "GRID_Y": 5}',itemSettings='{"M5000":1,"M1000":0,"M500":0,"M200":18,"itmShield":1,"itmKill":0,"itmSteal":0,"itmMirror":1,"itmBomb":2,"itmBank":1,"itmSwap":1,"itmGift":0}') #Creates active game for test purposes
    testUser = activeUsers(userSID=1,userGameID=1,userNickname="TEST USER",userGrid="itmSwap,itmSwap,itmSwap,itmKill,M5000,itmKill,itmKill,itmShield,itmGift,itmGift,itmGift,itmGift,itmMirror,itmBomb,itmBomb,itmSteal,itmSteal,itmSteal,itmBank,itmSteal,itmSteal,itmSwap,itmSteal,itmSteal,itmSteal",isHost=True,userCash=0,userBank=0,hasMirror=False,hasShield=False)
    gameDB.create_all() #Creates all defined tables in in-memory database
    gameDB.session.add(testUser)
    gameDB.session.add(testGame)
    gameDB.session.commit()
    socketio.run(app, debug=True, ssl_context=('selfsigned-cert.pem', 'selfsigned-key.pem')) #SocketIo required for two way communication
