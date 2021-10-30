/**
 * File: c:\Adam\Coding\PirateGame\static\javascript\header.js
 * Project: c:\Adam\Coding\PirateGame\static\javascript
 * Created Date: Saturday, October 30th 2021, 1:58:32 pm
 * Author: Adam O'Neill
 * -----
 * Last Modified: Sat Oct 30 2021
 * Modified By: Adam O'Neill
 * -----
 * Copyright (c) 2021 Adam O'Neill
 * ------------------------------------
 * Javascript will save your soul!
 */

window.onscroll = function() {Scrolling()}


var mainHeader = document.getElementById("mainHeader");
var headerOffSet = mainHeader.offsetTop

function Scrolling() {
    if (window.pageYOffset > headerOffSet) {
        mainHeader.classList.add("sticky");
        fitty("#mainHeader")
    }
    else {
        mainHeader.classList.remove("sticky")
    }
}
