import { Injectable } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class CountryService {
    private prisma = new PrismaClient();

    async findAll(): Promise<any[]> {
        return this.prisma.country.findMany();
    }
    async createCountry(countryData: { country_name: string }): Promise<any> {
        return this.prisma.country.create({
            data: {
                country_name: countryData.country_name,
                
            },
        });
    }
    async getCountryById(countryId: string): Promise<any> { 
        return this.prisma.country.findUnique({ where: { id: countryId } }); 
    }



}