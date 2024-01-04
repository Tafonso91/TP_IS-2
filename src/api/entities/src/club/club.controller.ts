import { Controller, Get, Post, Body, HttpStatus, HttpException, Param } from '@nestjs/common';
import { ClubService } from './club.service';

@Controller('club')
export class ClubController {
    constructor(private readonly clubService: ClubService) {}

    @Get()
    async findAll() {
        return this.clubService.findAll();
    }

    @Post(':clubName')
    async createClub(@Param('clubName') clubName: string) {
        try {
            const clubData = {
                club_name: clubName,
   
            };
            return await this.clubService.createClub(clubData);
        } catch (error) {
            throw new HttpException('Failed to create club', HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
    
}





