import { Injectable } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class ClubService {
    private prisma = new PrismaClient();

    async findAll(): Promise<any[]> {
        return this.prisma.club.findMany();
    }
}




