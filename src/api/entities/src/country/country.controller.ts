import { Controller, Get, Post, Body, Delete, Put, HttpStatus, HttpException, Param } from '@nestjs/common';
import { CountryService } from './country.service';

@Controller('country')
export class CountryController {
    constructor(private readonly countryService: CountryService) {}

    @Get()
    async findAll() {
        return this.countryService.findAll();
    }

    @Get(':countryId')
    async getCountryById(@Param('countryId') countryId: string) { 
        try {
            const country = await this.countryService.getCountryById(countryId); 
            if (!country) {
                throw new HttpException('Country not found', HttpStatus.NOT_FOUND);
            }
            return country;
        } catch (error) {
            throw new HttpException('Failed to fetch country', HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Post() 
    async createCountry(@Body() countryData: { country_name: string }) { 
        try {
            return await this.countryService.createCountry(countryData);
        } catch (error) {
            throw new HttpException('Failed to create country', HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

}


