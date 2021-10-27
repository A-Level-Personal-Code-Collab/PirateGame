#!/bin/python3
#---------------------------------------------------------------------#
# File: A-Level-Personal-Code-Collab/PirateGame/flask_main.py
# Project: A-Level-Personal-Code-Collab/PirateGame
# Created Date: Thursday, July 8th 2021, 4:38:56 pm
# Description: Main flask webserver root.
# Author: Will Hall
# Copyright (c) 2021 Lime Parallelogram
# -----
# Last Modified: Wed Oct 27 2021
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2021-10-27	WH	Added automatic commit to actions to users that are offline
# 2021-10-27	WH	Added new URL route for error pages
# 2021-10-27	WH	Added access control to lobby, sheet builder and gameplay pages to return an error if the game does not exist
# 2021-10-27	WH	Added isOpen property to all games
# 2021-10-27	WH	Added disconnect handling
# 2021-10-25	WH	Moved gameplay class and gameplay generators to gameplay file
# 2021-10-24	WH	Converted to allow gevent compatibility
# 2021-10-20	WH	Revereted to working system without disconnect handler
# 2021-10-01	WH	All user information sent to client is now sent as an SID and not as the nickname itself
# 2021-10-01	WH	Removed server side generation of target picker
# 2021-10-01	WH	Changed list generator to generate nickname/sid dictionary instead of sending raw html list
# 2021-10-01	WH	Added on_disconnect function
# 2021-09-29	WH	Declares the retaliation in order to show animation
# 2021-09-27	WH	Added nickname validation for new_game
# 2021-09-26	WH	Added game finnished event to forward to results page
# 2021-09-25	WH	Now sends list of invalied retaliations with action declare
# 2021-09-25	WH	Data classes now also define the future tense version of the event name for the popup
# 2021-09-19	WH	Added comments and tidy code
# 2021-09-19	WH	Added retaliation system for all other retaliation options
# 2021-09-18	WH	Added equation parser script
# 2021-09-18	WH	Dataclasses now contain an expression that is parsed to calculale how each action effects all the cash containers
# 2021-09-17	WH	standardised refrence to item names so, for example, kill is refrenced as itmKill everywhere
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
#=========================================================#
#^ Imports Modules ^#
from re import A, sub
import re
from typing import final
from weakref import ProxyTypes
from flask import Flask, render_template, Markup, send_file, request
from flask_socketio import SocketIO, join_room, rooms, send, emit
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
import json
import random
from string import Template
import time
from time import sleep

from werkzeug.wrappers import response

import gameplay
#=========================================================#
#^ Configure flask webserver ^#
app = Flask(__name__)
app.config['SECRET_KEY'] = '0nOxRU2ipDewLH1d'
socketio = SocketIO(app)

#---------------#
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

gameDB = SQLAlchemy(app)

TotalGames = 0
GAMEVERSION = "Beta 1.0"
#=========================================================#
#^ Database table models ^#
#(these are required by SQL alchemy to interact with database so the variable names and info must correspond with your database)
#---------------#
#The table that stores a log of all currently active games
class activeGames(gameDB.Model):
    __tablename__ = 'activeGamess'
    gameID = gameDB.Column(gameDB.Integer, primary_key=True)
    hostSID = gameDB.Column(gameDB.Integer)
    gridSettings = gameDB.Column(gameDB.String(100))
    itemSettings = gameDB.Column(gameDB.String(100))
    currentRound = gameDB.Column(gameDB.Integer)
    squareOrder = gameDB.Column(gameDB.String(300))
    remainingActions = gameDB.Column(gameDB.Integer, default=0)
    resultsScores = gameDB.Column(gameDB.String(1000))
    isOpen = gameDB.Column(gameDB.Boolean, default=True)

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
    userPendingExpression = gameDB.Column(gameDB.String(200), default="")
    userPendingDeclaration = gameDB.Column(gameDB.Boolean, default=False)
    userBank = gameDB.Column(gameDB.Integer, default=0)
    availableRetaliatios = gameDB.Column(gameDB.String(255))


