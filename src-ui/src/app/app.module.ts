import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './components/global/header/header.component';
import { FooterComponent } from './components/global/footer/footer.component';
import { IndexComponent } from './pages/facade/index-page/index.component';
import { NewsComponent } from './components/facade/news/news.component';
import { SocialComponent } from './components/facade/social/social.component';
import { AboutComponent } from './pages/facade/about-page/about.component';
import { TutorialComponent } from './components/facade/tutorial/tutorial.component';
import { BannerComponent } from './components/global/banner/banner.component';
import { TutorialPageComponent } from './pages/facade/tutorial-page/tutorial-page.component';
import { PatchPageComponent } from './pages/facade/patch-page/patch-page.component';
import { PlayStartComponent } from './pages/play-start/play-start.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    IndexComponent,
    NewsComponent,
    SocialComponent,
    AboutComponent,
    TutorialComponent,
    BannerComponent,
    TutorialPageComponent,
    PatchPageComponent,
    PlayStartComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
