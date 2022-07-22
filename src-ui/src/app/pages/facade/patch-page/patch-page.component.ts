import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-patch-page',
  templateUrl: './patch-page.component.html',
  styleUrls: ['./patch-page.component.scss']
})
export class PatchPageComponent implements OnInit {
  // Test releases
  releases = [{"versionNo": "TEST", "title": "Test Release"},{"versionNo": "TEST2", "title": "Test Release Number 2", "overview":"Release overview", "pageChanges": [{"title" : "Page1", "changes": ["change 1"]}]}]
  constructor(private router: Router) { }

  ngOnInit(): void {
  }

  // Jump to version information
  jumpTo(section : string) {
    this.router.navigate([], {fragment: section});
  }

}
