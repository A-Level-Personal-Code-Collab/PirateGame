import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PatchnotesService, Version } from 'src/app/services/patchnotes.service';

@Component({
  selector: 'app-patch-page',
  templateUrl: './patch-page.component.html',
  styleUrls: ['./patch-page.component.scss']
})
export class PatchPageComponent implements OnInit {
  // Test releases
  releases: Array<Version> = [];

  constructor(private router: Router, private patchnotesService: PatchnotesService) { }

  ngOnInit(): void {
    this.patchnotesService.getAllPatchnotes().subscribe((data) => {
      this.releases = data;
    })
  }

  // Jump to version information
  jumpTo(section : string) {
    this.router.navigate([], {fragment: section});
  }

}
