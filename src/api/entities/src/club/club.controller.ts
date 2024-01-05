import { Controller, Get, Post, Body, Delete, Put, HttpStatus, HttpException, Param } from '@nestjs/common';
import { ClubService } from './club.service';

@Controller('club')
export class ClubController {
    constructor(private readonly clubService: ClubService) {}

    @Get()
    async findAll() {
        return this.clubService.findAll();
    }

    @Get(':clubId')
    async getClubById(@Param('clubId') clubId: string) { 
        try {
            const club = await this.clubService.getClubById(clubId); 
            if (!club) {
                throw new HttpException('Club not found', HttpStatus.NOT_FOUND);
            }
            return club;
        } catch (error) {
            throw new HttpException('Failed to fetch club', HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Post() 
    async createClub(@Body() clubData: { club_name: string }) { 
        try {
            return await this.clubService.createClub(clubData);
        } catch (error) {
            throw new HttpException('Failed to create club', HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
    


    
}





