/**
 * File: https://github.com/A-Level-Personal-Code-Collab/PirateGame/static/javascript/game_sheet.js
 * Project: https://github.com/A-Level-Personal-Code-Collab/PirateGame/static/javascript
 * Created Date: Friday, July 9th 2021, 9:29:43 pm
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
 * 2021-09-27	WH	Added leave page confirmation
 * 2021-08-05	WH	Added stack counters to each item including their update routines
 * 2021-08-05	WH	Completely rewrote bank system grey-out items when a stack is exhausted
 * 2021-08-02	WH	Added function to show and hide the finished pop-up based on whether the grid is full or not
 * 2021-08-02	WH	Added grid builder function in preparation to send grid to server
 * 2021-08-01	WH	Tidied up code significantly including making stacking mechanic work for all items (not just money) and adding iteration to achieve this
 * 2021-07-31	WH	Removed code that aimed to remove ghost image as this was causing a notable resource catastrophe within browsers (See Issue#2)
 * 2021-07-29	WH	Money items now operate correctly in terms of duplicating themselves if they are allowed and re-combining when they are placed back into the bank
 * 2021-07-20	WH	Dropping may now occur in the bank section and items will return to the correct column based on whether they are money or other items
 * 2021-07-20	WH	Modified drop script so items can oly be dropped in empty cells.
 * 2021-07-11	WH	Created required javascript to allow for draggable grid elements
 */

 //=========================================================//
 //^ Get elements from the page ^//
 const draggables = document.querySelectorAll('div.gridItems')
 const containers = document.querySelectorAll('.dragReceptacle')
 const moneyItemBank = document.getElementById("div_moneyItems")
 const specialItemBank = document.getElementById("div_specialItems")
 const popupDiv = document.getElementById("div_gridFullPopUp")

 //=========================================================//
 //^ Constant parameters ^//
 /*--*/
 /*Constant variable for the maximum amount of each type of item*/
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
 var GRID_X = 6;
 var GRID_Y = 6;

 //=========================================================//
 //^ Program variables //
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
   itmShield : 1,
   itmMirror : 1,
   itmBomb : 1,
   itmBank : 1
 }

 /*--*/
 var draggingCurrent = null; //Stores the items that is currently being moved around
 var intentionalForward = false; //Sets whether the forwarding is intended

 //=========================================================//
 //====================== User subs ========================//
 //=========================================================//
 //^ Drag start event listener //
 function dragstartevent(event) {
  var draggable = event.target;
  /*REMOVED DUE TO 'Tanking Effect' (See Issue#2) */ ////event.dataTransfer.setDragImage(draggable, -99999, -99999); /*Move ghost images away to very far away from screen so you can't see them*/
  if(draggable.parentNode.classList.contains("itemStack")) { //Checks if the item is coming from the bank
    /*--*/
    draggable.classList.forEach(cssclass => {
      if (numItems[cssclass] != null) /*Ignores other classes that don't determine item type*/
      {
        if (numItems[cssclass] > 0) /*Checks if a new item can be created*/
        {
          numItems[cssclass] --;
          draggingCurrent = draggable.cloneNode(true);

          //Adds event listeners to cloned item
          draggingCurrent.addEventListener('dragstart', (event) => {dragstartevent(event)});
          draggingCurrent.addEventListener('dragend', (event) => {dragendevent(event)});
        }
      }
    })

    
  } else {draggingCurrent = draggable;} //If item doesn't originate from bank, don't duplicate it
  
  /*--*/
  draggingCurrent.classList.add('dragging'); /*Add css class that styles the dragging item*/
 }
 
 //=========================================================//
 //^ Drag end function - when the user stops dragging an item //
 function dragendevent(event) {
  /*Handles the restacking of the items if they are dropped over the item bank*/
  if (draggingCurrent.parentNode.id == "div_itemBank")
  {
      draggingCurrent.classList.forEach(cssclass => {
      if (numItems[cssclass] != null) //Ignores irrelevant classes
      {
          //Removes item if is dragged over the bank
          numItems[cssclass] ++; //Increments available items
          draggingCurrent.remove();
      }
    })
  }

  try{draggingCurrent.classList.remove('dragging') /*Remove dragging css class*/} catch {} //Hides error generated by trying to remove class from deleted object
  
  /*--*/
  if (is_grid_full()) {popupDiv.style.display = "block"} else {popupDiv.style.display = "none"} //Checks if grid is full and pops up finnish popup

  /*--*/
  update_counters(null);
 }

 //=========================================================//
 //^ Drag over function will detect when a user drags a draggable image over the top of a square //
 function dragoverevent(container) {
  if(container.innerHTML=="") { /*Prevents dragging into occupied squares*/
    container.appendChild(draggingCurrent)
    draggingCurrent.style.display="block" //Ensures item is shown again
    update_counters(null) //Updates counters with no extra 1
  }
  /*--*/
  if (container.id == "div_itemBank") //Handles item differently if dragged over bank
  {
    draggingCurrent.classList.forEach(cssclass => {if (numItems[cssclass] != null) {update_counters(cssclass)}}) //Updates counters, 1 is added to the cssclass to show where item will be added to without actually changing the numItems variable
    container.appendChild(draggingCurrent)
    draggingCurrent.style.display="none" //Hides item as it is dragged over the bank
   
  }
 }
 
 //=========================================================//
 //^ Perform all functions that should run when the space loads //
 function on_load() {
  /*--*/
  //Adds leave page confirmation
  window.addEventListener("beforeunload", function(event) {if (!intentionalForward) {event.returnValue = "Do you really wish to leave this site?"; return "Do you really wish to leave this site?";}});
    
  /*---------------*/
  /*Add event listeners*/
  /*Adds events to actual draggable items*/
  draggables.forEach(draggable => {
    draggable.addEventListener('dragstart', (event) => {dragstartevent(event)})
    draggable.addEventListener('dragend', (event) => {dragendevent(event)})


    /*---------------*/
    /* Fitty */ 
    fitty("#fitty_container")
  })

  /*Add drag over event listeners to each of the grid squares*/
  containers.forEach(container => {
    container.addEventListener('dragover', () => {dragoverevent(container)})
  })

  //Event listener for on completion button
  document.getElementById("btn_grid_done").addEventListener("click", send_grid);

  //Adds double click listener to 200s
  document.querySelector(".M200").addEventListener("dblclick", fill_200s, event)

  /*--*/
  //Parse JSONs from server (data brought in in gameSheet.html script tag)
  numItems = JSON.parse(itemsJSONString);
  var gridJSON = JSON.parse(gridJSONString);

  GRID_X = gridJSON["GRID_X"]
  GRID_Y = gridJSON["GRID_Y"]

  /*--*/
  update_counters(null);
 }
 
 //=========================================================//
 //^ Generate a grid matrix ready to send it back to the server //
 function generate_grid()
 {
   //Create empty 2D array in grid size
   var grid = new Array(GRID_Y);
   for (var i = 0; i < grid.length; i++)
   {
     grid[i] = new Array(GRID_X)
   }

   /*--*/
   //Loop through all items and find the cell that they are in
   const placedItems = document.querySelectorAll("div.gridItems")

   placedItems.forEach(item => 
    {
      
      var squareID = item.parentNode.id
      if (squareID.substring(0,8) == "tdt_grid") //Check if any items left in bank and break if so break the loop
      {
        var squareCol = squareID.charCodeAt(8) - 65 //Convert the capital letter into a number by taking away the unicode value of 'A'
        var squareRow = Number(squareID.substring(9)) - 1 //Convert remainder of ID to a number (should support 2 digit numbers)
        
        //Find class of interest from class list
        item.classList.forEach(cssclass => {
          if (numItems[cssclass] != null) //Discard classes that do not determine item type
          {
            grid[squareRow][squareCol] = cssclass;
          }
        })
      }
    })
    
    /*--*/
    //Return output
    return grid;
 }

 //=========================================================//
 //^ Check if grid is full or not //
 function is_grid_full()
 {
   for (var i = 0; i < containers.length; i++)
   {
     if (containers[i].innerHTML == "") {return false;} //Checks to see if each container is empty and if so returns false
   }
   return true;
 }
 
 //=========================================================//
 //^ Update all item stack counters//
 function update_counters(plusOne)
 {
   draggables.forEach(itm => {
     itm.classList.forEach(cssclass => {
       if (numItems[cssclass] != null) //Ignores non-identifying css classes
       {
         var count = numItems[cssclass];
         if (plusOne == cssclass) {count++;} //If the item is being dragged over the bank add one just to show where it would be added
         document.getElementById(cssclass+"_counter").innerHTML = count; //Update counter spans
         if (count == 0)
         {
           itm.classList.add("emptyStack") //Adds the empty stack class to show items have been exhausted
           itm.draggable = false; //Prevents further dragging of items
         } else
         {
          itm.classList.remove("emptyStack")
          itm.draggable = true;
         }
       }
     })
   })
 }

 //=========================================================//
 //^ Fill in remaining 200s ^//
 function fill_200s(event)
 {
   var originalM200 = event.target;
   containers.forEach(square => {
     if (numItems["M200"] > 0) //Checks if there are 200s left
     {
       if (square.innerHTML == "") //Only adds to empty cells
       {
         var newNote = originalM200.cloneNode(true) //Clones from original

         //Adds event listeners to cloned item
         newNote.addEventListener('dragstart', (event) => {dragstartevent(event)});
         newNote.addEventListener('dragend', (event) => {dragendevent(event)});

         square.appendChild(newNote) //Adds cloned item to empty square
         numItems["M200"] --;
       }
     } else //Breaks loop if 200s have run out
     {
       return true;
     }
   })

   /*--*/
   update_counters();
   if (is_grid_full()) {popupDiv.style.display = "block"} else {popupDiv.style.display = "none"} //Checks if grid is full and pops up finnish popup
 }

 //=========================================================//
 //^ Send completed grid layout to server ^//
 function send_grid()
 {
   var grid = generate_grid();

   var xhr = new XMLHttpRequest();
   var thisURL = window.location.href;
   xhr.open("POST",thisURL,true);
   xhr.onreadystatechange = function() {
    if (xhr.readyState == XMLHttpRequest.DONE) {
      intentionalForward = true;
      window.location.href = xhr.responseURL;
    }
}
   xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
   xhr.send(`grid=${grid}`)

 }

 //=========================================================//
 //^ Run the on page load scrips//
 on_load()