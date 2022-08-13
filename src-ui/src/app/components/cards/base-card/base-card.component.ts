import { Component, Input, OnInit, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'app-base-card',
  templateUrl: './base-card.component.html',
  styleUrls: ['./base-card.component.scss'],
  encapsulation: ViewEncapsulation.ShadowDom
})
export class BaseCardComponent implements OnInit {

  @Input() title = "Card Title";
  @Input() description = "";
  
  constructor() { }

  ngOnInit(): void {
  }

}
