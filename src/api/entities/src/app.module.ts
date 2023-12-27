import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { TeachersModule } from './teachers/teachers.module';
import { ClubModule } from './club/club.module';

@Module({
  imports: [TeachersModule, ClubModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
