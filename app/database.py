#---------------------------------------------------------------------#
# File: https://github.com/A-Level-Personal-Code-Collab/PirateGame/app/database.py
# Project: https://github.com/A-Level-Personal-Code-Collab/PirateGame/app
# Created Date: Saturday, November 6th 2021, 2:55:28 pm
# Description: A single python file that dictates how the database behaves in the app
# Author: Will Hall
# Copyright (c) 2021 Lime Parallelogram
# -----
# Last Modified: Thu Nov 11 2021
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2021-11-11	WH	Added function to automatically create databases if they don't exist
# 2021-11-08	WH	Added functionality to execute this file in order to reset all tables in the database
# 2021-11-07	WH	Added function to clean old users and games from database
# 2021-11-06	WH	Added database models and connected to new mysql server
#---------------------------------------------------------------------#
#=========================================================#
#^ Imports libraries ^#
from collections import defaultdict
import socketio
import sqlalchemy
from sqlalchemy.engine.create import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
import time

#=========================================================#
#^ Setup database connection engine ^#
gameDB_engine = create_engine("mariadb+pymysql://pirategame_python:local-only@pirategame_dbsvr1/pirategame")
gameDB = sessionmaker(bind=gameDB_engine)()
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

#=========================================================#
#^ Database action decorator ^#
def db_action(func):
    def decorator(*args,**kwargs):
        try:
            gameDB.commit()
        except:
            pass
        output = func(*args,**kwargs)
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
    gameDB.commit()

#---------------#
#Simple getter methods
@db_action
def get_game(gameID):
    game = gameDB.query(activeGames).get(int(gameID))
    return game

@db_action
def get_user(userID):
    try:
        user = gameDB.query(activeUsers).get(int(userID))
    except ValueError:
        user = gameDB.query(activeUsers).filter(activeUsers.socketio_id==userID).first()
    return user

@db_action
def get_players(gameID):
    all = gameDB.query(activeUsers).filter(activeUsers.user_game_id==int(gameID),activeUsers.socketio_id!=None).all()
    return all

@db_action
def delete_players(gameID):
    gameDB.query(activeUsers).filter(activeUsers.user_game_id==int(gameID)).delete()
    gameDB.commit()

#---------------#
#Delete old users and games from the database
@db_action
def clean_active():
    currentTime = int(time.time())
    gameDB.query(activeGames).filter(activeGames.deletion_time<currentTime).delete()
    gameDB.query(activeUsers).filter(activeUsers.deletion_time<currentTime).delete()
    gameDB.commit()

#---------------#
#Get the time that a new record well be
def get_deletion_time():
    currentTime = int(time.time())
    DEFAULT_DELETION_DELAY = 21000#s - Around 6 hours before a record is deleted

    return currentTime+DEFAULT_DELETION_DELAY

def check_tables():
    modelBase.metadata.create_all(bind=gameDB_engine)
    gameDB.commit()
    print("Successfully recreated all tables")