import { Component, EventEmitter, OnInit, Output } from '@angular/core';

interface textOut {
  valid: boolean;
  text: string;
}

@Component({
  selector: 'app-nickname-input',
  template: `<div><input maxlength=15 type="text" (input)="checkText($event)"><span class="{{warnClass}}"><span class="tooltip_text">{{ warningMessage }}</span></span></div>`,
  styleUrls: ['./nickname-input.component.scss']
})
export class NicknameInputComponent implements OnInit {

  warningMessage = "Must be at least 3 characters"
  warnClass = "warn"

  @Output() textChange = new EventEmitter<textOut>()

  constructor() { }

  ngOnInit(): void {
  }

  checkText(event: any) {
    let text = event.target.value;

    let tests_passed = 0;
    let total_tests = 2;
    
    // Test length
    if (text.length >=3) {tests_passed ++} else {this.warningMessage = "Must be at least 3 characters"}
    if (text.length <=15) {tests_passed ++} else {this.warningMessage = "Must be fewer than 16 characters"}

    // Display outputs
    if (tests_passed < total_tests) {
      this.warnClass = "warn"
    } else { this.warnClass = ""; this.warningMessage = ""}

    this.textChange.emit(<textOut>{valid: !!!(total_tests - tests_passed), text: text})
  }

}
