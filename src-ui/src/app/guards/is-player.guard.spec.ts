import { TestBed } from '@angular/core/testing';

import { IsPlayerGuard } from './is-player.guard';

describe('IsPlayerGuard', () => {
  let guard: IsPlayerGuard;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    guard = TestBed.inject(IsPlayerGuard);
  });

  it('should be created', () => {
    expect(guard).toBeTruthy();
  });
});
