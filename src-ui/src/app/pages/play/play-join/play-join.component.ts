import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { PlayerService, playerSettings } from 'src/app/services/player.service';

@Component({
  selector: 'app-play-join',
  templateUrl: './play-join.component.html',
  styleUrls: ['./play-join.component.scss']
})
export class PlayJoinComponent implements OnInit {

  player_settings: playerSettings = {
    player_nickname: "",
    player_is_host: false,
    player_is_participating: true,

    // Not required on server
    nickname_valid: false
  }

  constructor(private playerService: PlayerService, private route: ActivatedRoute, private routerService: Router) { }

  ngOnInit(): void {
    this.player_settings.player_game = this.route.snapshot.params['game_id'];
  }

  submitPlayer() {
    // Set nickname to projector if player is not participating
    if (!this.player_settings.player_is_participating) {
      this.player_settings.player_nickname = "projector"
    }

    this.playerService.createPlayer(this.player_settings).subscribe({
      next: (server_response) => {
      if (server_response.status == 201) {
        this.player_settings.player_id = (<playerSettings>server_response.body).player_id
        
        /* -------------------- Proceed to next phase of the game ------------------- */
        if (this.player_settings.player_id) {
          localStorage.setItem("player_id", this.player_settings.player_id)

          // Move to grid builder page
          if (this.player_settings.player_is_participating) {
            this.routerService.navigate(["/play/game/builder"])
          } else {
            //! This will represent moving to a view only page
            this.routerService.navigate(["/play/game/builder"])
          }
          
        }
        
      }},
      error: error => alert("Server Error, Could not create player.") })
  }

}
