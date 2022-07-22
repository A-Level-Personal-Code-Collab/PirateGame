import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.scss']
})
export class IndexComponent implements OnInit {
  currentActiveGames = 0;
  totalGames = 0;
  constructor() { }

  ngOnInit(): void {
  }

}
