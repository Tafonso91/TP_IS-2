import { Test, TestingModule } from '@nestjs/testing';
import { StrongFootController } from './strongfoot.controller';

describe('StrongFootController', () => {
  let controller: StrongFootController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [StrongFootController],
    }).compile();

    controller = module.get<StrongFootController>(StrongFootController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
