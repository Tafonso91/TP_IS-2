import { Controller, Get, Post, Body, Delete, Put, HttpStatus, HttpException, Param } from '@nestjs/common';
import { StrongFootService } from './strongfoot.service';

@Controller('strong_foot')
export class StrongFootController {
    constructor(private readonly strong_footService: StrongFootService) {}

    @Get()
    async findAll() {
        return this.strong_footService.findAll();
    }




    

    
}





