#---------------------------------------------------------------------#
# File: /home/will/GitHub Repos/PirateGame/flask_main.py
# Project: /home/will/GitHub Repos/PirateGame
# Created Date: Thursday, July 8th 2021, 4:38:56 pm
# Description: Main flask wedserver root.
# Author: Will Hall
# Copyright (c) 2021 Lime Parallelogram
# -----
# Last Modified: Thu Jul 08 2021
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2021-07-08	WH	Added very basic flask server structure
#---------------------------------------------------------------------#
#Imports modules 
from Flask import Flask, render_template

app = flask(__name__)

@app.route("/")
def index():
    return "Hello Web"

app.run(debug=True)