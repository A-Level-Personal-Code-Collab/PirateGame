/**
 * File: /home/will/GitHub Repos/PirateGame/static/javascript/online_game.js
 * Project: /home/will/GitHub Repos/PirateGame/static/javascript
 * Created Date: Saturday, August 28th 2021, 3:12:37 pm
 * Author: Will Hall
 * -----
 * Last Modified: Sat Aug 28 2021
 * Modified By: Will Hall
 * -----
 * Copyright (c) 2021 Lime Parallelogram
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 * 2021-08-28	WH	Added handling for new_square event
 */
 //=========================================================//
 //^ Gets elements from page ^//

 //=========================================================//
 //^ Variables ^//
 var socket = io.connect('https://localhost:5000');
 var previousSquare = null;

 //=========================================================//
 //^ OnLoad Function ^//
 function on_load()
 {
    var gameID = getUrlVar("gid")
    var userSID = getCookie("SID")

    /*---------------*/
    //Adds event listeners for socket events
    socket.on('connect', () => {
        socket.emit("join",{userSID: userSID, gameID: gameID}) //Sends join event to server which causes the user to get added to a room
    })

    socket.on('new_square', select_sqaure)
 }

 //=========================================================//
 //^ Slave Subs ^//
 /*---------------*/
 //Lights up a selected square and greys-out the old one
 function select_sqaure(serialSquareNum)
 {
    var square = document.getElementById(`square${serialSquareNum}`);

    square.classList.add("selected"); //Lights up currently selected square

    //Greys-out passed squares
    if (previousSquare)
    {
        previousSquare.classList.remove("selected");
        previousSquare.classList.add("completed");
    }

    previousSquare = square;
 }

 //=========================================================//
 //^ Copied functions to gain data from browser ^//
 //Gets cookie and splits it to individual cookies
 const getCookie = (name) => {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim().split('=');
        if (c[0] === name) {
            return c[1];
        }
    }
    return "";
}

//Gets values from url
function getUrlVar(name) {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars[name];
}

 //=========================================================//
 //^ Starts onLoad ^//
 on_load();