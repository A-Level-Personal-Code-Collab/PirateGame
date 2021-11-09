/**
 * File: /home/will/GitHub Repos/PirateGame/static/js/game/host_only/online_game_host.js
 * Project: /home/will/GitHub Repos/PirateGame/static/javascript
 * Created Date: Saturday, August 28th 2021, 1:29:43 pm
 * Description: Game-play CSS for the host's controls
 * Author: Will Hall
 * -----
 * Last Modified: Tue Nov 09 2021
 * Modified By: Will Hall
 * -----
 * Copyright (c) 2021 Lime Parallelogram
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 * 2021-11-09	WH	Added handling for next round button show delay (Issue #151)
 * 2021-09-26	WH	Changes next round button text on final round
 * 2021-09-25	WH	Added next round disabling system
 * 2021-08-28	WH	Added event listener to Next-Round button in order to move to next round
 */
 //=========================================================//
 //^ Get objects from HTML page ^//
 const nextRound_btn = document.getElementById("ipt_NextRoundButton");


 //=========================================================//
 //^ OnLoad Subroutine ^//
 function on_load()
 {
     //Add event listeners
     nextRound_btn.addEventListener("click", next_round);

     /*---------------*/
     // SocketIO Listeners
     socket.on("round_complete", round_complete)

 }

 //=========================================================//
 //^ Slave subs ^//
 function next_round()
 {
    socket.emit("next_round");
    nextRound_btn.disabled = true;
    var remainingSquares = document.querySelectorAll(".gridSquare:not(.completed):not(#None)").length
    if (remainingSquares == 2) {nextRound_btn.value = "Get Results ➪"}
 }

 function round_complete(data)
 {

     setTimeout(() => {nextRound_btn.disabled = false;}, data["delay"]);
 }

 //=========================================================//
 //^ Runs onload functions ^//
 on_load();