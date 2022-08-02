import { Component, OnInit } from '@angular/core';
import { PgToggleComponent } from 'src/app/widgets/pg-toggle/pg-toggle.component';

type gameSettings = {
  host_nickname: string;
  nickname_valid: boolean;
  host_participate: boolean;
  open_projector: boolean;
}

@Component({
  selector: 'app-play-create',
  templateUrl: './play-create.component.html',
  styleUrls: ['./play-create.component.scss']
})
export class PlayCreateComponent implements OnInit {

  public game_settings: gameSettings = {
    host_nickname: "",
    nickname_valid: false,
    host_participate: false,
    open_projector: false,
  };

  button_enable = false;

  constructor() { }

  ngOnInit(): void {
  }

  ngAfterViewInit(): void {
  }

  checkValues() {
    // Check if the user is participating
    this.button_enable = this.game_settings.nickname_valid;

  }

}
