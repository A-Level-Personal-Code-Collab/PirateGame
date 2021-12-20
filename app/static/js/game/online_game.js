/**
 * File: /home/will/GitHub Repos/PirateGame/static/js/game/online_game.js
 * Project: /home/will/GitHub Repos/PirateGame/static/javascript
 * Created Date: Saturday, August 28th 2021, 3:12:37 pm
 * Author: Will Hall
 * -----
 * Last Modified: Mon Dec 20 2021
 * Modified By: Will Hall
 * -----
 * Copyright (c) 2021 Lime Parallelogram
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 * 2021-12-20	WH	New items update the help message popup when they come in
 * 2021-11-15	WH	Fixed retaliation not removing bug
 * 2021-11-09	WH	Handle money values no longer being cumulative
 * 2021-11-09	WH	Increase available retaliation time
 * 2021-11-09	WH	Added handling for display delay on things after the spinner. e.g. Money items (Issue #151)
 * 2021-10-30	WH	Fixed  incorrect retaliation removal
 * 2021-10-29	WH	Added function to restrict height of log box to the height of the grid
 * 2021-10-01	WH	Added client side builder for target picker dropdown
 * 2021-10-01	WH	Switched to handle SIDs sent by client as oppose to RAW usernames and replace these client side
 * 2021-09-29	WH	Handle retaliation display event to show the animation on retaliations
 * 2021-09-27	WH	Added leave page confirmation
 * 2021-09-26	WH	Uses dynamic socketio address now
 * 2021-09-26	WH	Added handling for game finished event to forward users to results page (Issue#104)
 * 2021-09-26	WH	Fixed retaliation removal problem (Issue#)
 * 2021-09-26	WH	Implemented square picker animation
 * 2021-09-25	WH	Option to retaliate now disables unavailable retaliation
 * 2021-09-25	WH	Future tense message for popup now defined server side
 * 2021-09-25	WH	Bank update behaves like cash and doesn't show unless there is any need
 * 2021-09-25	WH	All animation delay now happens server side
 * 2021-09-19	WH	Added tracking for available retaliations
 * 2021-09-19	WH	Added system to display available retaliation options
 * 2021-09-17	WH	item_available event replaces perpetrate_kill and perpetrate_steel etc. events
 * 2021-09-17	WH	Changed item names to match the python naming and their names in the database (E.g) kill is now itmKill
 * 2021-09-02	WH	Added handling for log updates
 * 2021-09-02	WH	Added target picker popup
 * 2021-09-02	WH	Added handling for waiting for decision popups
 * 2021-09-02	WH	Added handling for special item updates
 * 2021-08-28	WH	Added handling for cash and bank updates
 * 2021-08-28	WH	Added handling for new_square event
 */
 //=========================================================//
 //^ Gets elements from page ^//
 const SOCKETIO_ADDRESS = "http://localhost:8001"
 const cashBox = document.getElementById("div_cashText")
 const bankBox = document.getElementById("div_bankText")
 const logBox = document.getElementById("p_logText")
 const declareButton = document.getElementById("ipt_declare")
 const chooseButton = document.getElementById("ipt_chooseTarget")
 const waitingForActionPopup =  document.getElementById("div_waitingPopup")
 const targetPickerPopup = document.getElementById("div_targetPickerPopup")
 const retaliationsStorage = document.getElementById("retaliation_box")
 const animationPopup = document.getElementById("retal-animation");

 //=========================================================//
 //^ Variables ^//
 var socket = io.connect(SOCKETIO_ADDRESS, {transports: ["websocket"]});
 var previousSquare = null;
 var recordedCash = 0;
 var recordedBank = 0;
 var declareAction = ""; //The name of the action that is going to be declared
 var targetSelector = false; //Tracks if the user is currently selecting a target
 var retaliations = [] //A list of available retaliations
 var retaliated = false //Has the user already retaliated to the incoming action
 var intentionalForward = false; //Sets whether the forwarding is intended
 var usersDictionary = {}

 //=========================================================//
 //^ OnLoad Function ^//
 function on_load()
 {
    //Adds leave page confirmation
    window.addEventListener("beforeunload", function(event) {if (!intentionalForward) {event.returnValue = "Do you really wish to leave this site?"; return "Do you really wish to leave this site?";}});
    
    /*---------------*/
    //Parse dictionary from python and sort the top 3 in array form
    var gameID = getUrlVar("gid")
    var userSID = getCookie("SID")

    /*---------------*/
    //Adds event listeners for socket events
    socket.on('connect', () => {
        socket.emit("join",{userSID: userSID, gameID: gameID}) //Sends join event to server which causes the user to get added to a room
    })

    socket.on("ERR", (msg) => {alert("Server Error: " + msg)}); //Displays server error messages

    socket.on('new_square', select_square)
    socket.on('cash_update', update_cash)
    socket.on('bank_update', update_bank)
    socket.on('log_update', log_update)

    socket.on('itm_available', item_available);
    socket.on('retal_available', update_retaliations) //Add new retaliation to retaliations array

    socket.on('action_declare', action_popup);
    socket.on('retaliation_declare', handle_retaliation_declare)

    socket.on('game_complete', function () {intentionalForward = true; window.location.href = `/playing_online/results?gid=${gameID}`}) //Starts game if game event is received

    socket.on('users_update', function(newDict) {usersDictionary = newDict;})
    /*---------------*/
    //Adds event listeners for page events
    declareButton.addEventListener("click", declare_action);
    chooseButton.addEventListener("click", declare_target);

    /*---------------*/
    //Restrict height of the game information boxes to the height of the grid
    document.getElementById("div_gameDataGroup").style.maxHeight = document.getElementById("tbl_playGrid").offsetHeight.toString()+"px"

 }

 //=========================================================//
 //^ Slave Subs ^//
 /*---------------*/
 //Lights up a selected square and greys-out the old one
 function select_square(serialSquareNum)
 {
     const RUN_TIMES = 30;
     const INTERVAL = 100;

    var intervalFunc = setInterval(() => {
        if (previousSquare) {previousSquare.classList.remove("selected"); previousSquare.classList.add("completed");}
        var randomTag = pickRandomSquare();
        randomTag.classList.add("selected");

        setTimeout(() => {
            randomTag.classList.remove("selected");
        }, INTERVAL);
    }, INTERVAL);

    //Ends interval loop after set time then adds the final square
    setTimeout(() => {
        clearInterval(intervalFunc)

        setTimeout(() =>{
            var square = document.getElementById(`square${serialSquareNum}`);
            square.classList.add("selected"); //Lights up winning square

            previousSquare = square;
        }, INTERVAL)
    },RUN_TIMES*INTERVAL)    

    
 }
 /*---------------*/
 //Choses a random square for the animation
 function pickRandomSquare() {
    var allRemainingSquares = document.querySelectorAll(".gridSquare:not(.completed):not(#None)")
    return allRemainingSquares[Math.floor(Math.random()*allRemainingSquares.length)]
 }

 /*---------------*/
 //Updates values in cash box
 function update_cash(data)
 {
     const cashTotal = data["value"]
     const timeout = data["delay"]
     setTimeout(() => {if (cashTotal != recordedCash) {cashBox.innerHTML = cashTotal};
     recordedCash = cashTotal}, timeout);
 }

 /*---------------*/
 //Updates values in bank
 function update_bank(data)
 {
    const bankTotal = data["value"]
    const timeout = data["delay"]
    setTimeout(() => {
    if (bankTotal != recordedBank) {bankBox.innerHTML = bankTotal};
     recordedBank = bankTotal},timeout);
 }

 /*---------------*/
 //Updates the game log panel
 function log_update(data)
 {
     console.log(data);
     var text = data["entry"]
     var delay = data["delay"]
     console.log(text)
     text = text.replace(`!<${MY_SID}>`,"YOU") //Replaces your name with 'YOU'

     //Handles replacement of SID's with nicknames
     for (const [sid, nick] of Object.entries(usersDictionary))
     {
        text = text.replace(`!<${sid}>`,nick)
     }

     setTimeout(() => {logBox.innerHTML += text + "<br>";},delay); //Appends entry to LOG
 }

 /*---------------*/
 //Update the box that displays available reactions
 function update_retaliations(retal_new)
 {
     if (retal_new != null) {var delay = retal_new["delay"]; retaliations.push(retal_new);}
     else {var delay = 0;}
     //Creates html images on page to show what actions the user has available
     var imageList = ""
     retaliations.forEach((a) => {
         imageList = imageList + `<img src="${a['image']}" class="retaliationItems" alt="${a["type"]}" id="${a["type"]}">`
     })

     setTimeout(() => {retaliationsStorage.innerHTML = imageList;}, delay); //Display images on page
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
     declareButton.disabled = true; //Update the declare button back to disabled state
     declareAction = "";

 }

 /*---------------*/
 //Declare the user's choice of retaliation to the server
 function retaliation_declare(type)
 {
     if (!retaliated) { //Check a retaliation hasn't already been sent
        socket.emit("retaliation_declare", {type: type}); //Send back to server
        if (type != "none") {
            var index = retaliations.map(function(d) { return d['type']; }).indexOf(type)
            retaliations.splice(index,1); //Remove retaliation from available retaliations events
            update_retaliations(); //Update the retaliations box on the page
        }
        retaliated = true;
     }
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
         var ftVerbMessage = data["ftVerb"]
         var explanation = data["explanation"]
         updateHelp(explanation)
         var invalidRetals = data["invalidRetals"].split(",")
         console.log(invalidRetals)

         //Get HTML elements from page
         var actionText = document.getElementById("h3_action_emphasis_text");
         var perpetratorText = document.getElementById("h3_perpetrator_text");
         waitingForActionPopup.style.display = "block";

        //Update the perpetrator text
         perpetratorText.innerHTML = usersDictionary[perpetrator];

         //Set the action text message that is shown e.g. Will Kill ...
         actionText.innerHTML = ftVerbMessage

         //Loading dots or target shown
         var loadingDots = document.getElementById("div_loadingdots");
         var targetText = document.getElementById("h3_target_text");
         var retaliations_area = document.getElementById("div_retaliation_controls");
         retaliations_area.innerHTML = "";
         if (target != "") //If target has been decided
         {
             if (target == MY_SID){
                 targetText.innerHTML = "YOU";

                 retaliated = false;
                 retaliations.forEach((a) => {
                    if (invalidRetals.includes(a["type"])) //Checks if a given retaliation is disallowed by the event in question
                    {
                        retaliations_area.innerHTML += `<img src="${a["image"]}" onClick="retaliation_declare('${a["type"]}')" class="retaliationOption disabled" alt="${a["type"]}">`
                    } else
                    {
                        retaliations_area.innerHTML += `<img src="${a["image"]}" onClick="retaliation_declare('${a["type"]}')" class="retaliationOption" alt="${a["type"]}">`
                    }
                 })

                 setTimeout(() => {retaliation_declare("none")}, 3000);
                 
             }else {targetText.innerHTML = usersDictionary[target];} //Show who the target is
             
             loadingDots.style.display = "none"; //Hide loading dots
             setTimeout(function () {waitingForActionPopup.style.display="none"; animationPopup.style.display = "none";}, 5000) //Close the popup after 3s

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
     //Generates target picker dropdown from local user list
     const targetPickerDropdown = document.getElementById("sel_target");
     targetPickerDropdown.innerHTML = "";

     //Loops through dictionary and sets front text as nickname and value as 
     for (const [sid, nick] of Object.entries(usersDictionary))
     {
        if (MY_SID != sid)
        {
            var opt = document.createElement("option");
            opt.setAttribute('value',`${sid}`);
            opt.innerHTML=nick;
            targetPickerDropdown.appendChild(opt);
        }
     }

     /*---------------*/
     targetPickerPopup.style.display="block" //Show the popup
 }

 //=========================================================//
 //^ Animations of retaliations ^//
 function handle_retaliation_declare(data)
 {
     var image = data["animation-image"]
     var aniClass = data["animation-class"]

     animationPopup.src = image;
     animationPopup.classList = aniClass;
     animationPopup.style.display = "block";
 }

 //=========================================================//
 //^ Defines what happens when events come in from the socket^//
 //Determines what happens when a new item is available (runs as soon as event comes in)
 function item_available(data)
 {
     declareAction = data["type"];
     var delay = data["delay"]
     var popupMessage = data["ftVerb"]
     var itemExplanation = data["explanation"]
     updateHelp(itemExplanation)
     document.getElementById("h3_targetPickerAction").innerHTML = popupMessage
     setTimeout(() => {declareButton.disabled = false;}, delay);
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