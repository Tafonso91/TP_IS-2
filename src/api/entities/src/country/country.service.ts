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
    async getCountryByName(countryName: string): Promise<any> {
        return this.prisma.country.findFirst({
            where: {
                country_name: countryName,
            },
        });
    }
    async deleteCountryByName(countryName: string): Promise<any> {
        return this.prisma.country.deleteMany({
            where: {
                country_name: countryName,
            },
        });
    }
 



async updateCountryName(currentCountryName: string, newCountryName: string): Promise<any> {
    const country = await this.prisma.country.findFirst({
        where: {
            country_name: currentCountryName,
        },
    });

    if (!country) {
        throw new Error(`Country '${currentCountryName}' not found`);
    }

    return this.prisma.country.update({
        where: {
            id: country.id,
        },
        data: {
            country_name: newCountryName,
        },
    });
}


}