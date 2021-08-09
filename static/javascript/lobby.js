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
     fetch_data();
    setInterval(fetch_data, 550);
 }

 /*---------------*/
 //Fetch data about current users from server
 function fetch_data()
 {
     fetch("https://localhost:5000/playing_online/lobby/active_users?gid=00000001") //Must do this dynamically based on ID
     .then (function(response) {return response})
     .then(data => {return data.text()})
     .then(text => {listDiv.innerHTML=text;})
     .catch(function(err) {console.log(err.message)})
 }

 //=========================================================//
 //^ Runs onload functions ^//
 on_load();