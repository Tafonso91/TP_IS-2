import { Test, TestingModule } from '@nestjs/testing';
import { StrongFootService } from './strongfoot.service';

describe('StrongFootService', () => {
  let service: StrongFootService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [StrongFootService],
    }).compile();

    service = module.get<StrongFootService>(StrongFootService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