#=========================================================#
#^ Data classes to define the action's model ^#
class actionItem():
    '''The base class for any action obejct that is created'''
    ACTION_EMOJI = "❔"
    ACTION_IDENTIFIER = "itmUNDEF"
    MATHS_EXPRESSION= "vCash=vCash:vBank=vBank|pCash=pCash:pBank=pBank"
    LOG_MESSAGE = "{emoji} !<{perpetrator}> did undefined action on !<{victim}> {emoji}"
    FUTURE_TENSE_VERB_MSG = "{emoji} UNDEF {emoji}"
    INVALIED_RETALIATIONS = []

    def get_log(self, victim, perpetrator):
        return self.LOG_MESSAGE.format(emoji=self.ACTION_EMOJI,perpetrator=perpetrator,victim=victim)

    def get_popupVerb(self):
        return self.FUTURE_TENSE_VERB_MSG.format(emoji=self.ACTION_EMOJI)

    def identify(self,test):
        if test == self.ACTION_IDENTIFIER:
            return True
        else:
            return False

    def get_itemNotify(self):
        popupMessage = self.get_popupVerb()
        return "itm_available", {"type": self.ACTION_IDENTIFIER, "ftVerb": popupMessage}

    def get_expressions(self):
        expression = self.MATHS_EXPRESSION.split("|")
        if len(expression) == 1:
            return expression[0], ""
        else:
            return expression[0], expression[1]

    def isRetalValid(self,retalType):
        if retalType in self.INVALIED_RETALIATIONS:
            return False
        else: 
            return True

#---------------#
class retaliatoryAction:
    '''The base class for retaliatory actions like mirror'''
    ACTION_EMOJI = "❔"
    ACTION_IDENTIFIER = "itmUNDEF"
    LOG_MESSAGE = "{emoji} !<{perpetrator}> did undefined action on !<{victim}> {emoji}"

    def get_log(self, victim, perpetrator):
        return self.LOG_MESSAGE.format(emoji=self.ACTION_EMOJI,perpetrator=perpetrator,victim=victim)

    def identify(self,test):
        if test == self.ACTION_IDENTIFIER:
            return True
        else:
            return False

    def get_itemNotify(self):
        return "retal_available", {"type": self.ACTION_IDENTIFIER, "image": self.IMAGE_LOCATION}

    def get_pushback_dat(self):
        return {"type": self.ACTION_IDENTIFIER, "animation-image": self.IMAGE_LOCATION[:-4]+"-notrans.png", "animation-class": self.ACTION_IDENTIFIER+"-animation"}

#=========================================================#
#^ Action Data classes  - describes what each action does and how it behaves ^#
class itmKill(actionItem):
    '''Class for kill item (victim's money is set to 0)'''
    IMAGE_LOCATION = "../static/img/kill.png"
    ACTION_EMOJI = "⚔"
    ACTION_IDENTIFIER = "itmKill"
    MATHS_EXPRESSION= "self.vCash=0:self.vBank={vBank}|self.pCash={pCash}:self.pBank={pBank}"
    LOG_MESSAGE = "{emoji} !<{perpetrator}> killed !<{victim}> {emoji}"
    FUTURE_TENSE_VERB_MSG = "{emoji} KILL {emoji}"
    INVALIED_RETALIATIONS = []
    TARGETTED = True

#---------------#
class itmSteal(actionItem):
    '''Class for steal item (victim's money is given to perpetrator)'''
    IMAGE_LOCATION = "../static/img/steal.png"
    ACTION_EMOJI = "💰"
    ACTION_IDENTIFIER = "itmSteal"
    MATHS_EXPRESSION= "self.vCash=0:self.vBank={vBank}|self.pCash={pCash}+{vCash}:self.pBank={pBank}"
    LOG_MESSAGE = "{emoji} !<{perpetrator}> stole from !<{victim}> {emoji}"
    FUTURE_TENSE_VERB_MSG = "{emoji} STEAL FROM {emoji}"
    INVALIED_RETALIATIONS = []
    TARGETTED = True

