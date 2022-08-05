import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

// Properties for the player that will be completed
export type playerSettings = {
  player_nickname: string;
  player_is_participating: boolean;
  player_is_host: boolean;
  player_game?: string;

  // Not used on server
  nickname_valid: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class PlayerService {

  constructor(private serverService: HttpClient) { }

  createPlayer(player: playerSettings) {
    return this.serverService.post("http://localhost:8000/api/player/", player, {observe: 'response'})
  }
}
