import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { ForbiddenException, NotFoundException } from '@nestjs/common';
import { ObjectLiteral, Repository } from 'typeorm';
import { CommentsService } from './comments.service';
import { Comment } from './entities/comment.entity';

type MockRepo<T extends ObjectLiteral> = Partial<
  Record<keyof Repository<T>, jest.Mock>
>;

describe('CommentsService', () => {
  let service: CommentsService;
  let commentsRepo: MockRepo<Comment>;

  beforeEach(async () => {
    commentsRepo = {
      create: jest.fn(),
      save: jest.fn(),
      find: jest.fn(),
      findOne: jest.fn(),
      remove: jest.fn(),
    };

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        CommentsService,
        { provide: getRepositoryToken(Comment), useValue: commentsRepo },
      ],
    }).compile();

    service = module.get(CommentsService);
  });

  it('creates a comment with user_id', async () => {
    commentsRepo.create!.mockReturnValue({ id: 'c1' });
    commentsRepo.save!.mockResolvedValue({ id: 'c1', user_id: 'u1' });

    const result = await service.create(
      { text: 'comment', task_id: 't1' },
      'u1',
    );

    expect(commentsRepo.create).toHaveBeenCalledWith({
      text: 'comment',
      task_id: 't1',
      user_id: 'u1',
    });
    expect(result.user_id).toBe('u1');
  });

  it('findAll with taskId filters and loads relations', async () => {
    commentsRepo.find!.mockResolvedValue([]);

    await service.findAll('t1');

    expect(commentsRepo.find).toHaveBeenCalledWith({
      where: { task_id: 't1' },
      order: { created_at: 'DESC' },
      relations: ['user', 'task'],
    });
  });

  it('findOne throws when not found', async () => {
    commentsRepo.findOne!.mockResolvedValue(null);

    await expect(service.findOne('missing')).rejects.toBeInstanceOf(
      NotFoundException,
    );
  });

  it('update rejects non-owner', async () => {
    commentsRepo.findOne!.mockResolvedValue({ id: 'c1', user_id: 'u1' });

    await expect(
      service.update('c1', { text: 'x' }, 'u2'),
    ).rejects.toBeInstanceOf(ForbiddenException);
  });

  it('remove rejects non-owner', async () => {
    commentsRepo.findOne!.mockResolvedValue({ id: 'c1', user_id: 'u1' });

    await expect(service.remove('c1', 'u2')).rejects.toBeInstanceOf(
      ForbiddenException,
    );
  });
});