#---------------#
class itmGift(actionItem):
    '''Class for gift item (victim recieves 1000M from nowhere)'''
    IMAGE_LOCATION = "../static/img/gift.png"
    ACTION_EMOJI = "🎁"
    ACTION_IDENTIFIER = "itmGift"
    MATHS_EXPRESSION= "self.vCash={vCash}+1000:self.vBank={vBank}|self.pCash={pCash}:self.pBank={pBank}"
    LOG_MESSAGE = "{emoji} !<{perpetrator}> gifted !<{victim}> {emoji}"
    FUTURE_TENSE_VERB_MSG = "{emoji} GIFT {emoji}"
    INVALIED_RETALIATIONS = []
    TARGETTED = True


#---------------#
class itmSwap(actionItem):
    '''Class for swap item (perpetrator and victim swap cash)'''
    IMAGE_LOCATION = "../static/img/swap.png"
    ACTION_EMOJI = "🤝"
    ACTION_IDENTIFIER = "itmSwap"
    MATHS_EXPRESSION= "self.vCash={pCash}:self.vBank={vBank}|self.pCash={vCash}:self.pBank={pBank}"
    LOG_MESSAGE = "{emoji} !<{perpetrator}> swapped with !<{victim}> {emoji}"
    FUTURE_TENSE_VERB_MSG = "{emoji} SWAP WITH {emoji}"
    INVALIED_RETALIATIONS = ["itmMirror"]
    TARGETTED = True

#---------------#
class itmBomb(actionItem):
    '''Class for bomb item'''
    IMAGE_LOCATION = "../static/img/bomb.png"
    ACTION_EMOJI = "💣"
    ACTION_IDENTIFIER = "itmBomb"
    MATHS_EXPRESSION= "self.vCash=0:self.vBank={vBank}"
    LOG_MESSAGE = ""
    INVALIED_RETALIATIONS = ["itmShield","itmMirror"]
    TARGETTED = False

#---------------#
class itmBank(actionItem):
    '''Class for bank item'''
    IMAGE_LOCATION = "../static/img/bank.png"
    ACTION_EMOJI = "🏦"
    ACTION_IDENTIFIER = "itmBank"
    MATHS_EXPRESSION= "self.vCash=0:self.vBank={vBank}+{vCash}"
    LOG_MESSAGE = ""
    INVALIED_RETALIATIONS = ["itmShield","itmMirror"]
    TARGETTED = False

#=========================================================#
#^ Defines how retaliation actions behave ^#
class itmMirror(retaliatoryAction):
    '''Class for mirror modifier item'''
    IMAGE_LOCATION = "../static/img/mirror.png"
    ACTION_EMOJI = "🪞"
    ACTION_IDENTIFIER = "itmMirror"
    LOG_MESSAGE = "{emoji} !<{victim}> mirrored that {emoji}"

    def expression_manipulate(self, expression):
        self.new_expression = expression.replace("self.vCash","___V.CASH___")
        self.new_expression = self.new_expression.replace("self.pCash","___P.CASH___")
        self.new_expression = self.new_expression.replace("___P.CASH___","self.vCash")
        self.new_expression = self.new_expression.replace("___V.CASH___","self.pCash")

        return self.new_expression

#---------------#
class itmShield(retaliatoryAction):
    '''Class for shield modifier item'''
    IMAGE_LOCATION = "../static/img/shield.png"
    ACTION_EMOJI = "🛡"
    ACTION_IDENTIFIER = "itmShield"
    LOG_MESSAGE = "{emoji} !<{victim}> blocked that {emoji}"

    def expression_manipulate(self, expression):
        return "self.vCash={vCash}:self.vBank={vBank}:self.pCash={pCash}:self.pBank={pBank}"

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
#^ URL routes ^#
#---------------#
#The index page
@app.route("/")
def index():
    activegames = gameplay.information().calcActiveGames(activeGames)
    return render_template("index.html",currentActiveGames = activegames, totalGames = TotalGames, version = GAMEVERSION)

