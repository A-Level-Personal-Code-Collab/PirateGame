#---------------------------------------------------------------------#
# File: https://github.com/A-Level-Personal-Code-Collab/PirateGame/app/gameserver.py
# Project: https://github.com/A-Level-Personal-Code-Collab/PirateGame
# Created Date: Saturday, November 6th 2021, 1:42:01 pm
# Description: A dedicated socketio game handling server
# Author: Will Hall
# Copyright (c) 2021 Lime Parallelogram
# -----
# Last Modified: Mon Dec 20 2021
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2021-11-19	WH	Added the session getter decorator to all functions to automatically get the database session and pass it in a parameter
# 2021-11-15	WH	Commented out host left popup for release
# 2021-11-11	WH	Added automatic database check
# 2021-11-09	WH	Send the delay information to the client along with applicable events (Issue #151)
# 2021-11-09	WH	Implemented constant for the length of time the spinner animation takes
# 2021-11-06	WH	Moved all socketio lines from old flask_main.py
# 2021-11-06	WH	Created file and added test code for new socketio server
#---------------------------------------------------------------------#

import socketio
import eventlet
import json
from time import sleep

import database
import gameplay
from game_items import *

usersTBL = database.activeUsers
gamesTBL = database.activeGames

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)


#=========================================================#
#^ Socketio Functions ^#
#---------------#
#When a user joins a game they get added to the game's room
@sio.event
@database.get_session
def join(session,sid,data):
    gameID = data["gameID"]
    userSID = data["userSID"]
    print(f"New user joined the game {gameID} with a userSID of {userSID}")

    try:
        #Stores user's current socketio SID in database 
        user = database.get_user(session,userSID)
        user.socketio_id = sid
        session.commit()

        sio.enter_room(sid,gameID)

        #Update the user list on all user's screen
        online_users = gameplay.generators().getActiveUsersDictionary(session,gameID)
        sio.emit("users_update", online_users,room=gameID)
        sio.emit("log_update", {"entry": gameplay.loggers().userConnect(user.user_nickname), "delay": 0},room=gameID) #Show log entry if a user leaves
    except AttributeError or ValueError as e:
        sio.emit("ERR", f"User ID ({userSID}) that was submitted was not found in our DB. ERROR: {e}", room=sid)

#---------------#
#When a user gets to disconnect from a page
@sio.event
@database.get_session
def disconnect(session,sid):
    userLine = database.get_user(session,sid)
    if userLine != None:
        gameID = str(userLine.user_game_id).zfill(8)
        #//if gameplay.validators().isHost(userLine.user_id,gameID):
            #//sio.emit("ERR", "The host of this game has left. If they do not return them the game cannot continue.",room=gameID)
        #//else:
        userLine.socketio_id = None
        if userLine.user_pending_declaration:
            gameLine = database.get_game(session,gameID)
            if gameplay.functions().actionComplete(gameLine): #Completed action and runs event if this completed a round
                sio.emit("round_complete", {"delay": 0}, room=gameID)

        userLine.user_pending_declaration = False
        #Update the user list on all user's screen
        session.commit()
        online_users = gameplay.generators().getActiveUsersDictionary(session,gameID)
        sio.emit("users_update", online_users,room=gameID)
        sio.emit("log_update", {"entry": gameplay.loggers().userDisconnect(userLine.user_nickname), "delay": 0},room=gameID)
            

#---------------#
#When the host opts to start the game (from lobby)
@sio.event
@database.get_session
def start(session,sid,data):
    gameID = data["gameID"]
    userSID = data ["userSID"]

    if gameplay.validators().isHost(session,userSID,gameID): #Confirms if user is host and re-broadcasts start event
        sio.emit("start",room=gameID)

        #Load grid data from database
        gameData = database.get_game(session,gameID)
        gridJSON = json.loads(gameData.grid_settings)
        gridSize = int(gridJSON["GRID_X"])*int(gridJSON["GRID_Y"])

        #Generate grid order
        gpClass = gameplay.generators()
        order = gpClass.generate_playOrder(gridSize)

        #Add selection order ro database
        gameData.square_order = order
        gameData.current_round = 0

        #Close game
        gameData.is_open = False
        
        session.commit()
    
    else:
        sio.emit("ERR", "User ID that was submitted is not the host of this game. Have you attempted to join a second game?", room=sid)

        

