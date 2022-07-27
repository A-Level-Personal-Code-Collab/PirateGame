import { Injectable } from '@angular/core';


@Injectable({
  providedIn: 'root'
})
export class GlobalService {
  // Define global variables used across the front-end
  public static BASE_URL = "http://localhost:8000/"
  public static CURRENT_VERSION = "2.0.0(B)"

  constructor() { }
}
