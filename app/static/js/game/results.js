/**
 * File: https://github.com/A-Level-Personal-Code-Collab/PirateGame/static/js/game/results.js
 * Project: https://github.com/A-Level-Personal-Code-Collab/PirateGame
 * Created Date: Sunday, September 19th 2021, 8:35:59 pm
 * Author: Ollie Burroughs
 * -----
 * Last Modified: Mon Dec 27 2021
 * Modified By: Will Hall
 * -----
 * Copyright (c) 2021 SchmetCorp.
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 * 2021-12-27	WH	Added resize function including compensation for page warning
 * 2021-12-27	WH	Moved to use class selectors for fitty
 * 2021-10-30	WH	Commented out cash info to make fitty work
 * 2021-09-27	WH	Sorts top 3 user properly
 * 2021-09-26	OB	Updates podium positions with player's name
 * 2021-09-26	OB	Added fitty reference to resize existing text
 */
const firsttxt = document.getElementById("firsttxt")
const secondtxt = document.getElementById("secondtxt")
const thirdtxt = document.getElementById("thirdtxt")
const firstcash = document.getElementById("firstcash")
const secondcash = document.getElementById("secondcash")
const thirdcash = document.getElementById("thirdcash")

function on_load()
{
    //Parse dictionary from python and sort the top 3 in array form
    var top3dict = JSON.parse(top3str)
    var sortedArray = Object.keys(top3dict).map(function(key) { return [key, top3dict[key]]});
    sortedArray.sort(function(first,second) {return second[1] - first[1]})

    //#//
    //Update podium positions
    firsttxt.innerHTML = sortedArray[0][0]
    secondtxt.innerHTML = sortedArray[1][0]
    thirdtxt.innerHTML = sortedArray[2][0]
    firstcash.innerHTML = sortedArray[0][1]
    secondcash.innerHTML = sortedArray[1][1]
    thirdcash.innerHTML = sortedArray[2][1]


    /*---------------*/
    //Run resize function to fit winner's names on podium
    function resizes() {
        fitty('.podtext', {minSize: 0})
        fitty('.podcash')

        //Compensate for warning message at top of screen
        const WARNING_HEIGHT =  document.querySelector(".Warning").clientHeight;
        const resultsOuter = document.getElementById("div_resultsData");
        resultsOuter.style.height = "calc(100vh - 77px - "+WARNING_HEIGHT+"px)";
    }

    resizes();
    window.addEventListener("resize",resizes);

}

//=========================================================//
//^ Execute OnLoad function ^//
on_load();