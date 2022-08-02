import { Component, EventEmitter, OnInit, Output, Input, ElementRef } from '@angular/core';

@Component({
  selector: 'app-pg-toggle',
  templateUrl: './pg-toggle.component.html',
  styleUrls: ['./pg-toggle.component.scss']
})
export class PgToggleComponent implements OnInit {
  @Input() default: boolean = false;

  @Output() checkedChange = new EventEmitter<boolean>();

  @Input() checked: boolean = false;

  constructor(private elt: ElementRef) { }

  ngOnInit(): void {
  }

  checkChanged(event: any) {
    this.checkedChange.emit(this.checked)
  }

}
