/**
 * File: https://github.com/A-Level-Personal-Code-Collab/PirateGame/static/javascript/game_sheet.js
 * Project: https://github.com/A-Level-Personal-Code-Collab/PirateGame/static/javascript
 * Created Date: Friday, July 9th 2021, 9:29:43 pm
 * Author: Will Hall
 * -----
 * Last Modified: Sun Aug 01 2021
 * Modified By: Will Hall
 * -----
 * Copyright (c) 2021 Lime Parallelogram
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 * 2021-08-01	WH	Tidied up code significantly including making stacking mechanic work for all items (not just money) and adding iteration to acheive this
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
 const specialItemBank = document.getElementById("div_specialItems")

 /*=========================================================*/
 /*Contant parameters*/
 /*--*/
 /*Constant variable for the maximumum amount of each type of item*/
 const maxItems = 
 {
  M5000 : 1,
  M1000 : 3,
  M500 : 5,
  M200 : 18,
  itmShield : 1,
  itmKill : 1,
  itmSteal : 1,
  itmMirror : 1,
  itmBomb : 1,
  itmBank : 2,
  itmSwap : 1,
  itmGift : 1
 }

 /*--*/
 /*The order of items in the item bank (not this does not affect the actual rendering order)*/
 const itemOrder = ["itmShield","itmKill","itmSteal","itmMirror","itmBomb","itmBank","itmSwap","itmGift",null,"M5000","M1000","M500","M200",null]

 /*=========================================================*/
 /*Program variables*/
 /*--*/
 /*Keeps track of how many of each money type have been used*/
 var numItems = 
 {
   M5000 : 1,
   M1000 : 1,
   M500 : 1,
   M200 : 1,
   itmKill : 1,
   itmSteal : 1,
   itmSwap : 1,
   itmGift : 1,
   itmSheild : 1,
   itmMirror : 1,
   itmBomb : 1,
   itmBank : 1
 }
 /*-*/

 /*#=========================================================#*/
 /*User subs*/
 /*=========================================================*/
 /*Drag start event listener*/
 function dragstartevent(draggable, event) {
  /*REMOVED DUE TO 'Tanking Effect' (See Issue#2) - event.dataTransfer.setDragImage(draggable, -99999, -99999); /*Move ghost images away to very far away from screen so you can't see them*/
  if(draggable.parentNode.id == "div_specialItems" | draggable.parentNode.id == "div_moneyItems") {
    const classList = draggable.classList
    var duplicate = false /*Whether a duplication event is permitted*/
    var afterItem = null /*The next item in the list that the duplicated item will be inserted before*/
    var afterItemLocation = null /*The location within itemOrder of the item after the current one*/

    /*--*/
    classList.forEach(cssclass => {
      if (maxItems[cssclass] != null) /*Igores other classes that don't determine item type*/
      {
        if (numItems[cssclass] < maxItems[cssclass]) /*Checks if a new item can be created*/
        {
          duplicate = true
          numItems[cssclass] ++
          afterItemLocation = itemOrder.indexOf(cssclass)+1
        }
      }
    })

    /*--*/
    if (duplicate) {
      /*Cone existing draggable and set up required listeners on new one*/
      var newDraggable = draggable.cloneNode(true)
      newDraggable.addEventListener('dragstart', (event) => {dragstartevent(newDraggable,event)})
      newDraggable.addEventListener('dragend', () => {dragendevent(newDraggable)})

      /*--*/
      if (classList.contains('itmMoney')) {var itemContainer = moneyItemBank} else {var itemContainer = specialItemBank} /*Chose whether duplicated item will be in money or special item box*/
      afterItem = itemContainer.querySelector("."+itemOrder[afterItemLocation])
      /*Either put the duplicated item at the end of the box or at its proper location*/
      if (afterItem == null) {itemContainer.appendChild(newDraggable)}
      else {itemContainer.insertBefore(newDraggable,afterItem)}

    }
    
  }
  draggable.classList.add('dragging') /*Add css class that styles the dragging item*/
 }
 
 /*=========================================================*/
 /*Drag end function - when the user stops dragging an item*/
 function dragendevent(draggable) {
  /*Handles the restacking of the items if they are dropped over the item bank*/
  if (draggable.parentNode.id == "div_moneyItems" | draggable.parentNode.id == "div_specialItems")
  {
    if (draggable.classList.contains('itmMoney')) {var itemContainer = moneyItemBank} else {var itemContainer = specialItemBank} /*Chose whether duplicated item will be in money or special item box*/
    draggable.classList.forEach(cssclass => {
      if (maxItems[cssclass] != null)
      {
        if (itemContainer.querySelector(`.${cssclass}:not(.dragging)`) != null)
        {
          numItems[cssclass] --
          draggable.remove()
        }

      }
    })
   
  }
  draggable.classList.remove('dragging') /*Remove dragging css class*/

 }

 /*=========================================================*/
 /*Drag over function will detect when a user drags a draggable image over the top of a square*/
 function dragoverevent(container) {
  if(container.innerHTML=="") { /*Prevents dragging into occupied squares*/
    /*Add the itemem with the .dragging class if it is being dragged over a square*/
    const draggable = document.querySelector('.dragging')
    container.appendChild(draggable)
    draggable.style.display="block"
  }

  /*Allow draggable item to be placed back into the item bank*/
  if (container.id == "div_itemBank") {
    const draggable = document.querySelector(".dragging")
    var classList = draggable.classList

    if (draggable.classList.contains('itmMoney')) {var recipientContainer = moneyItemBank} else {var recipientContainer = specialItemBank} /*Chose whether duplicated item will be in money or special item box*/
    
    /*--*/
    classList.forEach(cssclass => {
      if (maxItems[cssclass] != null)
      {
        if (recipientContainer.querySelector(`.${cssclass}:not(.dragging)`) != null) {draggable.style.display="none"} /*Hide element if it is being dragged over bank and the bank already contains this item*/
      
        /*Add item to correct place on dragover*/
        var nextItemLocation = itemOrder.indexOf(cssclass) + 1 /*Finds current asset in order array in order to determine next one*/
        var nextAsset = recipientContainer.querySelector("."+itemOrder[nextItemLocation])
        if (nextAsset == null) {recipientContainer.appendChild(draggable)}
        else {recipientContainer.insertBefore(draggable,nextAsset)}
      }
    })
  }
 }
 
 /*=========================================================*/
 /*Perform all functions that should run when the space loads*/
 function on_load() {
   /*--*/
  /*Add event listeners*/
  /*Adds events to actual draggable items*/
  draggables.forEach(draggable => {
    draggable.addEventListener('dragstart', (event) => {dragstartevent(draggable,event)})
    draggable.addEventListener('dragend', () => {dragendevent(draggable)})
  })

  /*Add drag over event listeners to each of the grid sqaures*/
  containers.forEach(container => {
    container.addEventListener('dragover', () => {dragoverevent(container)})
  })
 }
 
 /*=========================================================*/
 /*Run the on page load scrips*/
 on_load()