#!/bin/python3
#---------------------------------------------------------------------#
# File: A-Level-Personal-Code-Collab/PirateGame/flask_main.py
# Project: A-Level-Personal-Code-Collab/PirateGame
# Created Date: Thursday, July 8th 2021, 4:38:56 pm
# Description: Main flask webserver root.
# Author: Will Hall
# Copyright (c) 2021 Lime Parallelogram
# -----
# Last Modified: Fri Nov 12 2021
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2021-11-08	AO	Added the patch notes routes and tests whether they are a valid root or not
# 2021-11-07	WH	Runs deletion routine for users and games whenever a new game is created
# 2021-11-06	WH	Sheet builder and new game subdomain of playing_online
# 2021-11-06	WH	New game route now uses userID and gameID generators in gameplay.py
# 2021-10-31	WH	Zeros no longer allowed in gameID to ensure always 8 digits
# 2021-10-31	WH	Spelling corrections
# 2021-10-29	WH	Added game object deletion routine (Issue#90)
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
# 2021-09-26	WH	Added game finished event to forward to results page
# 2021-09-25	WH	Now sends list of invalid retaliations with action declare
# 2021-09-25	WH	Data classes now also define the future tense version of the event name for the popup
# 2021-09-19	WH	Added comments and tidy code
# 2021-09-19	WH	Added retaliation system for all other retaliation options
# 2021-09-18	WH	Added equation parser script
# 2021-09-18	WH	Dataclasses now contain an expression that is parsed to calculate how each action effects all the cash containers
# 2021-09-17	WH	standardized reference to item names so, for example, kill is referenced as itmKill everywhere
# 2021-09-17	WH	Changed perpetrate_<action> events to notify events as this makes more sense
# 2021-09-17	WH	Major overhaul of action definitions as they are now in data classes
# 2021-09-02	WH	Now handles Kill, Gift, Swap and Steal
# 2021-09-02	WH	Added handling for special action declaration
# 2021-08-28	WH	Added handling for Money, Bank and Bomb items being selected
# 2021-08-28	WH	Added method to respond to the pushing of the NEXT-ROUND button
# 2021-08-28	WH	Added function to generate the sequence of squares
# 2021-08-24	WH	Playing game draw-grid function now operates as intended
# 2021-08-23	WH	Began work on online play draw grid function
# 2021-08-19	WH	Added pop-up to warn users if they are already signed in in another tab
# 2021-08-05	WH	Converted application to use sqlite in-memory database to track active games
# 2021-08-05	WH	Grid is added to user database when sheet is submitted and user is redirected
# 2021-08-05	WH	Adds user to active users database when they join a game from the join game screen
# 2021-08-05	WH	Create system to query database when join game requested
# 2021-08-05	WH	Create link to MySQL database
# 2021-08-02	WH	Added nickname validator routine which, if successful, redirects user to /playing_online/sheet_builder
# 2021-08-02	WH	Converted application to socketio application
# 2021-07-09	WH	Added code to generate and serve basic playing grid
# 2021-07-08	WH	Added very basic flask server structure
#---------------------------------------------------------------------#
#=========================================================#
#^ Imports Modules ^#
from flask import Flask, render_template, Markup, send_file, request, make_response, redirect
import json
import time

from sqlalchemy.sql.functions import user
#from app.database import activeGames

import gameplay
import database
from game_items import *

#=========================================================#
#^ Configure flask webserver ^#
app = Flask(__name__)
app.config['SECRET_KEY'] = '0nOxRU2ipDewLH1d'

usersTBL = database.activeUsers
gamesTBL = database.activeGames
statsTBL = database.statistics

#---------------#
GAMEVERSION = "0.1.0(B)"

#=========================================================#
#^ URL routes ^#
#---------------#
# The index page


@app.route("/")
def index():
    TotalGames = database.statistics.getTotalGames()
    CalcActiveGames = database.statistics.calcActiveGames()
    return render_template("index.html", currentActiveGames=CalcActiveGames, totalGames=TotalGames, version=GAMEVERSION)

#---------------#
# Error pages


@app.route("/error")
def error():
    code = request.args.get("code")
    message = gameplay.parsers().getERROR(code)  # Get error message from code
    return render_template("errors/error_base.html", message=message)

#---------------#


