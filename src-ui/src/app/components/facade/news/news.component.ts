import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-news',
  templateUrl: './news.component.html',
  styleUrls: ['./news.component.scss']
})
export class NewsComponent implements OnInit {
  currentVersion = {
    "title": "Please update me",
    "overview": "Porting over to angular",
    "link": "NO LINK"
  }

  constructor() { }

  ngOnInit(): void {
  }

}
