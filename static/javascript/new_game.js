/**
 * File: c:\Adam\coding\1. VC Coding projects\PirateGame\static\javascript\new_game.js
 * Project: c:\Adam\coding\1. VC Coding projects\PirateGame\static\javascript
 * Created Date: Monday, August 2nd 2021, 1:24:07 pm
 * Author: Adam O'Neill
 * -----
 * Last Modified: Mon Aug 02 2021
 * Modified By: Will Hall
 * -----
 * Copyright (c) 2021 Adam O'Neill
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 * 2021-08-02	WH	Fixed disable item code and tidied File
 * 2021-08-02	AO	Added basic code aiming to disabale game customisation if master slider off
 */

const disablables = document.querySelectorAll(".disablable")
const custom_game_mode_button = document.getElementById("custom_game_mode_button")

/*=========================================================*/
function onload() {
    //Adds OnClick Listener
    custom_game_mode_button.addEventListener("change",disable)
}

/*=========================================================*/
//Disables all sliders and switches if custom gamemode switch is toggled off
function disable() {
    var button_status = custom_game_mode_button.checked /* boolean variable */ 
    if (button_status == true) {
        disablables.forEach(i => {i.classList.remove("disablable"); i.disabled = false})
    }
    else     {
        disablables.forEach(i => {i.classList.add("disablable"); i.disabled = true})
    }
}

/*=========================================================*/
//Executes onload
onload()