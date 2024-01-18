import { Controller, Get, Post, Body, Delete, Put, HttpStatus, HttpException, Param } from '@nestjs/common';
import { PlayerService } from './player.service';

@Controller('player')
export class PlayerController {
    constructor(private readonly playerService: PlayerService) {}

    @Get()
    async findAll() {
        return this.playerService.findAll();
    }
    @Post()
    async createPlayer(@Body() playerData: { name: string}) {
        try {
            return await this.playerService.createPlayer(playerData);
        } catch (error) {
            throw new HttpException('Failed to create player', HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }



    

    
}





