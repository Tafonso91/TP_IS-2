import { Controller, Get, Post, Body, Delete, Put, HttpStatus, HttpException, Param } from '@nestjs/common';
import { ClubService } from './club.service';

@Controller('club')
export class ClubController {
    constructor(private readonly clubService: ClubService) {}

    @Get()
    async findAll() {
        return this.clubService.findAll();
    }

    @Get(':clubName')
    async getClubByName(@Param('clubName') clubName: string) {
        try {
            const club = await this.clubService.getClubByName(clubName);
            if (!club) {
                throw new HttpException('Club not found', HttpStatus.NOT_FOUND);
            }
            return club;
        } catch (error) {
            throw new HttpException('Failed to fetch club', HttpStatus.INTERNAL_SERVER_ERROR);
        }
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
    
    @Delete(':clubName')
    async deleteClubByName(@Param('clubName') clubName: string) {
        try {
            return await this.clubService.deleteClubByName(clubName);
        } catch (error) {
            throw new HttpException('Failed to delete club', HttpStatus.INTERNAL_SERVER_ERROR);
        }
}


    @Put(':currentClubName')
    async updateClubName(@Param('currentClubName') currentClubName: string, @Body() updateData: { newClubName: string }) {
        try {
            return await this.clubService.updateClubName(currentClubName, updateData.newClubName);
        } catch (error) {
            throw new HttpException('Failed to update club name', HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    
}





