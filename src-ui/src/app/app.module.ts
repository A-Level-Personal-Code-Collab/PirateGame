import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

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
import { NicknameInputComponent } from './widgets/nickname-input/nickname-input.component';
import { GameBaseComponent } from './pages/play/game/game-base/game-base.component';
import { PlayJoinComponent } from './pages/play/play-join/play-join.component';
import { SheetBuilderComponent } from './pages/play/game/sheet-builder/sheet-builder.component';
import { MyProfileComponent } from './components/cards/my-profile/my-profile.component';
import { BaseCardComponent } from './components/cards/base-card/base-card.component';

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
    PgToggleComponent,
    NicknameInputComponent,
    GameBaseComponent,
    PlayJoinComponent,
    SheetBuilderComponent,
    MyProfileComponent,
    BaseCardComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
