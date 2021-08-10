/**
 * File: https://github.com/Lime-Parallelogram/PirateGame/static/javascript/lobby.js
 * Project:https://github.com/Lime-Parallelogram/PirateGame
 * Created Date: Monday, August 9th 2021, 12:12:44 pm
 * Author: Will Hall
 * -----
 * Last Modified: Mon Aug 09 2021
 * Modified By: Will Hall
 * -----
 * Copyright (c) 2021 Lime Parallelogram
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 * 2021-08-09	WH	Added fetch function to pull data from the active users
 */
 const listDiv = document.getElementById("div_listContainer");

 //=========================================================//
 //^ Performs user functions ^//
 //Runs on-load
 function on_load()
 {
    var socket = io.connect('https://localhost:5000')
    socket.on('connect', () => {
        socket.emit("join","00000001")
    })
    
    socket.on('message', msg => {
        listDiv.innerHTML = msg;
    })
 }

 //=========================================================//
 //^ Runs onload functions ^//
 on_load();