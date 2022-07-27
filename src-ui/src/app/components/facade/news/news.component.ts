import { Component, OnInit } from '@angular/core';
import { GlobalService } from 'src/app/services/global.service';
import { PatchnotesService, Version } from 'src/app/services/patchnotes.service';

@Component({
  selector: 'app-news',
  templateUrl: './news.component.html',
  styleUrls: ['./news.component.scss']
})
export class NewsComponent implements OnInit {
  declare currentVersion: Version;
  
  constructor(private patchnotesService: PatchnotesService) { }

  ngOnInit(): void {
    // Update the patch notes information
    this.patchnotesService.getPatchnotes(GlobalService.CURRENT_VERSION).subscribe((data) => this.currentVersion = data);
  }

}