@app.route("/playing_online", methods=["GET", "POST"])
def play_game():
    # Below variables should be set to match the error class in the event of an error
    nicknameError = ""
    IDError = ""
    popupHTML = ""

    # Get information from form
    nickname = request.form.get("ipt_nickname")
    gameID = request.form.get("ipt_game_ID")
    # The value on the submit button (changed if in answer to popup)
    submitButton = request.form.get("submit_button")

    if request.method == "POST":
        userSID = request.cookies.get("SID")  # Loads from client cookies

        # Check if the user has answered that they wish to use a new SID (in which case delete all reference to old SID)
        if submitButton == "Playing here instead":
            queryData = database.gameDB.query(usersTBL).filter(usersTBL.user_id==userSID)
            userObject = queryData.first()
            if userObject.is_host == True:  # Delete their old game if that were the host
                database.gameDB.query(gamesTBL).filter(gamesTBL.game_id==userObject.user_game_id).delete()
            queryData.delete()

        # Check if the SID stored in the user's cookies is still present in the active database
        elif userSID != None:
            if database.get_user(userSID) != None:
                popupHTML = render_template("popups/user_still_active_popup.html")
                return render_template("playing_online/join_game.html", nicknameErrClass=nicknameError, gameIDErrClass=IDError, nickname=nickname, gameID=gameID, CSSPopup=Markup(popupHTML))

        #---------------#
        if gameplay.validators().gameIDValidate(gameID):
            if gameplay.validators().nicknameValidate(nickname):
                # Saves user details to database
                userSID = gameplay.generators().generate_SID()

                deletionTime = database.get_deletion_time() # Get the deletion time

                # Build new database entry using base class
                newUserActivate = usersTBL(user_id=userSID, user_nickname=nickname, user_game_id=gameID, is_host=False, deletion_time=deletionTime)
                database.gameDB.add(newUserActivate)
                database.gameDB.commit()

                #-#
                # Move on to sheet builder page
                response = redirect(f"/playing_online/sheet_builder?gid={gameID}")
                # Save SID for later use
                response.set_cookie("SID", str(userSID))
                return response
            else:
                nicknameError = "inputError"
        else:
            IDError = "inputError"
    else:  # Ensure boxes are blank when page is loaded for the first time
        nickname = ""
        gameID = ""

    return render_template("playing_online/join_game.html", nicknameErrClass=nicknameError, gameIDErrClass=IDError, nickname=nickname, gameID=gameID, CSSPopup="")

#---------------#
@app.route('/playing_online/new_game', methods=["GET", "POST"])
def new_game():
    if request.method == "POST":
        # Colleting Item data from POST
        gameData = request.form.get("game_data")
        gameData = gameData.split("|")
        sliderData = gameData[0]
        itemData = gameData[1]
        nickname = request.form.get("nickname")

        if gameplay.validators().nicknameValidate(nickname):
            # Check database for old games and users pending deletion
            database.clean_active()
            
            #-#
            # Generate random IDs
            gameID = gameplay.generators().generate_gameID()
            gameIDString = str(gameID).zfill(8)
            userSID = gameplay.generators().generate_SID()

            #-#
            #Get the default deletion times for apps
            deletionTime = database.get_deletion_time()

            #-#
            # Commit to database
            newGame = gamesTBL(game_id=gameID, host_id=userSID,grid_settings=sliderData, game_items=itemData, deletion_time=deletionTime)
            newUser = usersTBL(user_id=userSID, user_game_id=gameID,user_nickname=nickname, is_host=True, deletion_time=deletionTime)

            database.gameDB.add(newGame)
            database.gameDB.add(newUser)
            database.gameDB.commit()

            database.statistics.incrementTotalGames()

            # Redirects to sheet builder page
            response = redirect(f"/playing_online/sheet_builder?gid={gameIDString}")
            response.set_cookie("SID", str(userSID))  # Save SID for later use

            return response

    return render_template("playing_online/new_game.html")

#---------------#
@app.route("/playing_online/sheet_builder", methods=["GET", "POST"])
@gameplay.validators.pageControlValidate()
def game_sheet():
    # Load values from client provided info
    userSID = request.cookies.get("SID")  # Loads from client cookies
    gameID = request.args.get("gid")  # Loads from URL bar

    # If a user's sheet is already full, move them on
    if database.gameDB.query(usersTBL).filter(usersTBL.user_grid != None, usersTBL.user_id == userSID).first() != None:
        return redirect(f"/playing_online/lobby?gid={gameID}")

    #-#
    # Queries and retries required data from database
    gameData = database.get_game(gameID)

    # Gets raw strings
    itemsString = gameData.game_items
    gridString = gameData.grid_settings

    # Converts strings to JSON form
    gridJSON = json.loads(gridString)
    itemsJSON = json.loads(itemsString)

    # Handles grid that gets sent back
    if request.method == "POST":
        retrievedGrid = request.form.get("grid")
        # Checks that number of items in grid matches its size
        if gridJSON["GRID_X"] * gridJSON["GRID_Y"] == len(retrievedGrid.split(",")):
            database.get_user(userSID).user_grid = retrievedGrid
            database.gameDB.commit()
            return redirect(f"/playing_online/lobby?gid={gameID}")

    gridHTML = gameplay.generators().html.buildEditableGrid(gridJSON["GRID_X"], gridJSON["GRID_Y"])  # Builds grid using values from loaded JSON

    return render_template("playing_online/sheet_builder.html", grid=gridHTML, itemsMaxJSON=itemsJSON, gridSizeJSON=gridJSON)

