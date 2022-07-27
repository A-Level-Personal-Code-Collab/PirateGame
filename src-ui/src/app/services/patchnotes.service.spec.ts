import { TestBed } from '@angular/core/testing';

import { PatchnotesService } from './patchnotes.service';

describe('PatchnotesService', () => {
  let service: PatchnotesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PatchnotesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
