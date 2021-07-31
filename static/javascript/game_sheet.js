/**
 * File: /home/will/GitHub Repos/PirateGame/static/javascript/game_sheet.js
 * Project: /home/will/GitHub Repos/PirateGame/static/javascript
 * Created Date: Friday, July 9th 2021, 9:29:43 pm
 * Author: Will Hall
 * -----
 * Last Modified: Sat Jul 31 2021
 * Modified By: Will Hall
 * -----
 * Copyright (c) 2021 Lime Parallelogram
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 * 2021-07-31	WH	Removed code that aimed to remove ghost image as this was casuing a notable resource catastrophy within browsers (See Issue#2)
 * 2021-07-29	WH	Money items now operate correctly in terms of duplicating themselves if they are allowed and re-combining when they are placed back into the bank
 * 2021-07-20	WH	Dropping may now occur in the bank section and items will return to the correct collum based on whether they are money or other items
 * 2021-07-20	WH	Modified drop script so items can oly be dropped in empty cells.
 * 2021-07-11	WH	Created required javascript to allow for draggable grid elements
 */

/*Get elements from the page*/
 const draggables = document.querySelectorAll('.gridItems')
 const containers = document.querySelectorAll('.dragReceptical')
 const moneyItemBank = document.getElementById("div_moneyItems")

 /*Contant parameters*/
const maxMoneys = 
{
  M5000 : 1,
  M1000 : 3,
  M500 : 5,
  M200 : 18
}

/*#=========================================================#*/
/*Program variables*/
/*Keeps track of how many of each money type have been used*/
 var numMoneys = 
 {
   M5000 : 1,
   M1000 : 1,
   M500 : 1,
   M200 : 1
 }

 /*#=========================================================#*/
 /*User subs*/
 /*Drag start event listener*/
 function dragstartevent(draggable, event) {
  /*REMOVED DUE TO 'Tanking Effect' (See Issue#2) - event.dataTransfer.setDragImage(draggable, -99999, -99999); /*Move ghost images away to very far away from screen so you can't see them*/
  /*UNFINNISHED - Attemps to create new money item if more are available*/
  if(draggable.classList.contains("itmMoney") && draggable.parentNode.id == "div_moneyItems") {
    const classLists = draggable.classList
    var moneyDuplicate = false
    var afterItem = null /*The previous next most valuable money item that the duplicated item will be inserted before*/
    if (classLists.contains("mon5000") && numMoneys["M5000"] < maxMoneys["M5000"]) {
      numMoneys["M5000"] ++
      moneyDuplicate = true
      afterItem = moneyItemBank.querySelector(".mon1000")
    } else if (classLists.contains("mon1000") && numMoneys["M1000"] < maxMoneys["M1000"]) {
      numMoneys["M1000"] ++
      moneyDuplicate = true
      afterItem = moneyItemBank.querySelector(".mon500")
    } else if (classLists.contains("mon500") && numMoneys["M500"] < maxMoneys["M500"]) {
      numMoneys["M500"] ++
      moneyDuplicate = true
      afterItem = moneyItemBank.querySelector(".mon200")
    } else if (classLists.contains("mon200") && numMoneys["M200"] < maxMoneys["M200"]) {
      numMoneys["M200"] ++
      moneyDuplicate = true
    }

    if (moneyDuplicate) {
      var newDraggable = draggable.cloneNode(true)
      newDraggable.addEventListener('dragstart', (event) => {dragstartevent(newDraggable,event)})
      newDraggable.addEventListener('dragend', () => {dragendevent(newDraggable)})
      console.log(afterItem)
      if (afterItem == null)
      {
        console.log("Should insert to end")
        moneyItemBank.appendChild(newDraggable)
      }
      else {
        console.log("Should insert after")
        moneyItemBank.insertBefore(newDraggable,afterItem)
      }
    }
    
  }
  draggable.classList.add('dragging') /*Add css class that styles the dragging item*/
 }

 function dragendevent(draggable) {
  if (draggable.parentNode.id == "div_moneyItems")
  {
    if (draggable.classList.contains("mon5000") && moneyItemBank.querySelector(".mon5000:not(.dragging)") != null)
    {
      numMoneys["M5000"] --
      draggable.remove()
    } else if (draggable.classList.contains("mon1000") && moneyItemBank.querySelector(".mon1000:not(.dragging)") != null)
    {
      numMoneys["M1000"] --
      draggable.remove()
    } else if (draggable.classList.contains("mon500")  && moneyItemBank.querySelector(".mon500:not(.dragging)") != null)
    {
      numMoneys["M500"] --
      draggable.remove()
    } else if (draggable.classList.contains("mon200")  && moneyItemBank.querySelector(".mon200:not(.dragging)") != null)
    {
      numMoneys["M200"] --
      draggable.remove()
    }
  }
  draggable.classList.remove('dragging') /*Remove dragging css class*/

}
 /*Add event listeners*/
 draggables.forEach(draggable => {
   draggable.addEventListener('dragstart', (event) => {
     dragstartevent(draggable,event)
   })
 
   draggable.addEventListener('dragend', () => {
     dragendevent(draggable)
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
       var classList = draggable.classList
       if (classList.contains("itmMoney"))
       {
          const classLists = draggable.classList
          var afterItem = null /*The previous next most valuable money item that the duplicated item will be inserted before*/
          if (classLists.contains("mon5000")) {
            afterItem = moneyItemBank.querySelector(".mon1000")
          } else if (classLists.contains("mon1000")) {
            afterItem = moneyItemBank.querySelector(".mon500")
          } else if (classLists.contains("mon500")) {
            afterItem = moneyItemBank.querySelector(".mon200")
          } 
          if (afterItem == null)
          {
            moneyItemBank.appendChild(draggable)
          } else
          {
            moneyItemBank.insertBefore(draggable,afterItem)
          }
       } else{
         document.getElementById("div_specialItems").appendChild(draggable)
       }
     }
   })
 })