#---------------#
# When the host presses button to move on to next round
@sio.event
@database.get_session
def next_round(session,sid):
    ANIMATION_LENGTH = 3000#ms - Time the animation takes to complete
    gameID = database.get_user(session,sid).user_game_id #Find game ID by querying based on sid
    gameIDString = str(gameID).zfill(8) #Adds leading zeros to gameID for the purpose of room function
    gameObject = database.get_game(session,gameID) #Load game information from database
    currentRound = gameObject.current_round +1
    allSquares = gameObject.square_order.split(",")

    if currentRound > len(allSquares):
        gameplay.events().gameEnd(session,gameID)
        sio.emit("game_complete", room=gameIDString)

    else:
        square = allSquares[currentRound-1]
        sio.emit("new_square", square, room=gameIDString) #Send selected square to clients

        all_players = database.get_players(session,gameID)
        actionsRequired = 0 #Used to track whether the next round can begin immediately

        for player in all_players:
            playerGrid = player.user_grid.split(",")
            item = playerGrid[int(square)]

            #---------------#
            #Handle money items
            if money(200).identify(item): #Use the identify method from data class
                denomination = item[1:] #Get the denomination value by removing the 'M' from the ID
                note = money(int(denomination)) #Get instance of data class
                player.user_cash = note.cash_update(player.user_cash) #Update player's cash value in database
                sio.emit("cash_update", {"value": player.user_cash,"delay":ANIMATION_LENGTH}, room=player.socketio_id) #Send cash update event
            #---------------#
            #Iterate through all action classes and process them
            for action in actionItem.__subclasses__():
                instance = action()
                if instance.identify(item): #Use the identify method to test if the action in question is the desired action
                    if not action.TARGETTED: #For actions that do not have target selectors, apply them immediately
                        actionExpression, null = instance.get_expressions() #Get the expression, discarding the second half as it doesn't have a second player involved
                        player.user_cash, player.user_bank , null, null = gameplay.parsers().parse_money(actionExpression,player) #Parse expression
                        sio.emit('log_update', {"entry": instance.get_log(player.user_id,None), "delay": ANIMATION_LENGTH}, room=player.socketio_id)
                        sio.emit("cash_update", {"value": player.user_cash,"delay":ANIMATION_LENGTH}, room=player.socketio_id) #Run cash updates
                        sio.emit("bank_update", {"value": player.user_bank,"delay":ANIMATION_LENGTH}, room=player.socketio_id)
                    elif gameplay.validators().isOnline(session,player.user_id): #Only handle actionable events if they are online
                        actionsRequired += 1
                        player.user_pending_declaration = True
                        event, data = instance.get_itemNotify() #For actions that are targetted, notify the client that they have one of these
                        data["delay"] = ANIMATION_LENGTH
                        sio.emit(event, data,room=player.socketio_id)
                    break #Break loop after detecting correct item to save resources
            
            #---------------#
            #Iterate through retaliation actions to identify if the user has one of those
            for action in retaliatoryAction.__subclasses__():
                instance = action()
                if instance.identify(item):
                    player.available_retaliations = f"{player.available_retaliations},{item}"
                    event, data = instance.get_itemNotify() #Notify client that they have a retaliation option
                    data["delay"] = ANIMATION_LENGTH
                    sio.emit(event, data,room=player.socketio_id)

        #---------------#
        if actionsRequired == 0:
            sio.emit("round_complete", {"delay":ANIMATION_LENGTH}, room=gameIDString)
        else:
            gameObject.round_remaining_actions = actionsRequired

        #---------------#
        #Update values in database to newest
        gameObject.current_round = currentRound
    
    session.commit()

