import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ClubModule } from './club/club.module';
import { CountryModule } from './country/country.module';
import { PlayerModule } from './player/player.module';
import { StrongFootModule } from './strongfoot/strongfoot.module';

@Module({
  imports: [ClubModule, CountryModule, PlayerModule, StrongFootModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
