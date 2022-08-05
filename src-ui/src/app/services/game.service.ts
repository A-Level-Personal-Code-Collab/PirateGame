import { HttpClient } from '@angular/common/http';
import { EventEmitter, Injectable, Output } from '@angular/core';
import { firstValueFrom } from 'rxjs';

// This information is sent to the server in order to generate a game entry
export type gameProperties = {
  game_id?: string;
  game_title: string;
  game_gameplay_settings: gameplaySettings;

  // Not stored on server
  open_projector: boolean;
}

// Settings related to the actual gameplay. Stored in JSON form in the main game database
export type gameplaySettings = {
  grid_height: number;
  grid_width: number;
}

@Injectable({
  providedIn: 'root'
})
export class GameService {

  @Output() serverResult = new EventEmitter<any>();
  
  constructor(private serverService: HttpClient) { }

  createGame(gameData: gameProperties) {
    return this.serverService.post("http://localhost:8000/api/game/",gameData, {observe: 'response'})

  }
}
