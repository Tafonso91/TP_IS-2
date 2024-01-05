import { Module } from '@nestjs/common';
import { StrongFootService } from './strongfoot.service';
import { StrongFootController } from './strongfoot.controller';

@Module({
    providers: [StrongFootService],
    controllers: [StrongFootController]
})
export class StrongFootModule {}




