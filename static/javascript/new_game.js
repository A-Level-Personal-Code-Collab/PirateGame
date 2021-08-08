/**
 * File: c:\Adam\coding\1. VC Coding projects\PirateGame\static\javascript\new_game.js
 * Project: c:\Adam\coding\1. VC Coding projects\PirateGame\static\javascript
 * Created Date: Monday, August 2nd 2021, 1:24:07 pm
 * Author: Adam O'Neill
 * -----
 * Last Modified: Sun Aug 08 2021
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
const secretmode_tick = document.getElementById("secretMode_tick")
const x_slider = document.getElementById("x_slider")
const y_slider = document.getElementById("y_slider")
const steal_slider = document.getElementById("steal_slider")
const kill_slider = document.getElementById("kill_slider")
const gift_slider = document.getElementById("gift_slider")
const swap_slider = document.getElementById("swap_slider")
const shield_slider = document.getElementById("shield_slider")
const mirror_slider = document.getElementById("mirror_slider")
const bomb_slider = document.getElementById("bomb_slider")
const bank_slider = document.getElementById("bank_slider")
const M5000_slider = bank_slider // Change to elemet id
const M1000_slider = bank_slider
const M500_slider = bank_slider
const M200_slider = bank_slider
const start_game_button = document.getElementById("start_game_button")

/*=========================================================*/
function onload() {
    //Adds OnClick Listener
    custom_game_mode_button.addEventListener("change",disable)
    start_game_button.addEventListener("click",return_settings)
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
        secretmode_tick.checked=false
        x_slider.value = 6
        y_slider.value = 6
        steal_slider.value = 1
        kill_slider.value = 1
        gift_slider.value = 1
        swap_slider.value = 1
        shield_slider.value = 1
        mirror_slider.value = 1
        bomb_slider.value = 1
        bank_slider.value = 1
        // Need to change output boxes to corresponding number

    }
}

/*=========================================================*/
// Collect data from page

function return_settings() {
    var grid_sliders = {GRID_X:x_slider.value, GRID_Y:y_slider.value}
    var item_settings = {M5000:M5000_slider.value, M1000:M1000_slider.value, M500:M500_slider.value, M200:M200_slider.value, itmShield:shield_slider.value, itmKill:kill_slider.value, itmSteal:steal_slider.value, itmMirror:mirror_slider.value, itmBomb:bomb_slider.value, itmBank:bank_slider.value, itmSwap:swap_slider.value, itmGift:gift_slider.value}
    var grid_sliders_string = JSON.stringify(grid_sliders)
    var item_settings_string = JSON.stringify(item_settings)
    var game_data = (grid_sliders_string + "|" + item_settings_string)
    console.log(game_data)
    postdata(game_data)
}

/*=========================================================*/
//Posting data to server

function postdata(game_data){
    var xhr = new XMLHttpRequest()
    var thisURL = window.location.href
    xhr.open("POST",thisURL,true)
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            window.location.href = xhr.responseURL
        }
    }
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhr.send(`game_data=${game_data}`)

}

/*=========================================================*/
//Executes onload
onload()