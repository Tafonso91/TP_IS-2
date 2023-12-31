import { Injectable } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PlayerService {
    private prisma = new PrismaClient();

    async findAll(): Promise<any[]> {
        return this.prisma.player.findMany();
    }
    }
 