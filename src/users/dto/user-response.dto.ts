import { ApiProperty } from '@nestjs/swagger';
import { UserRole } from '../entities/user.entity';

export class UserResponseDto {
  @ApiProperty({
    example: '3d4d4a4d-2f5e-49db-b5ea-8ac8abecf13f',
    format: 'uuid',
  })
  id: string;

  @ApiProperty({ example: 'user@example.com' })
  email: string;

  @ApiProperty({ enum: UserRole, example: UserRole.USER })
  role: UserRole;

  @ApiProperty({
    example: '2a8f2859-9f6e-45e8-b5ea-9dc9bc8f4691',
    format: 'uuid',
    required: false,
    nullable: true,
  })
  task_id?: string | null;

  @ApiProperty({ example: '2026-01-01T12:00:00.000Z' })
  created_at: Date;

  @ApiProperty({ example: '2026-01-01T12:00:00.000Z' })
  updated_at: Date;
}

