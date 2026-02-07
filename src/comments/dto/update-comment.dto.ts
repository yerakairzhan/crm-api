import { IsString, Length, IsOptional } from 'class-validator';

export class UpdateCommentDto {
  @IsString()
  @Length(1, 1000)
  @IsOptional()
  text?: string;
}
