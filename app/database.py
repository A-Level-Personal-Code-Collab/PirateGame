#---------------------------------------------------------------------#
# File: https://github.com/A-Level-Personal-Code-Collab/PirateGame/app/database.py
# Project: https://github.com/A-Level-Personal-Code-Collab/PirateGame/app
# Created Date: Saturday, November 6th 2021, 2:55:28 pm
# Description: A single python file that dictates how the database behaves in the app
# Author: Will Hall
# Copyright (c) 2021 Lime Parallelogram
# -----
# Last Modified: Fri Nov 19 2021
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2021-11-19	WH	Created session getter decorator for other files
# 2021-11-19	WH	Allowed all functions to accept a session as a parameter and use this to perform functions
# 2021-11-19	WH	Removed global session
# 2021-11-11	WH	Added function to automatically create databases if they don't exist
# 2021-11-08	WH	Added functionality to execute this file in order to reset all tables in the database
# 2021-11-07	WH	Added function to clean old users and games from database
# 2021-11-06	WH	Added database models and connected to new mysql server
#---------------------------------------------------------------------#
#=========================================================#
#^ Imports libraries ^#
from functools import wraps
import sqlalchemy
from sqlalchemy.engine.create import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session
from sqlalchemy.orm.session import sessionmaker
import time
from sqlalchemy import func

#=========================================================#
#^ Setup database connection engine ^#
gameDB_engine = create_engine("mariadb+pymysql://pirategame_python:local-only@pirategame_dbsvr1/pirategame")
#gameDB = sessionmaker(bind=gameDB_engine)()
modelBase = declarative_base()

#=========================================================#
#^ Database table models ^#
#(these are required by SQL alchemy to interact with database so the variable names and info must correspond with your database)
#---------------#
#The table that stores a log of all currently active games
class activeGames(modelBase):
    __tablename__ = 'active_games'
    game_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    host_id = sqlalchemy.Column(sqlalchemy.Integer)
    grid_settings = sqlalchemy.Column(sqlalchemy.String(100))
    game_items = sqlalchemy.Column(sqlalchemy.String(900))
    current_round = sqlalchemy.Column(sqlalchemy.Integer)
    square_order = sqlalchemy.Column(sqlalchemy.String(300))
    round_remaining_actions = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    results_json = sqlalchemy.Column(sqlalchemy.JSON)
    is_open = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    deletion_time = sqlalchemy.Column(sqlalchemy.Integer,default=-1)

#---------------#
#The table that stores a log of all active users and their grids
class activeUsers(modelBase):
    __tablename__ = 'active_users'
    user_nickname = sqlalchemy.Column(sqlalchemy.String(15))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    socketio_id = sqlalchemy.Column(sqlalchemy.String(100))
    user_game_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_grid = sqlalchemy.Column(sqlalchemy.String(9999))
    is_host = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    user_cash = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    user_pending_expression = sqlalchemy.Column(sqlalchemy.String(250), default="")
    user_pending_declaration = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    user_bank = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    available_retaliations = sqlalchemy.Column(sqlalchemy.JSON)
    deletion_time = sqlalchemy.Column(sqlalchemy.Integer, default=-1)


#---------------#
#The Database which stores the statistics of the game
class statisticsDB(modelBase):
    __tablename__ = 'statistics'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    contents_info = sqlalchemy.Column(sqlalchemy.String(100))
    actual_value = sqlalchemy.Column(sqlalchemy.Integer)


#=========================================================#
#^ Database action decorator ^#
def db_action(func):
    def decorator(session, *args,**kwargs):
        output = func(session, *args,**kwargs)
        return output

    return decorator

#=========================================================#
#^ Function used in socketio and flask to generate new session on request ^#
#Creates a new session for each request and then destroys it after the function has executed
def get_session(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        newSession = sessionmaker(bind=gameDB_engine)()
        output = func(newSession, *args, **kwargs)
        newSession.close()
        return output

    return decorator

#=========================================================#
#^ Common database function routines ^#

#---------------#
#Delete and recreate all tables
@db_action
def reset_tables():
    modelBase.metadata.drop_all(bind=gameDB_engine)
    modelBase.metadata.create_all(bind=gameDB_engine)

#---------------#
#Simple getter methods
@db_action
def get_game(session, gameID):
    game = session.query(activeGames).get(int(gameID))
    return game

@db_action
def get_user(session,userID):
    if userID == None:
        return None
    try:
        user = session.query(activeUsers).get(int(userID))
    except ValueError:
        user = session.query(activeUsers).filter(activeUsers.socketio_id==userID).first()
    return user

@db_action
def get_players(session,gameID):
    all = session.query(activeUsers).filter(activeUsers.user_game_id==int(gameID),activeUsers.socketio_id!=None).all()
    return all

@db_action
def delete_players(session,gameID):
    session.query(activeUsers).filter(activeUsers.user_game_id==int(gameID)).delete()
    session.commit()

#---------------#
#Delete old users and games from the database
@db_action
def clean_active(session):
    currentTime = int(time.time())
    session.query(activeGames).filter(activeGames.deletion_time<currentTime).delete()
    session.query(activeUsers).filter(activeUsers.deletion_time<currentTime).delete()
    session.commit()

#---------------#
#Get the time that a new record well be
def get_deletion_time():
    currentTime = int(time.time())
    DEFAULT_DELETION_DELAY = 21000#s - Around 6 hours before a record is deleted

    return currentTime+DEFAULT_DELETION_DELAY

def check_tables():
    modelBase.metadata.create_all(bind=gameDB_engine)
    session = sessionmaker(bind=gameDB_engine)()
    if session.query(statisticsDB).filter(statisticsDB.contents_info=="TotalGames").first() == None:
        totalGames = statisticsDB(id=1, contents_info="TotalGames",actual_value=0)
        session.add(totalGames)
        session.commit()
    session.close()
    print("Successfully recreated all tables")

#=========================================================#
#^ Database query/ manipulation for the home page ^#


class statistics:

    def calcActiveGames(session):
        numActiveGames = session.query(activeGames.game_id).count()
        return numActiveGames
     
    def getTotalGames(session):
        totalgamesfile = session.query(statisticsDB).filter(statisticsDB.id == 1).first().actual_value
        return totalgamesfile

    def incrementTotalGames(session):
        session.query(statisticsDB).filter(statisticsDB.contents_info == "TotalGames").first().actual_value += 1
        session.commit()