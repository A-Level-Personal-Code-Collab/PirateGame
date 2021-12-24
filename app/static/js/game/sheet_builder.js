/**
 * File: https://github.com/A-Level-Personal-Code-Collab/PirateGame/static/js/game/game_sheet.js
 * Project: https://github.com/A-Level-Personal-Code-Collab/PirateGame/static/javascript
 * Created Date: Friday, July 9th 2021, 9:29:43 pm
 * Author: Will Hall
 * -----
 * Last Modified: Fri Dec 24 2021
 * Modified By: Will Hall
 * -----
 * Copyright (c) 2021 Lime Parallelogram
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 * 2021-12-24	WH	Added handling for progression button to lobby
 * 2021-12-24	WH	Re-implemented 200s filler
 * 2021-12-23	WH	Added scroll method for item bank
 * 2021-12-23	WH	Added handling for deletion of elements
 * 2021-12-23	WH	Added checks for empty stacks and relevant class modifiers
 * 2021-12-23	WH	Added right-click functionality to bring up delete menu
 * 2021-12-23	WH	Added selection functionality from new item bank
 * 2021-12-23	WH	Removed all dragging functionality
 * 2021-12-23	WH	On-Resize method ensures that grid and elements are correct size
 * 2021-12-23	WH	Begin addition of click and drop infrastructure
 * 2021-11-07	WH	Fixed issue where items could not be added back to the bank (Issue #152)
 * 2021-11-07	WH	References item type based on their id as oppose to a CSS class that they had
 * 2021-11-07	WH	Update counters routine now always recounts from scratch in order to simplify code
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
 const itemStacks = document.querySelectorAll('div.itemStack')
 const containers = document.querySelectorAll('.dragReceptacle')
 const itemPicker = document.getElementById("div_itemPicker")
 const squareControls = document.getElementById("div_squareControls");
 const toLobby = document.getElementById("btn_toLobby")

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
 var selectedStack = null;
 var selectedContainer = null;
 var touchTimer;
 var intentionalForward = false; //Sets whether the forwarding is intended

 //=========================================================//
 //====================== User subs ========================//
 //=========================================================//
 //=========================================================//
 //^ Perform all functions that should run when the space loads //
 function on_load() {
  /*--*/
  //Adds leave page confirmation
  window.addEventListener("beforeunload", function(event) {if (!intentionalForward) {event.returnValue = "Do you really wish to leave this site?"; return "Do you really wish to leave this site?";}});
  
  /*---------------*/
  /* Fitty & Dimension Adjustments */
  function adjustDimension() {
    fitty("#fitty_container")
    var requiredDimension = window.getComputedStyle(containers[1], null).getPropertyValue("width");
    
    //Fix the width of the grid squares to their default value
    document.querySelectorAll(".gridSquare").forEach((element) => {
      element.style.height  = requiredDimension;
    })
  }

  adjustDimension();
  window.addEventListener("resize", adjustDimension);

  /*---------------*/
  /*Update the counters on the page*/
  update_counters();

  /*---------------*/
  /*Add event listeners*/
  containers.forEach(container => {
    container.addEventListener('contextmenu', openSquareMenu)
    container.addEventListener('touchstart', function (event) {touchTimer = setTimeout(function () {openSquareMenu(event)}, 500);})
    container.addEventListener('touchend', function (event) {if (touchTimer) {clearTimeout(touchTimer); placeItem(event);}})
    container.addEventListener('click', placeItem);
  })

  //The item bank stacks themselves
  itemStacks.forEach(item => {
    item.addEventListener('click', selectItem);
  })

  selectedStack = itemStacks[0];
  selectedStack.classList.add("selectedStack");

  //Clicking outside of popup closes it
  document.addEventListener("click", function () {squareControls.style.display = "none";});

  //Allow scrolling of item bank if required
  const scrollContainer = document.querySelector("#div_itemPicker");

  scrollContainer.addEventListener("wheel", (evt) => {
      evt.preventDefault();
      scrollContainer.scrollLeft += evt.deltaY;
  });

  // Fill remaining squares with 200s
  document.getElementById("div_m200Stack").addEventListener('dblclick',fill_200s)

 }
 
 //^ -------------------------- Facilitate the placement and dropping of items ------------------------- ^//
 function selectItem(event) //Allows the user to select the type of item stack they wish to place
 {
  if (is_available(event.target.childNodes[0].id))
  {
    selectedStack.classList.remove("selectedStack");
    selectedStack = event.target;
    selectedStack.classList.add("selectedStack");
  }
 }

 function placeItem(event) //Allows the user to select the target cell for their new item
 {
    var container = event.target;
    if (container.innerHTML == "") {
      squareControls.style.display = "none";
      if (is_available(selectedStack.childNodes[0].id)) {
        var newItem = selectedStack.childNodes[0].cloneNode(true);
        newItem.classList.remove("selectedStack");
        container.appendChild(newItem);
        update_counters();
      }
    }
 }

 function openSquareMenu(event) { //Open the deletion menu
  event.preventDefault();
  var container = event.target;
  if (container.innerHTML != "") { //Check container has something in it to manipulate
    //Places popup controls
    var boundingRect = container.getBoundingClientRect();
    var top = boundingRect.top;
    var left = boundingRect.left + boundingRect.width/2;

    squareControls.style.display = "block";
    squareControls.style.top = top - squareControls.clientHeight +"px";
    squareControls.style.left = left - squareControls.getBoundingClientRect().width/2 +"px";
    selectedContainer = container;

  }
 }

 //Delete an item from your grid
 function deleteItem() {
   squareControls.style.display = "none"; //Hide the controls again
   selectedContainer.removeChild(selectedContainer.firstChild);
   update_counters();
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
        grid[squareRow][squareCol] = item.id;
      }
    })
    
    /*--*/
    //Return output
    return grid;
 }

 //=========================================================//
 //^ Check if grid is full or not ^//
 function is_grid_full()
 {
   for (var i = 0; i < containers.length; i++)
   {
     if (containers[i].innerHTML == "") {return false;} //Checks to see if each container is empty and if so returns false
   }
   return true;
 }

 function is_grid_ready() {
   if (is_grid_full())
   {
     toLobby.disabled = false;
   }
   else {
     toLobby.disabled = true;
   }
 }
 
 //=========================================================//
 //^ Update all item stack counters ^//
 function update_counters(plusOne = 0)
 {
   var allItems = document.querySelectorAll('div.gridItems');
   numItems = {...maxItems}; //Start negative count from maxItems
   numItems[plusOne] ++; //Add extra value on plusOne item

   allItems.forEach(itm => {
     if (!itm.parentNode.classList.contains("itemStack")){ //Ignore items in the stacks in count
      numItems[itm.id] --;
     }
    document.getElementById(itm.id+"_counter").innerHTML = numItems[itm.id]; //Update counter spans
   })
  
   check_empty_stacks();
   is_grid_ready();
 }

 //=========================================================//
 //^ Check for empty stacks and give them appropriate classes ^//
 function check_empty_stacks() {
   itemStacks.forEach(itm => {
    var itemID = itm.childNodes[0].id; //Get the id of the items in the stack
    if (numItems[itemID] == 0)
    {
      itm.classList.add("emptyStack"); //Adds the empty stack class to show items have been exhausted

      //If the stack is selected then un-select it and select something else
      if (itm.classList.contains("selectedStack")) {
        itm.classList.remove("selectedStack");
        const nextItem = document.querySelector(".itemStack:not(.emptyStack)");
        if (nextItem != null)
        {
          selectedStack = nextItem;
          selectedStack.classList.add("selectedStack");
        }
      }

    } else
    {
      itm.classList.remove("emptyStack");
    }
   })
 }

 //=========================================================//
 //^ Check if a given item is available to be placed ^//
 function is_available(itemID) {
   if (numItems[itemID] > 0) {return true;} else {return false;}
 }

 //=========================================================//
 //^ Fill in remaining 200s ^//
 function fill_200s(event)
 {
   var originalM200 = event.target.childNodes[0];
   containers.forEach(square => {
     if (numItems["M200"] > 0) //Checks if there are 200s left
     {
       if (square.innerHTML == "") //Only adds to empty cells
       {
         var newNote = originalM200.cloneNode(true); //Clones from original

         //Adds event listeners to cloned item
         newNote.addEventListener('dragstart', (event) => {dragstartevent(event)});
         newNote.addEventListener('dragend', (event) => {dragendevent(event)});

         square.appendChild(newNote); //Adds cloned item to empty square
         numItems["M200"] --;
       }
     } else //Breaks loop if 200s have run out
     {
       return true;
     }
   })

   /*--*/
   update_counters();
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
   xhr.send(`grid=${grid}`);

 }

 //=========================================================//
 //^ Run the on page load scrips//
 on_load()