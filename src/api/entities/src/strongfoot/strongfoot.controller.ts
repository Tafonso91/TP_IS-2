import { Controller, Get, Post, Body, Delete, Put, HttpStatus, HttpException, Param } from '@nestjs/common';
import { StrongFootService } from './strongfoot.service';

@Controller('strong_foot')
export class StrongFootController {
    constructor(private readonly strong_footService: StrongFootService) {}

    @Get()
    async findAll() {
        return this.strong_footService.findAll();
    }
    @Post() 
    async createFoot(@Body() footData: { foot_name: string }) { 
        try {
            return await this.strong_footService.createFoot(footData);
        } catch (error) {
            throw new HttpException('Failed to create foot', HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}



    

    