#---------------#
#Error pages
@app.route("/error")
def error():
    code = request.args.get("code")
    message = gameplay.parsers().getERROR(code) #Get error message from code
    return render_template("errors/error_base.html",message=message)

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
                activeGames.query.filter(activeGames.gameID==queryData.userGameID).delete()
            activeUsers.query.filter(activeUsers.userSID==userSID).delete()

        #Check if the SID stored in the user's cookies is still present in the active database
        if userSID != None:
            if activeUsers.query.get(userSID) != None:
                popupHTML = render_template("popups/user_still_active_popup.html")
                return render_template("pre_game.html", nicknameErrClass=nicknameError, gameIDErrClass=IDError, nickname=nickname, gameID=gameID, CSSPopup=Markup(popupHTML))

        #---------------#
        if gameplay.validators().gameIDValidate(gameID,activeGames):
            if gameplay.validators().nicknameValidate(nickname):
                #Saves user details to database
                userSID = gameplay.generators().generate_SID(activeUsers)

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
        itemData = gameData[1]
        nickname = request.form.get("nickname")

        if gameplay.validators().nicknameValidate(nickname):
            #Generate random ID
            gameID = ""
            for x in range(8):
                gameID = gameID + str(random.randint(0,9))
            while activeGames.query.get(int(gameID)) != None: #Check if chosen gameID already exists and keep regerating until it doesn't
                        gameID = ""
                        for x in range(8):
                            gameID = gameID + str(random.randint(0,9))
            gameID = int(gameID)
            userSID = random.randint(0,999999)
            while activeGames.query.get(userSID) != None: #Check if chosen SID already exists and keep regerating until it doesn't
                userSID = random.randint(0,999999)

            newGame = activeGames(gameID=gameID,hostSID=userSID,gridSettings=sliderData,itemSettings=itemData)
            newUser = activeUsers(userSID=userSID,userGameID=gameID,userNickname=nickname,isHost=True)

            gameDB.session.add(newGame)
            gameDB.session.add(newUser)
            gameDB.session.commit()

            global TotalGames
            TotalGames = TotalGames + 1

            response = redirect(f"/sheet_builder?gid={gameID}") # Redirects to sheet builder page
            response.set_cookie("SID",str(userSID)) #Save SID for later use

            return response

    return render_template("new_game.html")

#---------------#
@app.route("/sheet_builder", methods=["GET","POST"])
@gameplay.validators.pageControlValidate(activeUsers,activeGames)
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
    gameData = activeGames.query.get(int(gameID))

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
            gameDB.session.execute(f"UPDATE activeUsers SET userGrid = \"{retrievedGrid}\" WHERE userSID = {userSID};") #Adds grid info to active user in database
            gameDB.session.commit()
            return redirect(f"/playing_online/lobby?gid={gameID}")

    gridHTML = gameplay.generators().html.buildEditableGrid(gridJSON["GRID_X"],gridJSON["GRID_Y"]) #Builds grid using values from loaded JSON

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
@app.route("/patch_notes")
def patch_notes():
    return render_template("patch_notes.html")

@app.route("/patch_notes/B1-0")
def B1_0():
    return render_template("beta_1-0.html")

#---------------#
@app.route("/playing_online/lobby")
@gameplay.validators.pageControlValidate(activeUsers,activeGames)
def lobby():
    #Redirect away if the user does not have correct cookies
    if request.cookies.get("SID") == None:
        return redirect("/error?code=NOSID")

    try:
        gameID = request.args.get("gid")
        gameLine = activeGames.query.get(int(gameID))
        if gameLine.isOpen == False:
            return redirect(f"/playing_online/game?gid={gameID}")
        hostSID = gameLine.hostSID
        hostNick = activeUsers.query.get(hostSID).userNickname
        host_content = ""
        if gameplay.validators().isHost(request.cookies.get("SID"),request.args.get("gid"),activeGames): #Renders host-only controls if the user is the host
            host_content = Markup(render_template("host_only_lobby.html"))

        return render_template("lobby.html",host_only_content=host_content,gameID=gameID,hostNick=hostNick)
    except AttributeError: #Redirect away if game does not exist
        return redirect("/error?code=GAMEINVALIED")

