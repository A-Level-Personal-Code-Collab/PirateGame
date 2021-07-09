#---------------------------------------------------------------------#
# File: /home/will/GitHub Repos/PirateGame/flask_main.py
# Project: /home/will/GitHub Repos/PirateGame
# Created Date: Thursday, July 8th 2021, 4:38:56 pm
# Description: Main flask wedserver root.
# Author: Will Hall
# Copyright (c) 2021 Lime Parallelogram
# -----
# Last Modified: Fri Jul 09 2021
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2021-07-08	WH	Added very basic flask server structure
#---------------------------------------------------------------------#
#Imports modules 
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)