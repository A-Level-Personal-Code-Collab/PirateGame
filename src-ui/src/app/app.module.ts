import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

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
import { PlayStartComponent } from './pages/play/play-start/play-start.component';
import { PlayCreateComponent } from './pages/play/play-create/play-create.component';
import { PgToggleComponent } from './widgets/pg-toggle/pg-toggle.component';

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
    PlayStartComponent,
    PlayCreateComponent,
    PgToggleComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
