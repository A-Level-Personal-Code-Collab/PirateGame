import { NgModule } from '@angular/core';
import { RouterModule, Routes, ExtraOptions } from '@angular/router';
import { AboutComponent } from './pages/facade/about-page/about.component';
import { IndexComponent } from './pages/facade/index-page/index.component';
import { PatchPageComponent } from './pages/facade/patch-page/patch-page.component';
import { TutorialPageComponent } from './pages/facade/tutorial-page/tutorial-page.component';
import { PlayStartComponent } from './pages/play/play-start/play-start.component';
import { PlayCreateComponent } from './pages/play/play-create/play-create.component';

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
  {path: "about", component: AboutComponent},
  {path: "tutorial", component: TutorialPageComponent},
  {path: "patch_notes", component: PatchPageComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes, routerOptions)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
