import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { GameService } from 'src/app/services/game.service';

@Component({
  selector: 'app-play-start',
  templateUrl: './play-start.component.html',
  styleUrls: ['./play-start.component.scss']
})
export class PlayStartComponent implements OnInit {

  input_game_id = "";
  id_valid = false;

  constructor(private thisRouter: Router, private gameService: GameService) { }

  ngOnInit(): void {
  }

  validateID() {
    // Controls whether you can press the submit button.
    // Replace statement ensures that the length requirement is met with digits only 
    this.id_valid = (this.input_game_id.replace(/[^\x30-\x39]/g, "").length == 8) 
  }

  nextPhase() {
    /* ----------- Check that game exists before moving to next stage ----------- */
    this.gameService.getGame(this.input_game_id).subscribe({
      next: (response) => {
      if (response.status == 200) {
        this.thisRouter.navigate(["/play/join", {"game_id": this.input_game_id}])
      }
    },
    error: (response) => {
      this.id_valid=false; // Temporarily disable button again
      alert("ERROR: Game does not exist!");
    }})
    
  }

}
