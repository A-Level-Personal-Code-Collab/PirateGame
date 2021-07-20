/**
 * File: /home/will/GitHub Repos/PirateGame/static/javascript/game_sheet.js
 * Project: /home/will/GitHub Repos/PirateGame/static/javascript
 * Created Date: Friday, July 9th 2021, 9:29:43 pm
 * Author: Will Hall
 * -----
 * Last Modified: Tue Jul 20 2021
 * Modified By: Will Hall
 * -----
 * Copyright (c) 2021 Lime Parallelogram
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 * 2021-07-20	WH	Dropping may now occur in the bank section and items will return to the correct collum based on whether they are money or other items
 * 2021-07-20	WH	Modified drop script so items can oly be dropped in empty cells.
 * 2021-07-11	WH	Created required javascript to allow for draggable grid elements
 */

/*Get elements from the page*/
 const draggables = document.querySelectorAll('.gridItems')
 const containers = document.querySelectorAll('.dragReceptical')
 
 /*Contant parameters*/
const maxMoneys = 
{
  M5000 : 1,
  M1000 : 3,
  M500 : 5,
  M200 : 18
}

 var numMoneys = 
 {
   M5000 : 0,
   M1000 : 0,
   M500 : 0,
   M200 : 0
 }

 /*Add event listeners*/
 draggables.forEach(draggable => {
   draggable.addEventListener('dragstart', (event) => {
     event.dataTransfer.setDragImage(draggable, -99999, -99999); /*Move ghost images away to very far away from screen so you can't see them*/
     /*UNFINNISHED - Attemps to create new money item if more are available*/
     if(draggable.classList.contains("itmMoney")) {
       const moneyItemBank = document.getElementById("div_moneyItems")
     }
     
     draggable.classList.add('dragging') /*Add css class that styles the dragging item*/
   })
 
   draggable.addEventListener('dragend', () => {
     draggable.classList.remove('dragging') /*Remove dragging css class*/
   })
 })
 
 /*Add drag over event listeners*/
 containers.forEach(container => {
   container.addEventListener('dragover', () => {
     if(container.innerHTML=="") { /*Prevents dragging into occupied squares*/
      /*Add the itemem with the .dragging class if it is being dragged over a square*/
      const draggable = document.querySelector('.dragging')
      container.appendChild(draggable)
     }
     /*Allow draggable item to be placed back into the item bank*/
     if (container.id == "div_itemBank") {
       const draggable = document.querySelector(".dragging")
       /*If item is money, handle it differently*/
       if (draggable.classList.contains("itmMoney"))
       {
         document.getElementById("div_moneyItems").appendChild(draggable)
       } else{
         document.getElementById("div_specialItems").appendChild(draggable)
       }
     }
   })
 })