/**
 * File: /home/will/GitHub Repos/PirateGame/static/javascript/verification_routines.js
 * Project: /home/will/GitHub Repos/PirateGame/static/javascript
 * Created Date: Wednesday, August 4th 2021, 10:32:28 am
 * Author: Will Hall
 * -----
 * Last Modified: Sun Oct 31 2021
 * Modified By: Will Hall
 * -----
 * Copyright (c) 2021 Lime Parallelogram
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 * 2021-08-04	WH	Moved game ID and nickname validation routines to new file
 */

 /*=========================================================*/
 //Checks an entered nickname for length and characters
 function check_nickname(text)
 {
     const VERIFICATION_STAGES = 2; //Required value of verification value to allow submission
     const NICKNAME_LEN = 15;
     const NICKNAME_MIN = 3;
 
     var verificationValue = 0; 
     if (text.length <= NICKNAME_LEN && text.length >= NICKNAME_MIN) {verificationValue ++;}
 
     //Checks that nickname contains ONLY english letters
     verificationValue ++;
     for (var l = 0; l < text.length; l++)
     {
         var charcode = text.toUpperCase().charCodeAt(l);
         if ((charcode > 90 || charcode < 65) && (charcode != 32)) {verificationValue--;} //Checks ASCII code falls into letter section
     }
 
     if (verificationValue >= VERIFICATION_STAGES) {return true} else {return false}
 }
 
 /*=========================================================*/
 //Checks an entered ID for length and number check
 function check_ID(idText)
 {
     //Values set for verification
     const GAMECODE_LEN = 8;
     const VERIFICATION_STAGES = 2; //Required value of verification value to allow submission
 
     var verificationValue = 0; 
     if (idText.length == GAMECODE_LEN) {verificationValue ++;}
     if (!isNaN(idText)) {verificationValue ++;} //Check if game ID is a valied number
 
     if (verificationValue >= VERIFICATION_STAGES) {return true} else {return false}
 }