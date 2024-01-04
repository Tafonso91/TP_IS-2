import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';

import { ClubModule } from './club/club.module';
import { CountryModule } from './country/country.module';

@Module({
  imports: [ClubModule, CountryModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
