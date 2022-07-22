import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AboutComponent } from './pages/facade/about-page/about.component';
import { IndexComponent } from './pages/facade/index-page/index.component';
import { PatchPageComponent } from './pages/facade/patch-page/patch-page.component';
import { TutorialPageComponent } from './pages/facade/tutorial-page/tutorial-page.component';

const routes: Routes = [
  {path: "", component: IndexComponent},
  {path: "about", component: AboutComponent},
  {path: "tutorial", component: TutorialPageComponent},
  {path: "patch_notes", component: PatchPageComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
