import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import urlJoin from 'url-join'
import { GlobalService } from './global.service';

export interface Version {
  title: string;
  version: string;
  overview: string;
  blocks: [];
}

@Injectable({
  providedIn: 'root'
})
export class PatchnotesService {

  constructor(private http : HttpClient) { }

  getAllPatchnotes() {
    return this.http.get<Array<Version>>(urlJoin(GlobalService.BASE_URL,"api/patch_notes"))
  }

  getPatchnotes(version: string) {
    return this.http.get<Version>(urlJoin(GlobalService.BASE_URL,"/api/patch_notes",version))
  }
}