#---------------#
@app.route("/playing_online/game")
@gameplay.validators.pageControlValidate(activeUsers,activeGames)
def game():
    gameID = request.args.get("gid")
    userID = request.cookies.get("SID")

    try:
        hostSID = activeGames.query.get(gameID).hostSID
        hostNick = activeUsers.query.get(hostSID).userNickname
        mySID = activeUsers.query.get(userID).userSID #Gets your own nickname and passes it to JS in order to replace it with 'YOU'

        #Gets grid information from relevant database
        gridSerial = activeUsers.query.get(userID).userGrid
        gridSettingsJSON = json.loads(activeGames.query.get(gameID).gridSettings)
        gridX = int(gridSettingsJSON["GRID_X"])
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
        usersGrid = gameplay.generators().html.drawGameplayGrid(gridX,gridSerial,IMAGE_URLS) #Gets the HTML for the grid to draw

        #-#
        if gameplay.validators().isHost(userID,gameID,activeGames):
            return render_template("playing_online_host.html", grid=usersGrid, hostNick=hostNick, mySID=mySID)
        else:
            return render_template("online_game.html", grid=usersGrid, hostNick=hostNick, mySID=mySID)
    except AttributeError:
        return redirect("/error?code=GAMEINVALIED")

@app.route("/playing_online/results")
def results():
    #fetches user data
    gameID = request.args.get("gid")
    userID = request.cookies.get("SID")

    userscores = json.loads(activeGames.query.get(gameID).resultsScores)

    sorted_scores = dict(sorted(userscores.items(),key = lambda x:x[1],reverse=True ))
    final_scores_table = "<table class=\"sidebarscores\"> <tr class=\"ResultsTableHeader\"> <td></td><td> Player </td> <td> Final Cash </td> </tr> "
    placing = 1
    podiumscores = {}
    for name,score in sorted_scores.items():
        if placing <=3:
            podiumscores[name] = score
        else:
            final_scores_table += f"<tr> <td>{placing}</td> <td> {name} </td> <td> {score} </td> </tr>"
        placing += 1 
    final_scores_table += "</table>"
    return render_template ("results.html",results_table = Markup (final_scores_table),podiumscores = podiumscores)

#=========================================================#
#^ Socketio Functions ^#
#---------------#
#When a user joins a game they get added to the game's room
@socketio.on("join")
def on_join(data):
    gameID = data["gameID"]
    userSID = data["userSID"]
    print(f"New user joined the game {gameID} with a userSID of {userSID}")

    try:
        #Stores user's current socketio SID in database 
        user = activeUsers.query.filter(activeUsers.userSID==int(userSID)).first()
        print(user)
        user.socketioSID = request.sid
        gameDB.session.commit()

        join_room(gameID)

        #Update the user list on all uer's screen
        online_users = gameplay.generators().getActiveUsersDictionary(gameID,activeUsers)
        emit("users_update", online_users,room=gameID)
        emit("log_update", gameplay.loggers().userConnect(user.userNickname),room=gameID) #Show log entry if a user leaves
    except AttributeError or ValueError:
        emit("ERR", "User ID that was submitted was not found in our DB", room=request.sid)

#---------------#
#When a user gets to disconnect from a page
@socketio.on("disconnect")
def disconnect():
    userLine = activeUsers.query.filter(activeUsers.socketioSID==request.sid).first()
    if userLine != None:
        gameID = str(userLine.userGameID).zfill(8)
        if gameplay.validators().isHost(request.sid,gameID,activeGames):
            print(f"HOST {userLine.userNickname} has just disconnected from a game")
        else:
            print(f"User {userLine.userNickname} has just disconnected from a game")
            userLine.socketioSID = None
            if userLine.userPendingDeclaration:
                gameLine = activeGames.query.get(userLine.userGameID)
                if gameplay.functions().actionComplete(gameLine): #Completed action and runs event if this completed a round
                    emit("round_complete",room=gameID)

            userLine.userPendingDeclaration = False
            #Update the user list on all uer's screen
            gameDB.session.commit()
            online_users = gameplay.generators().getActiveUsersDictionary(gameID,activeUsers)
            emit("users_update", online_users,room=gameID)
            emit("log_update", gameplay.loggers().userDisconnect(userLine.userNickname),room=gameID)
            

