import { Injectable, HttpException, HttpStatus } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PlayerService {
    private prisma = new PrismaClient();

    async findAll(): Promise<any[]> {
        return this.prisma.player.findMany();
    }

    async createPlayer(playerData: { name: string }): Promise<any> {
        return this.prisma.player.create({
            data: {
                name: playerData.name,
            },
        });
    }

    }


 