/**
 * File: c:\Users\ollie\OneDrive\Desktop\Documents\GitHub Repos\PirateGame\static\javascript\results.js
 * Project: c:\Users\ollie\OneDrive\Desktop\Documents\GitHub Repos\PirateGame\static\javascript
 * Created Date: Sunday, September 19th 2021, 8:35:59 pm
 * Author: Ollie Burroughs
 * -----
 * Last Modified: Sun Sep 26 2021
 * Modified By: Ollie Burroughs
 * -----
 * Copyright (c) 2021 SchmetCorp.
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 */
const firsttxt = document.getElementById("firsttxt")
const secondtxt = document.getElementById("secondtxt")
const thirdtxt = document.getElementById("thirdtxt")
fitty('#firsttxt')
fitty('#secondtxt')
fitty('#thirdtxt')
console.log(top3str)
var top3dict = JSON.parse(top3str)
var top3users = Object.keys(top3dict)
firsttxt.innerHTML = top3users[0]
secondtxt.innerHTML = top3users[1]
thirdtxt.innerHTML = top3users[2]