#---------------#
#When the host opts to start the game (from lobby)
@socketio.on("start")
def start_game(data):
    gameID = data["gameID"]
    userSID = data ["userSID"]

    if gameplay.validators().isHost(userSID,gameID,activeGames): #Confirms if user is host and re-broadcasts start event
        emit("start",room=gameID)

        #Load grid data from database
        gameData = activeGames.query.get(int(gameID))
        gridJSON = json.loads(gameData.gridSettings)
        gridSize = int(gridJSON["GRID_X"])*int(gridJSON["GRID_Y"])

        #Generate grid order
        gpClass = gameplay.generators()
        order = gpClass.generate_playOrder(gridSize)

        #Add selection order ro database
        gameData.squareOrder = order
        gameData.currentRound = 0

        #Close game
        gameData.isOpen = False
        
        gameDB.session.commit()

        

#---------------#
# When the host presses button to move on to next round
@socketio.on("next_round")
def next_round():
    requestSID = request.sid
    gameID = activeUsers.query.filter(activeUsers.socketioSID==requestSID).first().userGameID #Find game ID by querying based on sid
    gameIDString = str(gameID).zfill(8) #Adds leading zeros to gameID for the purpose of room function
    gameObject = activeGames.query.get(gameID) #Load game information from database
    currentRound = gameObject.currentRound +1
    allSquares = gameObject.squareOrder.split(",")

    if currentRound > len(allSquares):
        gameplay.events().gameEnd(gameID,activeGames,activeUsers,gameDB)
        emit("game_complete", room=gameIDString)

    else:
        square = allSquares[currentRound-1]
        emit("new_square", square, room=gameIDString) #Send selected square to clients

        sleep(3) #Time for animation to occur on client

        all_players = activeUsers.query.filter(activeUsers.userGameID==gameIDString,activeUsers.socketioSID!=None).all()
        actionsRequired = 0 #Used to track whether the next round can begin imediately
        for player in all_players:
            playerGrid = player.userGrid.split(",")
            item = playerGrid[int(square)]

            #---------------#
            #Handle money items
            if money(200).identify(item): #Use the identify method from data class
                denomination = item[1:] #Get the denomination value by removing the 'M' from the ID
                note = money(int(denomination)) #Get instance of data class
                player.userCash = note.cash_update(player.userCash) #Update player's cash value in database
                emit("cash_update", player.userCash, room=player.socketioSID) #Send cash update event

            #---------------#
            #Iterate through all action classes and process them
            for action in actionItem.__subclasses__():
                instance = action()
                if instance.identify(item): #Use the identify method to test if the action in question is the desired action
                    if not action.TARGETTED: #For actions that do not have target selectors, apply them imediately
                        actionExpression, null = instance.get_expressions() #Get the expression, discarding the seccond half as it doesn't have a seccond player involved
                        player.userCash, player.userBank , null, null = gameplay.parsers().parse_money(actionExpression,player) #Parse expression
                        emit("cash_update", player.userCash, room=player.socketioSID) #Run cash updates
                        emit("bank_update", player.userBank, room=player.socketioSID)
                    elif gameplay.validators().isOnline(player.userSID,activeUsers): #Only handle actionable events if they are onlie
                        actionsRequired += 1
                        player.userPendingDeclaration = True
                        event, data = instance.get_itemNotify() #For actions that are targetted, notify the client that they have one of these
                        emit(event, data,room=player.socketioSID)
                    break #Break loop after detecting correct item to save resources
            
            #---------------#
            #Iterate through retaliation actions to identify if the user has one of those
            for action in retaliatoryAction.__subclasses__():
                instance = action()
                if instance.identify(item):
                    player.availableRetaliatios = f"{player.availableRetaliatios},{item}"
                    event, data = instance.get_itemNotify() #Notify client that they have a retaliation option
                    emit(event, data,room=player.socketioSID)

    #---------------#
    if actionsRequired == 0:
        emit("round_complete",room=gameIDString)
    else:
        gameObject.remainingActions = actionsRequired

    #---------------#
    #Update values in database to newest
    gameObject.currentRound = currentRound
    gameDB.session.commit()

