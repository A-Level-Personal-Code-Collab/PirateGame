/**
 * File: c:\Adam\coding\1. VC Coding projects\PirateGame\static\javascript\new_game.js
 * Project: c:\Adam\coding\1. VC Coding projects\PirateGame\static\javascript
 * Created Date: Monday, August 2nd 2021, 1:24:07 pm
 * Author: Adam O'Neill
 * -----
 * Last Modified: Wed Sep 29 2021
 * Modified By: Adam O'Neill
 * -----
 * Copyright (c) 2021 Adam O'Neill
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 * 2021-09-27	WH	Added code to alert users if their nickname is rejected
 * 2021-08-09	WH	Fixed problem where output boxes failed to update on custom-mode-disable (issue#33)
 * 2021-08-02	WH	Fixed disable item code and tidied File
 * 2021-08-02	AO	Added basic code aiming to disabale game customisation if master slider off
 */

const disablables = document.querySelectorAll(".disablable")
const custom_game_mode_button = document.getElementById("custom_game_mode_button")
const secretmode_tick = document.getElementById("secretMode_tick")
const grid_slider = document.getElementById("grid_slider")
const steal_slider = document.getElementById("steal_slider")
const kill_slider = document.getElementById("kill_slider")
const gift_slider = document.getElementById("gift_slider")
const swap_slider = document.getElementById("swap_slider")
const shield_slider = document.getElementById("shield_slider")
const mirror_slider = document.getElementById("mirror_slider")
const bomb_slider = document.getElementById("bomb_slider")
const bank_slider = document.getElementById("bank_slider")
const M5000_slider = document.getElementById("5000_slider")
const M1000_slider = document.getElementById("1000_slider")
const M500_slider = document.getElementById("500_slider")
const M200_slider = document.getElementById("200_slider")
const start_game_button = document.getElementById("start_game_button")
const nicknameinput = document.getElementById("ipt_nickname")

/*=========================================================*/
function onload() {
    //Adds OnClick Listener
    custom_game_mode_button.addEventListener("change",disable)
    start_game_button.addEventListener("click",return_settings)
    nicknameinput.addEventListener('input', () => {check_data(); nicknameinput.classList.remove("inputError")});

    /*=========================================================*/
    // Fitty for this page

}

/*=========================================================*/
// Checks data in the nickname box
function check_data()
{
    /*---------------*/
    //Get data from forms
    var nicknameText = nicknameinput.value;

    /*---------------*/
    //Unlock button if data is accepted
    if (check_nickname(nicknameText))
    {
        start_game_button.classList.remove("disallowed")
        start_game_button.disabled = false;
    }
    else
    {
        start_game_button.classList.add("disallowed")
        start_game_button.disabled = true;
    }
}
/*=========================================================*/
//Disables all sliders and switches if custom gamemode switch is toggled off
function disable() {
    var button_status = custom_game_mode_button.checked /* boolean variable */ 
    if (button_status == true) {
        disablables.forEach(i => {i.classList.remove("disablable"); i.disabled = false})
    }
    else     {
        disablables.forEach(i => {i.classList.add("disablable"); i.disabled = true;})
        // Resets the switches to their defult positions
        grid_slider.value = 6
        steal_slider.value = 1
        kill_slider.value = 1
        gift_slider.value = 1
        swap_slider.value = 1
        shield_slider.value = 1
        mirror_slider.value = 1
        bomb_slider.value = 1
        bank_slider.value = 2
        M5000_slider.value = 1
        M1000_slider.value = 3
        M500_slider.value = 5
        M200_slider.value = 18

        // Need to change output boxes to corresponding number
        disablables.forEach(i => {output_update(i)})

    }
}

/*=========================================================*/
// Collect data from page

function return_settings() {
    var grid_sliders = {GRID_X:Number(grid_slider.value), GRID_Y:Number(grid_slider.value)}
    var item_settings = {M5000:Number(M5000_slider.value), M1000:Number(M1000_slider.value), M500:Number(M500_slider.value), M200:Number(M200_slider.value), itmShield:Number(shield_slider.value), itmKill:Number(kill_slider.value), itmSteal:Number(steal_slider.value), itmMirror:Number(mirror_slider.value), itmBomb:Number(bomb_slider.value), itmBank:Number(bank_slider.value), itmSwap:Number(swap_slider.value), itmGift:Number(gift_slider.value)}
    var nickname = nicknameinput.value
    var grid_sliders_string = JSON.stringify(grid_sliders)
    var item_settings_string = JSON.stringify(item_settings)
    var game_data = (grid_sliders_string + "|" + item_settings_string)
    console.log(game_data)
    postdata(game_data,nickname)
}

/*=========================================================*/
//Posting data to server

function postdata(game_data,nickname){
    var xhr = new XMLHttpRequest()
    var thisURL = window.location.href
    xhr.open("POST",thisURL,true)
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            if (xhr.responseURL == window.location.href) {nicknameinput.classList.add("inputError")} //If the same page gets served again the assume problem with nickname
            else {window.location.href = xhr.responseURL}
        }
    }
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhr.send(`game_data=${game_data}&nickname=${nickname}`)

}

//=========================================================//
//^ Updates the output numbers ^//
function output_update(element) {
    element.nextElementSibling.value = element.value
}

/*=========================================================*/
//Executes onload
onload()