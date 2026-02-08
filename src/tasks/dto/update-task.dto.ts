import { IsString, Length, IsOptional } from 'class-validator';
import { ApiPropertyOptional } from '@nestjs/swagger';

export class UpdateTaskDto {
  @ApiPropertyOptional({
    example: 'Updated task description',
    minLength: 1,
    maxLength: 1000,
  })
  @IsString()
  @Length(1, 1000)
  @IsOptional()
  description?: string;

  @ApiPropertyOptional({
    example: 'Updated comment for task',
    minLength: 1,
    maxLength: 1000,
  })
  @IsString()
  @Length(1, 1000)
  @IsOptional()
  comment?: string;
}