#---------------#
#Handles when somone declares their action item
@socketio.on("action_declare")
def action_declared(data):
    requestSID = request.sid
    targetSID = data["target"]
    actionIdentifier = data["action"] #The type of action we are dealing with
    perpetrator = activeUsers.query.filter(activeUsers.socketioSID==requestSID).first() #Get a table row representing the perpetrator's information
    gameID = perpetrator.userGameID #Find game ID by querying based on sid
    gameIDString = str(gameID).zfill(8) #Adds leading zeros to gameID for the purpose of room function
    invalidRetals = ""
    
    #---------------#
    #Handling for once a target has been selcted
    if targetSID != "": #If the declaration includes the target information
        target = activeUsers.query.filter(activeUsers.userSID==targetSID).first() #Gets a database record object of the target

        for actionType in actionItem.__subclasses__():
            instance = actionType()
            if instance.identify(actionIdentifier):
                target.userPendingExpression, perpetrator.userPendingExpression = instance.get_expressions() #Save the expression information to the database based on what event has taken place
                invalidRetals = ",".join(instance.INVALIED_RETALIATIONS)
                logEntry = instance.get_log(targetSID,perpetrator.userSID) #Log the action to the logs
                if not gameplay.validators().isOnline(target.userSID,activeUsers): #Automatically commit action if user is offline
                    moneyHandlingExpression = target.userPendingExpression+":"+perpetrator.userPendingExpression #Create combined expression for money that tells what happens to both parties
                    target.userCash, target.userBank, perpetrator.userCash, perpetrator.userBank = gameplay.parsers().parse_money(moneyHandlingExpression, target, perpetrator)
                    for user in [target,perpetrator]:
                        user.userPendingExpression = ""
                        #Updates the cash boxes of both the perpetrator and victim
                        emit("cash_update", user.userCash, room=user.socketioSID)
                        emit("bank_update", user.userBank, room=user.socketioSID)

                    if gameplay.functions().actionComplete(activeGames.query.get(gameID)): #Completed action and runs event if this completed a round
                        emit("round_complete",room=gameIDString)
                break # Break to save resources

        gameDB.session.commit()

        #Updates the log
        emit('log_update', logEntry, room=gameIDString)
    
    fTenseMessage = eval(f"{actionIdentifier}().get_popupVerb()") #Uses the dataclass system to get the propper grammer for the popup messgae
    emit('action_declare', {"target" : targetSID, "action": actionIdentifier, "perpetrator": perpetrator.userSID, "ftVerb": fTenseMessage, "invalidRetals": invalidRetals}, room=gameIDString) #Re-broadcast event to enforce popup

