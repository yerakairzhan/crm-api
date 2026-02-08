import { IsString, Length, IsUUID } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class CreateCommentDto {
  @ApiProperty({
    example: 'Please update acceptance criteria and estimate.',
    minLength: 1,
    maxLength: 1000,
  })
  @IsString()
  @Length(1, 1000)
  text: string;

  @ApiProperty({
    example: '487f3b13-2f77-470f-9fcb-bf8b4398f2a9',
    format: 'uuid',
  })
  @IsUUID()
  task_id: string;
}
