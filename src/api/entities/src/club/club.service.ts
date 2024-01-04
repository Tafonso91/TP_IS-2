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
    async getClubByName(clubName: string): Promise<any> {
        return this.prisma.club.findFirst({
            where: {
                club_name: clubName,
            },
        });
    }
    async deleteClubByName(clubName: string): Promise<any> {
        return this.prisma.club.deleteMany({
            where: {
                club_name: clubName,
            },
        });
    }
 



async updateClubName(currentClubName: string, newClubName: string): Promise<any> {
    const club = await this.prisma.club.findFirst({
        where: {
            club_name: currentClubName,
        },
    });

    if (!club) {
        throw new Error(`Club '${currentClubName}' not found`);
    }

    return this.prisma.club.update({
        where: {
            id: club.id,
        },
        data: {
            club_name: newClubName,
        },
    });
}


}




