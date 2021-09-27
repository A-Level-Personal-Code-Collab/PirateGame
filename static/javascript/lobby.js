/**
 * File: https://github.com/Lime-Parallelogram/PirateGame/static/javascript/lobby.js
 * Project:https://github.com/Lime-Parallelogram/PirateGame
 * Created Date: Monday, August 9th 2021, 12:12:44 pm
 * Author: Will Hall
 * -----
 * Last Modified: Mon Sep 27 2021
 * Modified By: Will Hall
 * -----
 * Copyright (c) 2021 Lime Parallelogram
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 * 2021-09-27	WH	Added leave page confirmation
 * 2021-09-26	WH	Added dynamic socketio address
 * 2021-09-26	WH	Added music plaback control
 * 2021-09-25	WH	Disables start button if number of users is too small
 * 2021-08-28	WH	Join event now sends userID to server also
 * 2021-08-09	WH	Added fetch function to pull data from the active users
 */
 const listDiv = document.getElementById("div_listContainer");
 const btn_BeginGame = document.getElementById("start_button");
 const mcontrol_btn = document.getElementById("ipt_musicControl")
 const musicPlayer = new Audio(`${window.location.origin}/static/audio/lobby_backing.ogg`)
 const MIN_USERS = 3;

 var socket = io.connect(window.location.origin); //Connects to server's socket server
 var musicState = true;
 var intentionalForward = false; //Sets whether the forwarding is intended
 
 //=========================================================//
 //^ Performs user functions ^//
 //Runs on-load
 function on_load()
 {
    //Adds leave page confirmation
    window.addEventListener("beforeunload", function(event) {if (!intentionalForward) {event.returnValue = "Do you reall wish to leave this site?"; return "Do you reall wish to leave this site?";}});
    
    /*---------------*/
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

    socket.on('start', function () {intentionalForward = true; window.location.href = `/playing_online/game?gid=${gameID}`}) //Starts game if game event is recieved

    /*---------------*/
    //Handles background music playback
    mcontrol_btn.addEventListener("click", musicToggle)
    musicPlayer.loop = true
    musicPlayer.play()
 }

 /*---------------*/
 //Sends start game event when start button is clicked (HOST ONLY)
 function start_game()
 {
     socket.emit("start",{userSID: getCookie("SID"), gameID: getUrlVar("gid")})
 }

 /*---------------*/
 //Toggles background music on click of button
 function musicToggle()
 {
     musicState = !musicState
     if (musicState) {(musicPlayer.play())} else {musicPlayer.pause()}
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
