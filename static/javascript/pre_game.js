/**
 * File: https://github.com/Lime-Parallelogram/PirateGame/static/javascript/pre_game.js
 * Project: https://github.com/Lime-Parallelogram/PirateGame
 * Created Date: Sunday, August 1st 2021, 3:48:42 pm
 * Author: Adam O'Neill
 * -----
 * Last Modified: Sun Oct 31 2021
 * Modified By: Will Hall
 * -----
 * Copyright (c) 2021 Adam O'Neill
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 * 2021-08-19	WH	Added listeners for existing SID cookie popup
 * 2021-08-04	WH	Moved actual verification routines to other js file (ensure this is loaded)
 * 2021-08-02	WH	Added basic verification of join game inputs before submitting information to server
 */

const submitButton = document.getElementById("btn_submit_button");
const nicknameInput = document.getElementById("ipt_nickname");
const gameIDInput = document.getElementById("ipt_game_ID");
const returnActive = document.getElementById("btn_goto_active")
const playHere = document.getElementById("btn_join_here")

/*=========================================================*/
//Runs function on page load
function on_load()
{
    //Adds event listeners to various objects
    nicknameInput.addEventListener('input', () => {check_data(); nicknameInput.classList.remove("inputError")});
    gameIDInput.addEventListener('input', () => {check_data(); gameIDInput.classList.remove("inputError")});
    returnActive.addEventListener('click', () => {window.location.href = "/sheet_builder?gid="+gameIDInput.value})
    playHere.addEventListener('click', () => {submitButton.value="Playing here instead"; submitButton.click()}) //We use the button's value to signal we wish to accept the new SID and discard the old one

    //Checks data on load in case backspace has been pressed and data is already present
    check_data();
}

/*=========================================================*/
//Checks data in input boxes and 
function check_data()
{
    /*---------------*/
    //Get data from forms
    var nicknameText = nicknameInput.value;
    var gameIDText = gameIDInput.value;

    /*---------------*/
    //Unlock button if data is accepted
    if (check_nickname(nicknameText) && check_ID(gameIDText))
    {
        submitButton.classList.remove("disallowed")
        submitButton.disabled = false;
    }
    else
    {
        submitButton.classList.add("disallowed")
        submitButton.disabled = true;
    }
}

/*=========================================================*/
//Executes onload function
on_load()