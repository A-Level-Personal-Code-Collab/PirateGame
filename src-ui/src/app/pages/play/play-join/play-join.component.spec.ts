import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayJoinComponent } from './play-join.component';

describe('PlayJoinComponent', () => {
  let component: PlayJoinComponent;
  let fixture: ComponentFixture<PlayJoinComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PlayJoinComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PlayJoinComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
