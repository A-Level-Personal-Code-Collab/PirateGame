import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { GameService } from 'src/app/services/game.service';
import { gameplaySettings, gameProperties } from 'src/app/services/game.service';
import { PlayerService, playerSettings } from 'src/app/services/player.service';

@Component({
  selector: 'app-play-create',
  templateUrl: './play-create.component.html',
  styleUrls: ['./play-create.component.scss']
})
export class PlayCreateComponent implements OnInit {

  // Game settings is a subset of gameProperties. These dictate how the game is actually played
  public gameplay_settings: gameplaySettings = {
    grid_height: 6,
    grid_width: 6
  };

  public new_game: gameProperties = {
    game_title: "",
    game_gameplay_settings: this.gameplay_settings,

    // Not required for server
    open_projector: false,
  };

  public player_settings: playerSettings = {
    player_nickname: "",
    player_is_participating: true,
    player_is_host: true,

    // Not used on server
    nickname_valid: false,
  };

  button_enable = false;

  constructor(private gameService: GameService, private playerService: PlayerService, private routerService: Router) { }

  ngOnInit(): void {
  }

  checkValues() {
    // Check if the user is participating
    this.button_enable = this.player_settings.nickname_valid;

  }

  /* ------------- Called by submit button - create game on server ------------ */
  submitGame() {
    this.new_game.game_title = this.player_settings.player_nickname + "'s Pirate Game";

    if (this.new_game.game_id) { this.submitPlayer() } // If a game already exists for any reason, move to create a player

    /* -------------------- Create a new game on the server ------------------- */
    else {
      this.gameService.createGame(this.new_game).subscribe({
        next: (server_response) => {
        if (server_response.status == 201 && server_response.body) {
          this.new_game.game_id = (<gameProperties>server_response.body).game_id
          this.player_settings.player_game = this.new_game.game_id
  
          this.submitPlayer()
        }},
        error: error => alert("Server Error, Could not create game.") })
    }
  }

  /* ----------------------- Create new player on server ---------------------- */
  submitPlayer() {
    this.playerService.createPlayer(this.player_settings).subscribe({
      next: (server_response) => {
      if (server_response.status == 201) {
        this.toNextStep()
      }},
      error: error => alert("Server Error, Could not create player.") })
  }

  /* ------------------------- Move user to next page ------------------------- */
  toNextStep() {
    console.log("Will now move to sheet builder")
    //// this.routerService.navigate(["/play/builder"])
  }

}
