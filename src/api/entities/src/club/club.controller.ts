import { Controller, Get } from '@nestjs/common';
import { ClubService } from './club.service';

@Controller('club')
export class ClubController {
constructor(private readonly clubService: ClubService) {}

@Get()
    async findAll() {
        return this.clubService.findAll();
    }
}