#---------------#
#Handles when a client declares their response to an action being done against them
@socketio.on("retaliation_declare")
def retaliation_decl(data):
    requestSID = request.sid
    victim = activeUsers.query.filter(activeUsers.socketioSID==requestSID).first() #Load victim from database
    perpetrator = activeUsers.query.filter(activeUsers.userGameID==victim.userGameID, activeUsers.userPendingExpression != "", activeUsers.userSID != victim.userSID).first() #Find perpetrator based on the fact that they too will have changes to their pending

    moneyHandlingExpression= victim.userPendingExpression+":"+perpetrator.userPendingExpression #Create combined expression for money that tells what happens to both parties
    gameID = perpetrator.userGameID #Find game ID from perpetrator
    gameIDString = str(gameID).zfill(8) #Adds leading zeros to gameID for the purpose of room function
    retal_type = data["type"] #Gets the string dictating the clients response
    aktvGame = activeGames.query.get(gameID)

    #---------------#
    #Loops through avilable retaliations to check if it matches any of those
    if retal_type != "none":
        for action in retaliatoryAction.__subclasses__():
            instance = action()
            if instance.identify(retal_type):
                availableRetals = victim.availableRetaliatios.split(",")
                if retal_type in availableRetals:
                    availableRetals.remove(retal_type)
                    victim.availableRetaliatios = ",".join(availableRetals)
                    moneyHandlingExpression = instance.expression_manipulate(moneyHandlingExpression) #Change the money handling expression based on what is dicted in the retaliation's data class
                    emit("log_update", instance.get_log(victim.userSID,perpetrator.userSID),room=gameIDString) #Add retaliation log entry
                    emit("retaliation_declare", instance.get_pushback_dat(),room=gameIDString)
                    break #Break to save resources

    #---------------#
    #Actually parse new (or un-updated) money expression to new cash values
    victim.userCash, victim.userBank, perpetrator.userCash, perpetrator.userBank = gameplay.parsers().parse_money(moneyHandlingExpression, victim, perpetrator)

    #---------------#
    #Send cash updates and bank updates to users as well as resetting their pending expression
    for user in [victim,perpetrator]:
        user.userPendingExpression = ""

        #Updates the cash boxes of both the perpetrator and victim
        emit("cash_update", user.userCash, room=user.socketioSID)
        emit("bank_update", user.userBank, room=user.socketioSID)

    if gameplay.functions().actionComplete(aktvGame): #Completed action and runs event if this completed a round
        emit("round_complete",room=gameIDString)

    gameDB.session.commit()

#=========================================================#
#^ Main app execution ^#
testGame = activeGames(gameID=1,hostSID=1,resultsScores='{"tuser1": 5000, "testifications2": 5587, "tuser2":4000, "test3": 2870, "test4": 2587, "test5": 3540, "test6": 1234, "WWWWWWWWWWWWWWW": 5343, "test8": 1750, "test9": 4300, "test10": 2900, "test11": 2800, "test12": 1750, "test13": 1700, "test14": 3900, "test15": 1500, "test16": 4700, "test17": 3500}',gridSettings='{"GRID_X": 5, "GRID_Y": 5}',itemSettings='{"M5000":1,"M1000":0,"M500":0,"M200":18,"itmShield":1,"itmKill":0,"itmSteal":0,"itmMirror":1,"itmBomb":2,"itmBank":1,"itmSwap":1,"itmGift":0}') #Creates active game for test purposes
testUser = activeUsers(userSID=1,userGameID=1,userNickname="MONEY USER",userGrid="M5000,M5000,M5000,M5000,M5000,M5000,M5000,M5000,M5000,M5000,M5000,M5000,M5000,M5000,M5000,itmBank,itmBank,itmBank,itmBank,itmBank,itmBank,itmBank,itmBank,itmBank,itmBank",isHost=True,userCash=0,userBank=0,socketioSID="jkdfhjkjdjkfhunbmbnmvcbhjdbnmjhhejhjfksajkhfdjkhfjh")
testUser2 = activeUsers(userSID=2,userGameID=1,userNickname="ACTIONS USER",userGrid="itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal,itmSteal",isHost=False,userCash=0,userBank=0,socketioSID="kfjkjkdkfjhjghsgvfjhfhj")
testUser3 = activeUsers(userSID=3,userGameID=1,userNickname="RETALIATIONS USER",userGrid="itmMirror,itmMirror,itmMirror,itmMirror,itmMirror,itmMirror,itmMirror,itmMirror,itmMirror,itmMirror,itmMirror,itmMirror,itmMirror,itmSteal,itmSteal,itmSteal,itmSteal,itmShield,itmShield,itmShield,itmShield,itmShield,itmShield,itmShield,itmShield",isHost=False,userCash=0,userBank=0,socketioSID="jdsgfghdjfghjsgfhghjghjgsjf")
gameDB.create_all() #Creates all defined tables in in-memory database
gameDB.session.add(testUser)
gameDB.session.add(testUser2)
gameDB.session.add(testUser3)
gameDB.session.add(testGame)
gameDB.session.commit()

if __name__ == "__main__":
    socketio.run(app, debug=True, ssl_context=('selfsigned-cert.pem', 'selfsigned-key.pem'), host="0.0.0.0") #SocketIo required for two way communication