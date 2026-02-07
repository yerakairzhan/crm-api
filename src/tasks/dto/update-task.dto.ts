import { IsString, Length, IsOptional } from 'class-validator';

export class UpdateTaskDto {
  @IsString()
  @Length(1, 1000)
  @IsOptional()
  description?: string;
}
