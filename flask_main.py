#---------------------------------------------------------------------#
# File: A-Level-Personal-Code-Collab/PirateGame/flask_main.py
# Project: A-Level-Personal-Code-Collab/PirateGame
# Created Date: Thursday, July 8th 2021, 4:38:56 pm
# Description: Main flask webserver root.
# Author: Will Hall
# Copyright (c) 2021 Lime Parallelogram
# -----
# Last Modified: Wed Aug 04 2021
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2021-08-02	WH	Added nickname validator routine which, if sucessful, redirects user to /sheet_builder
# 2021-08-02	WH	Converted application to socketio application
# 2021-07-09	WH	Added code to generate and serve basic playing grid
# 2021-07-08	WH	Added very basic flask server structure
#---------------------------------------------------------------------#
from re import sub
from flask import Flask, render_template, Markup, send_file, request
from flask_socketio import SocketIO
from flask.helpers import url_for
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = '0nOxRU2ipDewLH1d'
socketio = SocketIO(app)

#=========================================================#
#Slave subs

#---------------#
#Builds the HTML syntax to draw the game grid - makes the grid easily exapandable + avoid typing repetative HTML code
def buildGrid():
#Imports modules 
    #Local Constants
    CLASS_NAME = "gridSquare" #The name of the class that all td objects will share

    #Grid variable will acumulate the HTML table
    grid = "<table id=\"tbl_CoordinatesGrid\">"

    collums = [" ","A","B","C","D","E","F"] #The lables on the X-Axis
    rows = list(range(1,7)) #The Y-axis lables

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
    ####TODO: Create databaselinkage####
    return True

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
                return redirect("/sheet_builder") #Move on to sheet builder page
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
@app.route('/new_game')
def new_game():
    return render_template("new_game.html")

#---------------#
@app.route("/sheet_builder")
def game_sheet():
    gridHTML = buildGrid()
    return render_template("game_sheet.html", grid = gridHTML)

#---------------#
@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")

#---------------#
@app.route("/about")
def about_page():
    return render_template("about_page.html")

#=========================================================#
#Main app execution
if __name__ == "__main__":
    socketio.run(app) #SocketIo required for two way communication