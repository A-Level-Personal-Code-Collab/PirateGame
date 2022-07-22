import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-banner',
  templateUrl: './banner.component.html',
  styleUrls: ['./banner.component.scss']
})
export class BannerComponent implements OnInit {
  @Input ()
  mainTitle = "No Title Specified"
  @Input ()
  subtitle = "No subtitle specified"

  constructor() { }

  ngOnInit(): void {
  }

}
