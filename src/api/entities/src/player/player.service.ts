// player.service.ts

import { Injectable, HttpException, HttpStatus } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PlayerService {
    private prisma = new PrismaClient();

    async findAll(): Promise<any[]> {
        return this.prisma.player.findMany();
    }

    async createPlayer(playerData: { name: string, country_name: string, salary: string, overall: string }): Promise<any> {
        try {
            const country = await this.prisma.country.findFirst({
                where: { country_name: playerData.country_name },
            });

            if (!country) {
                throw new HttpException('Country not found', HttpStatus.NOT_FOUND);
            }

            return await this.prisma.player.create({
                data: {
                    name: playerData.name,
                    salary: playerData.salary,
                    overall: playerData.overall,
                    country: { connect: { id: country.id } },
                },
            });
        } catch (error) {
            throw new HttpException('Failed to create player', HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}





 