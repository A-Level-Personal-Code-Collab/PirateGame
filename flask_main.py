#---------------------------------------------------------------------#
# File: A-Level-Personal-Code-Collab/PirateGame/flask_main.py
# Project: A-Level-Personal-Code-Collab/PirateGame
# Created Date: Thursday, July 8th 2021, 4:38:56 pm
# Description: Main flask webserver root.
# Author: Will Hall
# Copyright (c) 2021 Lime Parallelogram
# -----
# Last Modified: Mon Aug 09 2021
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
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
from flask_socketio import SocketIO
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
import json
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = '0nOxRU2ipDewLH1d'
socketio = SocketIO(app)

#---------------#
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

gameDB = SQLAlchemy(app)

#=========================================================#
#^ Database table models ^#
#(these are required by SQL alchemy to interact with database so the variable names and info must correspond with your database)
#---------------#
#The table that stores a log of all currently active games
class activeGame(gameDB.Model):
    __tablename__ = 'activeGames'
    gameID = gameDB.Column(gameDB.Integer, primary_key=True)
    hostSID = gameDB.Column(gameDB.Integer)
    gridSettings = gameDB.Column(gameDB.String(100))
    itemSettings = gameDB.Column(gameDB.String(100))

#---------------#
#The table that stores a log of all active users and their grids
class activeUsers(gameDB.Model):
    __tablename__ = 'activeUsers'
    userNickname = gameDB.Column(gameDB.String(15))
    userSID = gameDB.Column(gameDB.Integer, primary_key=True)
    userGameID = gameDB.Column(gameDB.Integer)
    userGrid = gameDB.Column(gameDB.String(9999))
    isHost = gameDB.Column(gameDB.Boolean)


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

    #Get information from form
    nickname = request.form.get("ipt_nickname")
    gameID = request.form.get("ipt_game_ID")

    if request.method == "POST":
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

    return render_template("pre_game.html", nicknameErrClass=nicknameError, gameIDErrClass=IDError, nickname=nickname, gameID=gameID)

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

        gameDB.session.add(newGame)
        gameDB.session.commit()


    return render_template("new_game.html")

#---------------#
@app.route("/sheet_builder", methods=["GET","POST"])
def game_sheet():
    #Load values from client provided info
    userSID = request.cookies.get("SID") #Loads from client cookies
    gameID = request.args.get("gid") #Loads from URL bar

    if userSID == None or gameID == None:
        return redirect("/new_game")

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
            gameDB.session.execute(f"UPDATE activeUsers SET userGrid = \"{retrievedGrid}\" WHERE userSID = {userSID};") #Adds grid info to active user in database
            gameDB.session.commit()
            return redirect("/waiting")

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
@app.route("/waiting")
def lobby():
    return "Waiting"

#=========================================================#
#Main app execution
if __name__ == "__main__":
    testGame = activeGame(gameID=1,hostSID=1,gridSettings='{"GRID_X": 5, "GRID_Y": 5}',itemSettings='{"M5000":1,"M1000":0,"M500":0,"M200":18,"itmShield":1,"itmKill":0,"itmSteal":0,"itmMirror":1,"itmBomb":2,"itmBank":1,"itmSwap":1,"itmGift":0}')
    gameDB.create_all() #Creates all defined tables in in-memory database
    gameDB.session.add(testGame)
    gameDB.session.commit()
    socketio.run(app, debug=True, ssl_context=('selfsigned-cert.pem', 'selfsigned-key.pem')) #SocketIo required for two way communication
