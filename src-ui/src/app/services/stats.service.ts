/**
 * File: /src/app/services/stats.service.ts
 * Project: https://github.com/Lime-Parallelogram/angular
 * Created Date: Tuesday, July 26th 2022, 5:40:31 pm
 * Author: Will Hall
 * -----
 * Last Modified: Wed Jul 27 2022
 * Modified By: Will Hall
 * -----
 * Copyright (c) 2022 Lime Parallelogram
 * ------------------------------------
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	---------------------------------------------------------
 */
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import urlJoin from 'url-join'

const BASE_URL = "http://localhost:8000/"

export interface Statistic {
    stat_value: number;
}

// Interface that shows all statistics that come in from the server
export interface AvailableStats {
  total_games: number;
  current_games: number;
}

@Injectable({
  providedIn: 'root'
})
export class StatsService {

  constructor(private http: HttpClient) { }

  getStat(stat_name : string) {
    let request_url = urlJoin(BASE_URL,"/api/stats",stat_name);
    return this.http.get<Statistic>(request_url);
  }

  // Get a dictionary of all available statistics
  getAllStats() {
    let request_url = urlJoin(BASE_URL,"/api/stats");
    return this.http.get<AvailableStats>(request_url);
  }
}