#---------------#
#Handles when somone declares their action item
@sio.event
@database.get_session
def action_declare(session,sid,data):
    targetSID = data["target"]
    actionIdentifier = data["action"] #The type of action we are dealing with
    perpetrator = database.get_user(session,sid) #Get a table row representing the perpetrator's information
    gameID = perpetrator.user_game_id #Find game ID by querying based on sid
    gameIDString = str(gameID).zfill(8) #Adds leading zeros to gameID for the purpose of room function
    invalidRetals = ""
    
    #---------------#
    #Handling for once a target has been selected
    if targetSID != "": #If the declaration includes the target information
        target = database.get_user(session,targetSID) #Gets a database record object of the target

        for actionType in actionItem.__subclasses__():
            instance = actionType()
            if instance.identify(actionIdentifier):
                target.user_pending_expression, perpetrator.user_pending_expression = instance.get_expressions() #Save the expression information to the database based on what event has taken place
                invalidRetals = ",".join(instance.INVALID_RETALIATIONS)
                logEntry = instance.get_log(targetSID,perpetrator.user_id) #Log the action to the logs
                if not gameplay.validators().isOnline(session,target.user_id): #Automatically commit action if user is offline
                    moneyHandlingExpression = target.user_pending_expression+":"+perpetrator.user_pending_expression #Create combined expression for money that tells what happens to both parties
                    target.user_cash, target.user_bank, perpetrator.user_cash, perpetrator.user_bank = gameplay.parsers().parse_money(moneyHandlingExpression, target, perpetrator)
                    for user in [target,perpetrator]:
                        user.user_pending_expression = ""
                        #Updates the cash boxes of both the perpetrator and victim
                        sio.emit("cash_update", {"value": user.user_cash,"delay":0}, room=user.socketio_id)
                        sio.emit("bank_update", {"value": user.user_bank,"delay":0}, room=user.socketio_id)

                    if gameplay.functions().actionComplete(database.get_game(session,gameID)): #Completed action and runs event if this completed a round
                        sio.emit("round_complete", {"delay":0},room=gameIDString)
                break # Break to save resources

        session.commit()

        #Updates the log
        sio.emit('log_update', {"entry": logEntry, "delay": 0}, room=gameIDString)
    
    emitData = eval(f"{actionIdentifier}().get_declareData()") #Uses the dataclass system to get the propper grammer for the popup message
    #Add information about target and perpetrator to the base information about the target and perpetrator
    emitData["target"] =targetSID
    emitData["perpetrator"] =perpetrator.user_id
    
    sio.emit('action_declare', emitData, room=gameIDString) #Re-broadcast event to enforce popup

#---------------#
#Handles when a client declares their response to an action being done against them
@sio.event
@database.get_session
def retaliation_declare(session,sid,data):
    victim = database.get_user(session,sid) #Load victim from database
    perpetrator = session.query(usersTBL).filter(usersTBL.user_game_id==victim.user_game_id, usersTBL.user_pending_expression != "", usersTBL.user_id != victim.user_id).first() #Find perpetrator based on the fact that they too will have changes to their pending

    moneyHandlingExpression= victim.user_pending_expression+":"+perpetrator.user_pending_expression #Create combined expression for money that tells what happens to both parties
    gameID = perpetrator.user_game_id #Find game ID from perpetrator
    gameIDString = str(gameID).zfill(8) #Adds leading zeros to gameID for the purpose of room function
    retal_type = data["type"] #Gets the string dictating the clients response
    aktvGame = database.get_game(session,gameID)

    #---------------#
    #Loops through available retaliations to check if it matches any of those
    if retal_type != "none":
        for action in retaliatoryAction.__subclasses__():
            instance = action()
            if instance.identify(retal_type):
                availableRetals = victim.available_retaliations.split(",")
                if retal_type in availableRetals:
                    availableRetals.remove(retal_type)
                    victim.available_retaliations = ",".join(availableRetals)
                    moneyHandlingExpression = instance.expression_manipulate(moneyHandlingExpression) #Change the money handling expression based on what is dictated in the retaliation's data class
                    sio.emit("log_update", {"entry": instance.get_log(victim.user_id,perpetrator.user_id), "delay":0},room=gameIDString) #Add retaliation log entry
                    sio.emit("retaliation_declare", instance.get_pushback_dat(),room=gameIDString)
                    break #Break to save resources

    #---------------#
    #Actually parse new (or un-updated) money expression to new cash values
    victim.user_cash, victim.user_bank, perpetrator.user_cash, perpetrator.user_bank = gameplay.parsers().parse_money(moneyHandlingExpression, victim, perpetrator)

    #---------------#
    #Send cash updates and bank updates to users as well as resetting their pending expression
    for user in [victim,perpetrator]:
        user.user_pending_expression = ""

        #Updates the cash boxes of both the perpetrator and victim
        sio.emit("cash_update", {"value": user.user_cash, "delay": 0}, room=user.socketio_id)
        sio.emit("bank_update", {"value": user.user_bank, "delay": 0}, room=user.socketio_id)

    if gameplay.functions().actionComplete(aktvGame): #Completed action and runs event if this completed a round
        sio.emit("round_complete",{"delay": 0}, room=gameIDString)

    session.commit()

if __name__ == "__main__":
    database.check_tables()
    eventlet.wsgi.server(eventlet.listen(("", 5000)), app)