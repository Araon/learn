import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { scryptSync, timingSafeEqual } from 'crypto';
import { User } from './entities/user.entity';

@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private usersRepository: Repository<User>,
  ) {}

  async findAll(): Promise<User[]> {
    return this.usersRepository.find();
  }

  async findOne(id: number): Promise<User | null> {
    return this.usersRepository.findOneBy({ id });
  }

  async findByName(name: string): Promise<User | null> {
    return this.usersRepository.findOneBy({ name });
  }

  async create(user: User): Promise<User> {
    return this.usersRepository.save(user);
  }

  async validatePassword(plain: string, hashed: string): Promise<boolean> {
    const [hash, salt] = hashed.split(':');
    const derived = scryptSync(plain, salt, 64).toString('hex');
    if (hash.length !== derived.length) return false;
    return timingSafeEqual(Buffer.from(hash), Buffer.from(derived));
  }
}
