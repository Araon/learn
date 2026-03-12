import { Injectable } from '@nestjs/common';
import { CreateNoteDto } from './dto/create-note.dto';
import { UpdateNoteDto } from './dto/update-note.dto';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Note } from './entities/note.entity';

@Injectable()
export class NotesService {
  constructor(
    @InjectRepository(Note)
    private notesRepository: Repository<Note>,
  ) {}
  async create(createNoteDto: CreateNoteDto): Promise<Note> {
    const note = this.notesRepository.create({
      ...createNoteDto,
      tags: createNoteDto.tags
        ? createNoteDto.tags.split(',').map((t) => t.trim())
        : [],
    });
    return this.notesRepository.save(note);
  }

  async findAll(): Promise<Note[]> {
    return this.notesRepository.find();
  }

  async findOne(id: number): Promise<Note | null> {
    return this.notesRepository.findOneBy({ id });
  }

  async findByTag(tag: string): Promise<Note[]> {
    return this.notesRepository
      .createQueryBuilder('note')
      .where('note.tags LIKE :tag', { tag: `%${tag}%` })
      .getMany();
  }

  async update(id: number, updateNoteDto: UpdateNoteDto): Promise<Note | null> {
    const note = await this.notesRepository.findOneBy({ id });
    if (!note) return null;

    Object.assign(note, updateNoteDto);
    return this.notesRepository.save(note);
  }

  async remove(id: number): Promise<void> {
    await this.notesRepository.delete(id);
  }
}
