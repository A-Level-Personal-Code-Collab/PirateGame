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
 * 2021-08-28	WH	Added handling for cash and bank updates
 * 2021-08-28	WH	Added handling for new_square event
 */
 //=========================================================//
 //^ Gets elements from page ^//
 const cashBox = document.getElementById("p_cashText")
 const bankBox = document.getElementById("p_bankText")
 const logBox = document.getElementById("p_logText")

 //=========================================================//
 //^ Variables ^//
 var socket = io.connect('https://localhost:5000');
 var previousSquare = null;
 var cashTotal = 0;
 var recordedCash = 0;
 var bankTotal = 0;
 var recordedBank = 0; //Keeps track of the last value recorded on the page

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
    socket.on('cash_update', newsum => {cashTotal = newsum})
    socket.on('bank_update', newsum => {bankTotal = newsum; recordedBank = 999}) //Change recorded bank variable to impossible value to force recording of bank value
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
    setTimeout(update_money, 2000) //Delay here immitates the time that animation would be taking
 }

 //Updates values in cash and bank boxes
 function update_money()
 {
     if (cashTotal != recordedCash) {if (cashBox.innerHTML == "") {cashBox.innerHTML = cashTotal} else {cashBox.innerHTML = cashBox.innerHTML + `, ${cashTotal}`}} //Adds commas only if box is not empty
     if (bankTotal != recordedBank) {if (bankBox.innerHTML == "") {bankBox.innerHTML = bankTotal} else {bankBox.innerHTML = bankBox.innerHTML + `, ${bankTotal}`}}
     recordedBank = bankTotal
     recordedCash = cashTotal
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