import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
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
    this.patchnotesService.getAllPatchnotes().subscribe((data) => { // Sort versions with newest at top.
      this.releases = data.sort((i1,i2) => {
        if (i1.version < i2.version) {
          return 1;
        }

        else if (i1.version > i2.version) {
          return -1;
        }

        return 0;
      });
      
    })
    
  }


  // Jump to version information
  jumpTo(section : string) {
    this.router.navigate([], {fragment: section});
    if (section == "") { window.scrollTo(0,0); }
  }

}
