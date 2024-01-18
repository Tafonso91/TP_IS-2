import { Injectable } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class StrongFootService {
    private prisma = new PrismaClient();

    async findAll(): Promise<any[]> {
        return this.prisma.strongFoot.findMany();
    }
    async createFoot(footData: { foot_name: string }): Promise<any> {
        return this.prisma.strongFoot.create({
            data: {
                foot_name: footData.foot_name,
                
            },
        });
    }


 
    }
 











