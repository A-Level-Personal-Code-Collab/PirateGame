import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})
export class FooterComponent implements OnInit {
  version = "Version 2.0.0 (Angular Alpha)";

  constructor() {
    
  }

  ngOnInit(): void {
    
  }

}
