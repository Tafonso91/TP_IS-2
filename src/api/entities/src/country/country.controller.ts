import { Controller, Get, Post, Body, Delete, Put, HttpStatus, HttpException, Param } from '@nestjs/common';
import { CountryService } from './country.service';

@Controller('country')
export class CountryController {
    constructor(private readonly countryService: CountryService) {}

    @Get()
    async findAll() {
        return this.countryService.findAll();
    }

    @Get(':countryName')
    async getCountryByName(@Param('countryName') countryName: string) {
        try {
            const country = await this.countryService.getCountryByName(countryName);
            if (!country) {
                throw new HttpException('Country not found', HttpStatus.NOT_FOUND);
            }
            return country;
        } catch (error) {
            throw new HttpException('Failed to fetch country', HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Post(':countryName')
    async createCountry(@Param('countryName') countryName: string) {
        try {
            const countryData = {
                country_name: countryName,
   
            };
            return await this.countryService.createCountry(countryData);
        } catch (error) {
            throw new HttpException('Failed to create country', HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
    
    @Delete(':countryName')
    async deleteCountryByName(@Param('countryName') countryName: string) {
        try {
            return await this.countryService.deleteCountryByName(countryName);
        } catch (error) {
            throw new HttpException('Failed to delete country', HttpStatus.INTERNAL_SERVER_ERROR);
        }
}


    @Put(':currentCountryName')
    async updateCountryName(@Param('currentCountryName') currentCountryName: string, @Body() updateData: { newCountryName: string }) {
        try {
            return await this.countryService.updateCountryName(currentCountryName, updateData.newCountryName);
        } catch (error) {
            throw new HttpException('Failed to update country name', HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    
}





