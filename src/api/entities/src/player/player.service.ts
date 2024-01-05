import { Injectable } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PlayerService {
    private prisma = new PrismaClient();

    async findAll(): Promise<any[]> {
        return this.prisma.player.findMany();
    }
    async createPlayer(playerData: { player_name: string }): Promise<any> {
        return this.prisma.player.create({
            data: {
                name: playerData.player_name,
                height: 0, 
                price: '', 
                salary: '', 
                
                club: { connect: { id: 'default-club-id' } }, 
                country: { connect: { id: 'default-country-id' } }, 
                foot: { connect: { id: 'default-foot-id' } }, 
                
            },
        });
    }

 
    }
 











