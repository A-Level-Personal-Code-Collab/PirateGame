import { Component, OnInit } from '@angular/core';
import { GlobalService } from 'src/app/services/global.service';
import { PatchnotesService, Version } from 'src/app/services/patchnotes.service';
import { StatsService, Statistic, AvailableStats } from 'src/app/services/stats.service';

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.scss']
})
export class IndexComponent implements OnInit {
  currentActiveGames = 0;
  totalGames = 0;

  constructor(private statsService: StatsService) {}

  ngOnInit(): void {
    // Update home page statistics
    this.statsService.getAllStats().subscribe((data: AvailableStats) => {
      this.totalGames = data.total_games;
      this.currentActiveGames = data.current_games
    });
  }

}
