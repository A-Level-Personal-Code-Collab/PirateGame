import { HttpClient } from '@angular/common/http';
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

  warningMessage = "Must be at least 3 characters";
  warnClass = "warn";

  csv_text: string[] = [];

  @Output() textChange = new EventEmitter<textOut>()

  constructor(private assetReader: HttpClient) {
    // Pre-Load the CSV of bad words
    this.assetReader.get("assets/nickname-word-blacklist.csv", {"responseType": "text"}).subscribe((data) => {this.csv_text = data.split(",")})
  }

  ngOnInit(): void {
  }

  checkText(event: any) {
    /* -------------------------------------------------------------------------- */
    /*                           Validate the input text                          */
    /* -------------------------------------------------------------------------- */
    let text = event.target.value;
    let ASCII_only_text = text.replace(/[^\x30-\x39&^\x41-\x5A&^\x61-\x7A]/g, "");  // Used for profanity checker

    let tests_passed = 0;
    let total_tests = 3;
    
    /* ------------------------------- Test length ------------------------------ */
    if (text.length >=3) {tests_passed ++} else {this.warningMessage = "Must be at least 3 characters"}
    if (text.length <=15) {tests_passed ++} else {this.warningMessage = "Must be fewer than 16 characters"}


    /* ----------------------- Validate against profanity ----------------------- */
    tests_passed ++
    let checkedWords = 0;

    // Compare all words in banned words list
    while (tests_passed == 3 && checkedWords < this.csv_text.length) {
      let word = this.csv_text[checkedWords]
      let wordLen = word.length
      if (!(wordLen > ASCII_only_text.length)) {
        if (word == ASCII_only_text) {
            this.warningMessage = "Rejected: Profanity"
            tests_passed --
        }
        let numSubstrings = ASCII_only_text.length - wordLen + 1
        for (let i = 0; i < numSubstrings; i++) {
          let substring = ASCII_only_text.substring(i, i+wordLen)
          if (substring == word) {
            this.warningMessage = "Rejected: Contains profanity"
            tests_passed --
          }
        }
      }
      checkedWords ++
    }

    /* ----------------------------- Display outputs ---------------------------- */
    if (tests_passed < total_tests) {
      this.warnClass = "warn"
    } else { this.warnClass = ""; this.warningMessage = ""}

    this.textChange.emit(<textOut>{valid: !!!(total_tests - tests_passed), text: text})
  }

}
