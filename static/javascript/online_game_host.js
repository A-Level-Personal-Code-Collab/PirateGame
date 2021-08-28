/**
 * File: /home/will/GitHub Repos/PirateGame/static/javascript/online_game_host.js
 * Project: /home/will/GitHub Repos/PirateGame/static/javascript
 * Created Date: Saturday, August 28th 2021, 1:29:43 pm
 * Decription: Gameplay CSS for the host's controls
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

 }

 //=========================================================//
 //^ Slave subs ^//
 function next_round()
 {
    socket.emit("next_round");
 }

 //=========================================================//
 //^ Runs onload functions ^//
 on_load();