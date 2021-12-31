/**
 * File: https://github.com/A-Level-Personal-Code-Collab/PirateGame/app/static/js/libraries/help_popup.js
 * Project: https://github.com/A-Level-Personal-Code-Collab/PirateGame
 * Created Date: Monday, December 20th 2021, 8:03:31 pm
 * Description: Javascript to close the html help popup
 * Author: Will Hall
 * -----
 * Last Modified: Mon Dec 20 2021
 * Modified By: Will Hall
 * -----
 * Copyright (c) 2021 Lime Parallelogram
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 * 2021-12-20	WH	Functions to show hide and update the on screen help box
 */
 const popup = document.querySelector("#help_box")
 const popupText = document.getElementById("helpText")

 function closeHelp() {
     popup.style.display = "none";
 }

 function showHelp() {
     popup.style.display="block";
 }

 function updateHelp(text) {
     popupText.innerHTML = text;
 }