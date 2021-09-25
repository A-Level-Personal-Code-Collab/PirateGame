/**
 * File: https://github.com/Lime-Parallelogram/PirateGame/static/javascript/lobby.js
 * Project:https://github.com/Lime-Parallelogram/PirateGame
 * Created Date: Monday, August 9th 2021, 12:12:44 pm
 * Author: Will Hall
 * -----
 * Last Modified: Sat Sep 25 2021
 * Modified By: Will Hall
 * -----
 * Copyright (c) 2021 Lime Parallelogram
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 * 2021-09-25	WH	Disables start button if number of users is too small
 * 2021-08-28	WH	Join event now sends userID to server also
 * 2021-08-09	WH	Added fetch function to pull data from the active users
 */
 const listDiv = document.getElementById("div_listContainer");
 const btn_BeginGame = document.getElementById("start_button")

 const MIN_USERS = 3;

 var socket = io.connect('https://localhost:5000'); //Connects to server's socket server
 
 //=========================================================//
 //^ Performs user functions ^//
 //Runs on-load
 function on_load()
 {
    var gameID = getUrlVar("gid")
    var userSID = getCookie("SID")

    /*---------------*/
    //Adds event listeners for socket event
    socket.on('connect', () => {
        socket.emit("join",{userSID: userSID, gameID: gameID}) //Sends join event to server which causes the user to get added to a room
    })
    
    socket.on('message', msg => { //Updates list to match incomming messahe
        listDiv.innerHTML = msg;

        //Disabes start button if number of users is below the threshold
        var numPeople = document.querySelector(".names_list").querySelectorAll("li").length;
        if (!!btn_BeginGame) //Check button is not null
        {
            if (numPeople < MIN_USERS){
                btn_BeginGame.disabled=true;
            }
            else
            {
                btn_BeginGame.disabled=false;
            }
        }
        
    })

    socket.on('start', function () {window.location.href = `/playing_online/game?gid=${gameID}`}) //Starts game if game event is recieved
 }

 /*---------------*/
 //Sends start game event when start button is clicked (HOST ONLY)
 function start_game()
 {
     socket.emit("start",{userSID: getCookie("SID"), gameID: getUrlVar("gid")})
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
 //^ Runs onload functions ^//
 on_load();
