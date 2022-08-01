import { Component, EventEmitter, OnInit, Output, Input, ElementRef } from '@angular/core';

@Component({
  selector: 'app-pg-toggle',
  templateUrl: './pg-toggle.component.html',
  styleUrls: ['./pg-toggle.component.scss']
})
export class PgToggleComponent implements OnInit {
  @Input() default: boolean = false;

  @Output() interactions = new EventEmitter()

  @Input() checked: Boolean = false;

  constructor(private elt: ElementRef) { }

  ngOnInit(): void {
    if (this.default) {
      console.log(this.default)
    }
  }

  checkChanged(event: any) {
    this.checked = event.target.checked
    this.interactions.emit(this.checked)

  }

}
