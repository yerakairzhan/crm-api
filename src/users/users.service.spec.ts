import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { ConflictException, NotFoundException } from '@nestjs/common';
import * as bcrypt from 'bcrypt';
import { ObjectLiteral, Repository } from 'typeorm';
import { UsersService } from './users.service';
import { User } from './entities/user.entity';
import { UserRole } from './entities/user.entity';

jest.mock('bcrypt');

type MockRepo<T extends ObjectLiteral> = Partial<
  Record<keyof Repository<T>, jest.Mock>
>;

describe('UsersService', () => {
  let service: UsersService;
  let usersRepo: MockRepo<User>;

  beforeEach(async () => {
    usersRepo = {
      findOne: jest.fn(),
      create: jest.fn(),
      save: jest.fn(),
      delete: jest.fn(),
    };

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UsersService,
        { provide: getRepositoryToken(User), useValue: usersRepo },
      ],
    }).compile();

    service = module.get(UsersService);
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('creates a user with hashed password', async () => {
    const createDto = {
      email: 'user@test.com',
      password: 'password123',
      role: UserRole.USER,
    };

    const bcryptMock = bcrypt as jest.Mocked<typeof bcrypt>;
    usersRepo.findOne!.mockResolvedValue(null);
    bcryptMock.hash.mockResolvedValue('hashed' as never);
    usersRepo.create!.mockReturnValue({
      id: 'u1',
      ...createDto,
      password: 'hashed',
    });
    usersRepo.save!.mockResolvedValue({
      id: 'u1',
      ...createDto,
      password: 'hashed',
    });

    const result = await service.create(createDto);

    expect(usersRepo.findOne).toHaveBeenCalledWith({
      where: { email: 'user@test.com' },
    });
    expect(usersRepo.save).toHaveBeenCalled();
    expect(result.password).toBe('hashed');
  });

  it('rejects duplicate email on create', async () => {
    usersRepo.findOne!.mockResolvedValue({ id: 'existing' });

    await expect(
      service.create({
        email: 'user@test.com',
        password: 'password123',
        role: UserRole.USER,
      }),
    ).rejects.toBeInstanceOf(ConflictException);
  });

  it('findOne throws when user does not exist', async () => {
    usersRepo.findOne!.mockResolvedValue(null);

    await expect(service.findOne('missing')).rejects.toBeInstanceOf(
      NotFoundException,
    );
  });

  it('updates a user and hashes password if provided', async () => {
    const bcryptMock = bcrypt as jest.Mocked<typeof bcrypt>;
    usersRepo.findOne!.mockResolvedValue({
      id: 'u1',
      email: 'user@test.com',
      password: 'old',
    });
    bcryptMock.hash.mockResolvedValue('new-hash' as never);
    usersRepo.save!.mockResolvedValue({
      id: 'u1',
      email: 'user@test.com',
      password: 'new-hash',
    });

    const result = await service.update('u1', { password: 'newpass' });

    expect(result.password).toBe('new-hash');
  });

  it('remove throws when user does not exist', async () => {
    usersRepo.delete!.mockResolvedValue({ affected: 0 });

    await expect(service.remove('missing')).rejects.toBeInstanceOf(
      NotFoundException,
    );
  });
});
