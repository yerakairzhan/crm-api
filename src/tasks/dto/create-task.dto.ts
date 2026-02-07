import { IsString, Length } from 'class-validator';

export class CreateTaskDto {
  @IsString()
  @Length(1, 1000)
  description: string;
}
