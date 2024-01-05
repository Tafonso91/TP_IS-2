import { Controller, Get, Post, Body, Delete, Put, HttpStatus, HttpException, Param } from '@nestjs/common';
import { PlayerService } from './player.service';

@Controller('player')
export class PlayerController {
    constructor(private readonly playerService: PlayerService) {}

    @Get()
    async findAll() {
        return this.playerService.findAll();
    }



    @Post(':playerName')
    async createPlayer(@Param('playerName') playerName: string) {
        try {
            const playerData = {
                player_name: playerName, // Corrigido para 'player_name' em vez de 'name'
            };
            return await this.playerService.createPlayer(playerData);
        } catch (error) {
            throw new HttpException('Failed to create player', HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
    
    @Delete(':playerId')
    async deletePlayerById(@Param('playerId') playerId: string) {
        try {
            return await this.playerService.deletePlayerById(playerId);
        } catch (error) {
            throw new HttpException('Failed to delete player', HttpStatus.INTERNAL_SERVER_ERROR);
        }
}




    
}





