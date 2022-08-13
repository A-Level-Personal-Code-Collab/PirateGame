import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import { playerSettings } from 'src/app/services/player.service';

@Component({
  selector: 'app-my-profile',
  templateUrl: './my-profile.component.html',
  styleUrls: ['./my-profile.component.scss']
})
export class MyProfileComponent implements OnInit {

  @Input() player_settings: playerSettings = {
    player_nickname: "",
    player_is_participating: true,
    player_is_host: false,

    // Not used on server
    nickname_valid: false,
  };

  @Output() player_settingsChange = new EventEmitter<playerSettings>();
  
  constructor() { }

  ngOnInit(): void {
  }

  emitChanged() {
    this.player_settingsChange.emit(this.player_settings)
  }

}