#---------------#
@app.route("/tutorial")
def tutorial():
    return render_template("accessory/tutorial.html")

#---------------#
@app.route("/about")
def about_page():
    return render_template("accessory/about.html")

#---------------#
@app.route("/patch_notes")
def patch_notes():
    return render_template("accessory/patch_notes.html")

@app.route("/patch_notes/<version>")
def versioninfo(version):
    print(version)
    try:
        f=open(f"static/patchnotes/{version}.txt","r") 
        displayhtml = gameplay.parsers.convertTxtToHtml(f)
        return render_template("accessory/patch_notes_base.html", body=displayhtml, title=version)
    except:
        return redirect("/error?code=VERSIONINVALID")



#---------------#
@app.route("/playing_online/lobby")
@gameplay.validators.pageControlValidate()
def lobby():
    # Redirect away if the user does not have correct cookies
    if request.cookies.get("SID") == None:
        return redirect("/error?code=NOSID")

    try:
        gameID = request.args.get("gid")
        gameLine = database.get_game(gameID)
        if gameLine.is_open == False:
            return redirect(f"/playing_online/game?gid={gameID}")
        host_id = gameLine.host_id
        hostNick = database.get_user(host_id).user_nickname
        host_content = ""
        # Renders host-only controls if the user is the host
        if gameplay.validators().isHost(request.cookies.get("SID"), request.args.get("gid")):
            host_content = Markup(render_template(
                "playing_online/host_only/host_only_lobby.html"))

        return render_template("playing_online/lobby.html", host_only_content=host_content, gameID=gameID, hostNick=hostNick)
    except AttributeError:  # Redirect away if game does not exist
        return redirect("/error?code=GAMEINVALID")

#---------------#
@app.route("/playing_online/game")
@gameplay.validators.pageControlValidate()
def game():
    gameID = request.args.get("gid")
    userID = request.cookies.get("SID")

    try:
        if gameplay.validators().isFinished(gameID):
            return redirect(f"/playing_online/results?gid={gameID}")

        gameLine = database.get_game(gameID)
        hostID = gameLine.host_id
        hostNick = database.get_user(hostID).user_nickname

        # Gets grid information from relevant database
        gridSerial = database.get_user(userID).user_grid
        gridSettingsJSON = json.loads(gameLine.grid_settings)
        gridX = int(gridSettingsJSON["GRID_X"])
        IMAGE_URLS = {  # Defines the locations of the images associated with the following items
            "M5000": money(5000).IMAGE_LOCATION,
            "M1000": money(1000).IMAGE_LOCATION,
            "M500": money(500).IMAGE_LOCATION,
            "M200": money(200).IMAGE_LOCATION,
            "itmKill": itmKill.IMAGE_LOCATION,
            "itmSwap": itmSwap.IMAGE_LOCATION,
            "itmSteal": itmSteal.IMAGE_LOCATION,
            "itmGift": itmGift.IMAGE_LOCATION,
            "itmBank": itmBank.IMAGE_LOCATION,
            "itmBomb": itmBomb.IMAGE_LOCATION,
            "itmShield": itmShield.IMAGE_LOCATION,
            "itmMirror": itmMirror.IMAGE_LOCATION
        }
        usersGrid = gameplay.generators().html.drawGameplayGrid(gridX, gridSerial, IMAGE_URLS)  # Gets the HTML for the grid to draw

        #-#
        if gameplay.validators().isHost(userID, gameID):
            return render_template("playing_online/host_only/playing_online_host.html", grid=usersGrid, hostNick=hostNick, mySID=userID)
        else:
            return render_template("playing_online/online_game.html", grid=usersGrid, hostNick=hostNick, mySID=userID)
    except AttributeError:
        return redirect("/error?code=GAMEINVALID")

#---------------#
@app.route("/playing_online/results")
@gameplay.validators.pageControlValidate()
def results():
    # fetches user data
    gameID = request.args.get("gid")

    if gameplay.validators().isFinished(gameID):
        userscores = json.loads(database.get_game(gameID).results_json)

        sorted_scores = dict(sorted(userscores.items(), key=lambda x: x[1], reverse=True))
        final_scores_table = "<table class=\"sidebarscores\"> <tr class=\"ResultsTableHeader\"> <td></td><td> Player </td> <td> Final Cash </td> </tr> "
        placing = 1
        podiumscores = {}
        for name, score in sorted_scores.items():
            if placing <= 3:
                podiumscores[name] = score
            else:
                final_scores_table += f"<tr> <td>{placing}</td> <td> {name} </td> <td> £{score} </td> </tr>"
            placing += 1
        final_scores_table += "</table>"
        response = make_response(render_template("playing_online/results.html",results_table=Markup(final_scores_table), podiumscores=podiumscores))
        response.delete_cookie("SID")
        return response

    return redirect("/error?code=GAMEONGOING")


#=========================================================#
#^ Main app execution ^#