/**
 * File: /home/will/GitHub Repos/PirateGame/static/javascript/online_game.js
 * Project: /home/will/GitHub Repos/PirateGame/static/javascript
 * Created Date: Saturday, August 28th 2021, 3:12:37 pm
 * Author: Will Hall
 * -----
 * Last Modified: Sat Sep 18 2021
 * Modified By: Will Hall
 * -----
 * Copyright (c) 2021 Lime Parallelogram
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 * 2021-09-17	WH	item_available event replaces perpetrate_kill and perpetrate_steel etc. events
 * 2021-09-17	WH	Changed item names to match the python naming and their names in the dtabase (E.g) kill is now itmKill
 * 2021-09-02	WH	Added handling for log updates
 * 2021-09-02	WH	Added target picker popup
 * 2021-09-02	WH	Added handling for waiting for decision popups
 * 2021-09-02	WH	Added handling for special item updates
 * 2021-08-28	WH	Added handling for cash and bank updates
 * 2021-08-28	WH	Added handling for new_square event
 */
 //=========================================================//
 //^ Gets elements from page ^//
 const cashBox = document.getElementById("p_cashText")
 const bankBox = document.getElementById("p_bankText")
 const logBox = document.getElementById("p_logText")
 const declareButton = document.getElementById("ipt_declare")
 const chooseButton = document.getElementById("ipt_chooseTarget")
 const waitingForActionPopup =  document.getElementById("div_waitingPopup")
 const targetPickerPopup = document.getElementById("div_targetPickerPopup")

 //=========================================================//
 //^ Variables ^//
 var socket = io.connect('https://localhost:5000');
 var previousSquare = null;
 var cashTotal = 0;
 var recordedCash = 0;
 var bankTotal = 0;
 var recordedBank = 0; //Keeps track of the last value recorded on the page
 var declareAction = ""; //The name of the action that is going to be declared
 var targetSelector = false; //Tracks if the user is currently selecting a target

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
    socket.on('log_update', log_update)

    socket.on('itm_available', item_available);

    socket.on('action_declare', action_popup);

    /*---------------*/
    //Adds event listeners for page events
    declareButton.addEventListener("click", declare_action);
    chooseButton.addEventListener("click", declare_target);
 }

 //=========================================================//
 //^ Slave Subs ^//
 /*---------------*/
 //Lights up a selected square and greys-out the old one
 function select_sqaure(serialSquareNum)
 {
    var square = document.getElementById(`square${serialSquareNum}`);
    //var allSquares = document.querySelector("")
    
    square.classList.add("selected"); //Lights up currently selected square

    //Greys-out passed squares
    if (previousSquare)
    {
        previousSquare.classList.remove("selected");
        previousSquare.classList.add("completed");
    }


    previousSquare = square;
    setTimeout(update_money, 2000) //Delay here immitates the time that animation would be taking
    setTimeout(function () {if (declareAction != "") {update_declare(false);}}, 2000)
 }

 /*---------------*/
 //Updates values in cash and bank boxes
 function update_money()
 {
     if (cashTotal != recordedCash) {if (cashBox.innerHTML == "") {cashBox.innerHTML = cashTotal} else {cashBox.innerHTML = cashBox.innerHTML + `, ${cashTotal}`}} //Adds commas only if box is not empty
     if (bankTotal != recordedBank) {if (bankBox.innerHTML == "") {bankBox.innerHTML = bankTotal} else {bankBox.innerHTML = bankBox.innerHTML + `, ${bankTotal}`}}
     recordedBank = bankTotal
     recordedCash = cashTotal
 }

 /*---------------*/
 //Updates the game log panel
 function log_update(text)
 {
     text = text.replace(MY_NICKNAME,"YOU") //Replaces your name with 'YOU'
     logBox.innerHTML += text + "<br>"; //Appends entry to LOG
 }

 /*---------------*/
 //Update declaration button
 function update_declare(state)
 {
     declareButton.disabled = state; //Disables button
     //Add / Remove CSS class
     if (state) {declareButton.classList.add("disabled")}
     else {declareButton.classList.remove("disabled")}
 }

 /*---------------*/
 //Sends a declaration to server that an event has been declared (called when declare button pressed)
 function declare_action()
 {
     socket.emit('action_declare', {target : "", action : declareAction}); //Declares that an action has been called but doesn't have a target
     targetSelector = true; //Target selector variable prevents other waiting pop-up from showing
     target_picker(declareAction); //Shows target picker popup
 }

 /*---------------*/
 //Sends target information to server (Called when Choose button on popup is clicked)
 function declare_target()
 {
     var target = document.getElementById("sel_target").value; //Get the value from the target picker
     socket.emit('action_declare', {target : target, action : declareAction}); //Send over another declaration event but including target
     targetPickerPopup.style.display="none"; //Hide target picker popup again
     targetSelector = false; //Disable other popup inhibiting
     update_declare(true) //Update the declare button back to disabled state
     declare_action = "";

 }

 //=========================================================//
 //^ Defines popups ^//
 //The popup showing the current happening of other users
 function action_popup(data)
 {
     if (targetSelector == false) //Do not show popup who currently is picking the target
     {
         var target = data["target"];
         var perpetrator = data["perpetrator"];
         var action = data["action"];

         //Get HTML elements from page
         var actionText = document.getElementById("h3_action_emphasis_text");
         var perpetratorText = document.getElementById("h3_perpetrator_text");
         waitingForActionPopup.style.display = "block";

        //Update the perpatrator text
         perpetratorText.innerHTML = perpetrator

         //Set the action that is shown
         if (action == "itmKill") {actionText.innerHTML = "⚔ KILL ⚔"}
         if (action == "itmSteal") {actionText.innerHTML = "💰 STEAL FROM 💰"}
         if (action == "itmSwap") {actionText.innerHTML = "🤝 SWAP WITH 🤝"}
         if (action == "itmGift") {actionText.innerHTML = "🎁 GIFT 🎁"}

         //Loading dots or target shown
         var loadingDots = document.getElementById("div_loadingdots");
         var targetText = document.getElementById("h3_target_text");
         if (target != "") //If target has been decided
         {
             if (target.toLowerCase() == MY_NICKNAME.toLowerCase()){
                 targetText.innerHTML = "YOU"
                 socket.emit("retaliation_declare", {type: "none"})
             }else {targetText.innerHTML = target;} //Show who the target is
             
             loadingDots.style.display = "none"; //Hide loading dots
             setTimeout(function () {update_money();},100); //Update all user's cash box in case they are the target
             setTimeout(function () {waitingForActionPopup.style.display="none"}, 3000) //Close the popup after 3s
         } else //Show loading circles
         {
            targetText.innerHTML = ""
            loadingDots.style.display = "block";
         }

         
     }
 }

 /*---------------*/
 //The popup for the perpetrator to select a target
 function target_picker(action)
 {
     var actionText = document.getElementById("h3_targetPickerAction")
     if (action == "itmKill") {actionText.innerHTML = "⚔ KILL ⚔"}
     if (action == "itmSteal") {actionText.innerHTML = "💰 STEAL FROM 💰"}
     if (action == "itmSwap") {actionText.innerHTML = "🤝 SWAP WITH 🤝"}
     if (action == "itmGift") {actionText.innerHTML = "🎁 GIFT 🎁"}

     targetPickerPopup.style.display="block" //Show the popup
 }

 //=========================================================//
 //^ Defines what happens for different actions when you are the perpetrator ^//
 //Determines what happens on kill
 function item_available(data)
 {

     declareAction = data["type"];
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