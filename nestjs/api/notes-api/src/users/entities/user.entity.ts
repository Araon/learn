import { Entity, Column, PrimaryGeneratedColumn, BeforeInsert } from 'typeorm';
import { scryptSync, randomBytes } from 'crypto';

@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @Column()
  password: string;

  @BeforeInsert()
  hashPassword() {
    const salt = randomBytes(16).toString('hex');
    this.password = scryptSync(this.password, salt, 64).toString('hex') + ':' + salt;
  }
}
