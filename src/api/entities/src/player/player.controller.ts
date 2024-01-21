// player.controller.ts

import { Controller, Get, Post, Body, HttpStatus, HttpException } from '@nestjs/common';
import { PlayerService } from './player.service';

@Controller('player')
export class PlayerController {
    constructor(private readonly playerService: PlayerService) {}

    @Get()
    async findAll() {
        return this.playerService.findAll();
    }

    @Post()
    async createPlayer(@Body() playerData: { name: string, country_name: string, salary: string, overall: string }) {
        try {
            const createdPlayer = await this.playerService.createPlayer(playerData);
            return createdPlayer;
        } catch (error) {
            throw new HttpException('Failed to create player', HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}




    

    






