import { Test, TestingModule } from '@nestjs/testing';
import { UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { ConfigService } from '@nestjs/config';
import * as bcrypt from 'bcrypt';
import { AuthService } from './auth.service';
import { UsersService } from '../users/users.service';
import { UserRole } from '../users/entities/user.entity';

jest.mock('bcrypt');

describe('AuthService', () => {
  let service: AuthService;
  let usersService: jest.Mocked<UsersService>;
  let jwtService: jest.Mocked<JwtService>;

  beforeEach(async () => {
    usersService = {
      create: jest.fn(),
      findByEmail: jest.fn(),
      setRefreshTokenHash: jest.fn(),
    } as unknown as jest.Mocked<UsersService>;

    jwtService = {
      sign: jest.fn(),
      verify: jest.fn(),
    } as unknown as jest.Mocked<JwtService>;

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        AuthService,
        { provide: UsersService, useValue: usersService },
        { provide: JwtService, useValue: jwtService },
        {
          provide: ConfigService,
          useValue: {
            get: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get(AuthService);
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('register returns user without password', async () => {
    usersService.create.mockResolvedValue({
      id: 'u1',
      email: 'user@test.com',
      role: 'user',
      password: 'hashed',
    } as any);

    const result = await service.register({
      email: 'user@test.com',
      password: 'password123',
      role: UserRole.USER,
    });

    expect(result).toEqual({
      id: 'u1',
      email: 'user@test.com',
      role: 'user',
    });
  });

  it('login returns token and user payload', async () => {
    const bcryptMock = bcrypt as jest.Mocked<typeof bcrypt>;
    usersService.findByEmail.mockResolvedValue({
      id: 'u1',
      email: 'user@test.com',
      role: 'user',
      password: 'hashed',
    } as any);
    bcryptMock.compare.mockResolvedValue(true as never);
    jwtService.sign.mockReturnValue('token');

    const result = await service.login({
      email: 'user@test.com',
      password: 'password123',
    });

    expect(jwtService.sign).toHaveBeenCalledWith({
      email: 'user@test.com',
      sub: 'u1',
      role: 'user',
    });
    expect(result).toEqual({
      access_token: 'token',
      refresh_token: 'token',
      user: { id: 'u1', email: 'user@test.com', role: 'user' },
    });
  });

  it('login rejects unknown email', async () => {
    usersService.findByEmail.mockResolvedValue(null);

    await expect(
      service.login({ email: 'missing@test.com', password: 'password123' }),
    ).rejects.toBeInstanceOf(UnauthorizedException);
  });

  it('login rejects invalid password', async () => {
    const bcryptMock = bcrypt as jest.Mocked<typeof bcrypt>;
    usersService.findByEmail.mockResolvedValue({
      id: 'u1',
      email: 'user@test.com',
      role: 'user',
      password: 'hashed',
    } as any);
    bcryptMock.compare.mockResolvedValue(false as never);

    await expect(
      service.login({ email: 'user@test.com', password: 'wrong' }),
    ).rejects.toBeInstanceOf(UnauthorizedException);
  });

  it('refresh issues new token pair', async () => {
    const bcryptMock = bcrypt as jest.Mocked<typeof bcrypt>;
    jwtService.verify.mockReturnValue({
      email: 'user@test.com',
      sub: 'u1',
      role: 'user',
    } as any);
    usersService.findByEmail.mockResolvedValue({
      id: 'u1',
      email: 'user@test.com',
      role: 'user',
      password: 'hashed',
      refresh_token_hash: 'rt-hash',
    } as any);
    bcryptMock.compare.mockResolvedValue(true as never);
    jwtService.sign.mockReturnValue('new-token');

    const result = await service.refresh('refresh-token');

    expect(result).toEqual({
      access_token: 'new-token',
      refresh_token: 'new-token',
    });
  });
});
