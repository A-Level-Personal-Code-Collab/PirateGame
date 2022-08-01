import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PgToggleComponent } from './pg-toggle.component';

describe('PgToggleComponent', () => {
  let component: PgToggleComponent;
  let fixture: ComponentFixture<PgToggleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PgToggleComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PgToggleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
