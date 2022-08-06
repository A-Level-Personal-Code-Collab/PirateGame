import { NgModule } from '@angular/core';
import { RouterModule, Routes, ExtraOptions } from '@angular/router';
import { AboutComponent } from './pages/facade/about-page/about.component';
import { IndexComponent } from './pages/facade/index-page/index.component';
import { PatchPageComponent } from './pages/facade/patch-page/patch-page.component';
import { TutorialPageComponent } from './pages/facade/tutorial-page/tutorial-page.component';
import { PlayStartComponent } from './pages/play/play-start/play-start.component';
import { PlayCreateComponent } from './pages/play/play-create/play-create.component';
import { GameBaseComponent } from './pages/play/game/game-base/game-base.component';
import { SheetBuilderComponent } from './pages/play/game/sheet-builder/sheet-builder.component';
import { PlayJoinComponent } from './pages/play/play-join/play-join.component';
import { IsPlayerGuard } from './guards/is-player.guard';

// Extra options to allow scrolling to specific fragment
const routerOptions: ExtraOptions = {
  scrollPositionRestoration: 'enabled',
  anchorScrolling: 'enabled',
  scrollOffset: [0, 48],
};

const routes: Routes = [
  {path: "", component: IndexComponent},
  {path: "play", component: PlayStartComponent},
  {path: "play/create", component: PlayCreateComponent},
  {path: "play/join", component: PlayJoinComponent},
  {path: "about", component: AboutComponent},
  {path: "tutorial", component: TutorialPageComponent},
  {path: "patch_notes", component: PatchPageComponent},
  {
    path: 'play/game',
    component: GameBaseComponent,
    canActivate: [IsPlayerGuard],
    children: [
      {
        path: 'builder', // child route path
        component: SheetBuilderComponent, // child route component that the router renders
      },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, routerOptions)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
