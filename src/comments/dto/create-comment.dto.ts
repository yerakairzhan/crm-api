import { IsString, Length, IsUUID } from 'class-validator';

export class CreateCommentDto {
  @IsString()
  @Length(1, 1000)
  text: string;

  @IsUUID()
  task_id: string;
}
