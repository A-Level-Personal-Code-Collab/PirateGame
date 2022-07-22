import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PatchPageComponent } from './patch-page.component';

describe('PatchPageComponent', () => {
  let component: PatchPageComponent;
  let fixture: ComponentFixture<PatchPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PatchPageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PatchPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
