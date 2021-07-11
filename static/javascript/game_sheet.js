/**
 * File: /home/will/GitHub Repos/PirateGame/static/javascript/game_sheet.js
 * Project: /home/will/GitHub Repos/PirateGame/static/javascript
 * Created Date: Friday, July 9th 2021, 9:29:43 pm
 * Author: Will Hall
 * -----
 * Last Modified: Sun Jul 11 2021
 * Modified By: Will Hall
 * -----
 * Copyright (c) 2021 Lime Parallelogram
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 * 2021-07-11	WH	Created required javascript to allow for draggable grid elements
 */

/*Get elements from the page*/
 const draggables = document.querySelectorAll('.gridItems')
 const containers = document.querySelectorAll('.gridSquare')
 
 /*Add event listeners*/
 draggables.forEach(draggable => {
   draggable.addEventListener('dragstart', (event) => {
     event.dataTransfer.setDragImage(draggable, -99999, -99999); /*Move ghost images away to very far away from screen so you can't see them*/
     draggable.classList.add('dragging') /*Add css class that styles the dragging item*/
   })
 
   draggable.addEventListener('dragend', () => {
     draggable.classList.remove('dragging') /*Remove dragging css class*/
   })
 })
 
 /*Add drag over event listeners*/
 containers.forEach(container => {
   container.addEventListener('dragover', () => {
     /*Add the itemem with the .dragging class if it is being dragged over a square*/
     const draggable = document.querySelector('.dragging')
     container.appendChild(draggable)
   })
 })