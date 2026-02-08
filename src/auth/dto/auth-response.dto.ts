import { ApiProperty } from '@nestjs/swagger';
import { UserRole } from '../../users/entities/user.entity';
import { UserResponseDto } from '../../users/dto/user-response.dto';

export class LoginUserDto {
  @ApiProperty({
    example: 'f8f1a41b-255a-4e8f-bdf4-1d855d8d8f7c',
    format: 'uuid',
  })
  id: string;

  @ApiProperty({ example: 'user@example.com' })
  email: string;

  @ApiProperty({ enum: UserRole, example: UserRole.USER })
  role: UserRole;
}

export class LoginResponseDto {
  @ApiProperty({ example: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...' })
  access_token: string;

  @ApiProperty({ example: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...' })
  refresh_token: string;

  @ApiProperty({ type: LoginUserDto })
  user: LoginUserDto;
}

export class RefreshResponseDto {
  @ApiProperty({ example: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...' })
  access_token: string;

  @ApiProperty({ example: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...' })
  refresh_token: string;
}

export class RegisterResponseDto extends UserResponseDto {}

