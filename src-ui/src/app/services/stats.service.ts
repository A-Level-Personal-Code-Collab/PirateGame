/**
 * File: /src/app/services/stats.service.ts
 * Project: https://github.com/Lime-Parallelogram/angular
 * Created Date: Tuesday, July 26th 2022, 5:40:31 pm
 * Author: Will Hall
 * -----
 * Last Modified: Tue Jul 26 2022
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

@Injectable({
  providedIn: 'root'
})
export class StatsService {

  constructor(private http: HttpClient) { }

  getStat(stat_name : string) {
    let request_url = urlJoin(BASE_URL,"/api/stats",stat_name);
    console.log(request_url)
    return this.http.get<Statistic>(request_url);
  }
}


