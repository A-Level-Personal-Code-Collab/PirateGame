/**
 * File: c:\Adam\coding\1. VC Coding projects\PirateGame\static\javascript\new_game.js
 * Project: c:\Adam\coding\1. VC Coding projects\PirateGame\static\javascript
 * Created Date: Monday, August 2nd 2021, 1:24:07 pm
 * Author: Adam O'Neill
 * -----
 * Last Modified: Mon Aug 02 2021
 * Modified By: Adam O'Neill
 * -----
 * Copyright (c) 2021 Adam O'Neill
 * ------------------------------------
 * Javascript will save your soul!
 */

const disablable = document.querySelectorAll(".disablable")
const custom_game_mode_button = document.getElementById("custom_game_mode_button")

function onload() {
    custom_game_mode_button.addEventListener("change",disable)
}

function disable() {
    var button_status = custom_game_mode_button.checked /* boolean variable */ 
    console.log(button_status)
    if (button_status == true) {
        disablable.forEach(i => {i.classList.remove("disablable"); i.disabled = false; console.log(i)})
    }
    else     {
        disablable.forEach(i => {i.classList.add("disablable"); i.disable = true; console.log(i)})
    }
}

onload()