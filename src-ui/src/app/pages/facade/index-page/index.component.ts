import { Component, OnInit } from '@angular/core';
import { StatsService, Statistic } from 'src/app/services/stats.service';

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
    this.statsService.getStat("/total_games").subscribe((data: Statistic) => this.totalGames = data.stat_value)
  }

}
