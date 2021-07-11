#---------------------------------------------------------------------#
# File: A-Level-Personal-Code-Collab/PirateGame/flask_main.py
# Project: A-Level-Personal-Code-Collab/PirateGame
# Created Date: Thursday, July 8th 2021, 4:38:56 pm
# Description: Main flask webserver root.
# Author: Will Hall
# Copyright (c) 2021 Lime Parallelogram
# -----
# Last Modified: Fri Jul 09 2021
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2021-07-09	WH	Added code to generate and serve basic playing grid
# 2021-07-08	WH	Added very basic flask server structure
#---------------------------------------------------------------------#
#Imports modules 
from flask import Flask, render_template, Markup

app = Flask(__name__)

#=========================================================#
#Slave subs

#---------------#
#Builds the HTML syntax to draw the game grid - makes the grid easily exapandable + avoid typing repetative HTML code
def buildGrid():
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
                grid += f"<td class=\"{CLASS_NAME}\" id=\"tdt_grid{col}{row}\"></td>"
        grid += "</tr>"

    grid += "</table>"

    #Return finnished grid as Markdown and not plain text
    return Markup(grid)

#=========================================================#
#URL routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game")
def game_sheet():
    gridHTML = buildGrid()
    print(gridHTML)
    return render_template("game_sheet.html", grid = gridHTML)

#=========================================================#
#Main app execution
if __name__ == "__main__":
    app.run(debug=True)