import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { ForbiddenException, NotFoundException } from '@nestjs/common';
import { ObjectLiteral, Repository } from 'typeorm';
import { TasksService } from './tasks.service';
import { Task } from './entities/task.entity';
import { UsersService } from '../users/users.service';

type MockRepo<T extends ObjectLiteral> = Partial<
  Record<keyof Repository<T>, jest.Mock>
>;

describe('TasksService', () => {
  let service: TasksService;
  let tasksRepo: MockRepo<Task>;
  let usersService: jest.Mocked<UsersService>;

  beforeEach(async () => {
    tasksRepo = {
      create: jest.fn(),
      save: jest.fn(),
      find: jest.fn(),
      findOne: jest.fn(),
      remove: jest.fn(),
    };
    usersService = {
      setTaskId: jest.fn(),
    } as unknown as jest.Mocked<UsersService>;

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        TasksService,
        { provide: getRepositoryToken(Task), useValue: tasksRepo },
        { provide: UsersService, useValue: usersService },
      ],
    }).compile();

    service = module.get(TasksService);
  });

  it('creates a task with user_id', async () => {
    tasksRepo.create!.mockReturnValue({ id: 't1' });
    tasksRepo.save!.mockResolvedValue({ id: 't1', user_id: 'u1' });

    const result = await service.create(
      { description: 'task', comment: 'note' },
      'u1',
    );

    expect(tasksRepo.create).toHaveBeenCalledWith({
      description: 'task',
      comment: 'note',
      user_id: 'u1',
    });
    expect(usersService.setTaskId).toHaveBeenCalledWith('u1', 't1');
    expect(result.user_id).toBe('u1');
  });

  it('findAll uses DESC ordering and user relation', async () => {
    tasksRepo.find!.mockResolvedValue([]);

    await service.findAll();

    expect(tasksRepo.find).toHaveBeenCalledWith({
      order: { created_at: 'DESC' },
      relations: ['user'],
    });
  });

  it('findOne throws when not found', async () => {
    tasksRepo.findOne!.mockResolvedValue(null);

    await expect(service.findOne('missing')).rejects.toBeInstanceOf(
      NotFoundException,
    );
  });

  it('update rejects non-owner', async () => {
    tasksRepo.findOne!.mockResolvedValue({ id: 't1', user_id: 'u1' });

    await expect(
      service.update('t1', { description: 'x' }, 'u2'),
    ).rejects.toBeInstanceOf(ForbiddenException);
  });

  it('remove rejects non-owner', async () => {
    tasksRepo.findOne!.mockResolvedValue({ id: 't1', user_id: 'u1' });

    await expect(service.remove('t1', 'u2')).rejects.toBeInstanceOf(
      ForbiddenException,
    );
  });
});
