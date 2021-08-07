/**
 * File: c:\Adam\coding\1. VC Coding projects\PirateGame\static\javascript\new_game.js
 * Project: c:\Adam\coding\1. VC Coding projects\PirateGame\static\javascript
 * Created Date: Monday, August 2nd 2021, 1:24:07 pm
 * Author: Adam O'Neill
 * -----
 * Last Modified: Sat Aug 07 2021
 * Modified By: Adam O'Neill
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
        // Resets the switches to their defult positions
        document.getElementById("secretMode_tick").checked=false
        document.getElementById("x_slider").value = 6
        document.getElementById("y_slider").value = 6
        document.getElementById("steal_slider").value = 1
        document.getElementById("kill_slider").value = 1
        document.getElementById("gift_slider").value = 1
        document.getElementById("swap_slider").value = 1
        document.getElementById("shield_slider").value = 1
        document.getElementById("mirror_slider").value = 1
        document.getElementById("bomb_slider").value = 1
        document.getElementById("bank_slider").value = 1
        // Need to change output boxes to corresponding number

    }
}

/*=========================================================*/
// Resets the switches to their defult positions
/*=========================================================*/
//Executes onload
onload()