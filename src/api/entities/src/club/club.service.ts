import { Injectable } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class ClubService {
    private prisma = new PrismaClient();

    async findAll(): Promise<any[]> {
        return this.prisma.club.findMany();
    }
    async createClub(clubData: { club_name: string }): Promise<any> {
        return this.prisma.club.create({
            data: {
                club_name: clubData.club_name,
                
            },
        });
    }
    async getClubById(clubId: string): Promise<any> { 
        return this.prisma.club.findUnique({ where: { id: clubId } }); 
    }



}




