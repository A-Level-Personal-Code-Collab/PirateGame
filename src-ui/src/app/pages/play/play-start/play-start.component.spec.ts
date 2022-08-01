import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayStartComponent } from './play-start.component';

describe('PlayStartComponent', () => {
  let component: PlayStartComponent;
  let fixture: ComponentFixture<PlayStartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PlayStartComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PlayStartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
