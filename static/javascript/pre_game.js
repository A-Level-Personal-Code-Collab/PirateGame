/**
 * File: https://github.com/Lime-Parallelogram/PirateGame/static/javascript/pre_game.js
 * Project: https://github.com/Lime-Parallelogram/PirateGame
 * Created Date: Sunday, August 1st 2021, 3:48:42 pm
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
 * 2021-08-02	WH	Added basic varification of join game inputs before submitting information to server
 */

const submitButton = document.getElementById("btn_submit_button");
const nicknameInput = document.getElementById("ipt_nickname");
const gameIDInput = document.getElementById("ipt_game_ID");

/*=========================================================*/
//Runs function on page load
function on_load()
{
    //Adds event listeners to various objects
    nicknameInput.addEventListener('input', check_data);
    gameIDInput.addEventListener('input', check_data);

    //Checks data on load in case backspace has been pressed and data is already present
    check_data();
}

/*=========================================================*/
//Checks data in input boxes and 
function check_data()
{
    //Values set for varification
    const GAMECODE_LEN = 8;
    const VARIFICATION_STAGES = 4; //Required value of varification value to allow submission
    const NICKNAME_LEN = 15;
    const NICKNAME_MIN = 3;

    /*---------------*/
    //Perform varifications
    var nicknameText = nicknameInput.value;
    var gameIDText = gameIDInput.value;
    var verificationValue = 0; 
    if (gameIDText.length == GAMECODE_LEN) {verificationValue ++;}
    if (nicknameText.length <= NICKNAME_LEN && nicknameText.length >= NICKNAME_MIN) {verificationValue ++;}
    if (!isNaN(gameIDText)) {verificationValue ++;} //Check if game ID is a valied number

    verificationValue ++;
    for (var l = 0; l < nicknameText.length; l++)
    {
        var charcode = nicknameText.toUpperCase().charCodeAt(l);
        if (charcode > 90 || charcode < 65) {verificationValue--;}
    }


    /*---------------*/
    //Unlock button if data is accepted
    if (verificationValue >= VARIFICATION_STAGES)
    {
        submitButton.classList.remove("disallowed")
        submitButton.disabled = false;
    }
    else
    {
        submitButton.classList.add("disallowed")
        submitButton.disabled = true;
    }
    
    /*---------------*/
    //Remove python error classes on type
    nicknameInput.classList.remove("inputError")
    gameIDInput.classList.remove("inputError")
}

/*=========================================================*/
//Executes onload function
on_load()