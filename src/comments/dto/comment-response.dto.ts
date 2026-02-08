import { ApiProperty } from '@nestjs/swagger';

export class CommentResponseDto {
  @ApiProperty({
    example: '975f98db-fffb-4774-860f-8d7f3ec0ea3a',
    format: 'uuid',
  })
  id: string;

  @ApiProperty({
    example: '487f3b13-2f77-470f-9fcb-bf8b4398f2a9',
    format: 'uuid',
  })
  task_id: string;

  @ApiProperty({
    example: 'd565f17b-36a0-47f9-b1c3-f53c73d9d384',
    format: 'uuid',
  })
  user_id: string;

  @ApiProperty({ example: 'Looks good, please update the due date.' })
  text: string;

  @ApiProperty({ example: '2026-01-01T12:00:00.000Z' })
  created_at: Date;

  @ApiProperty({ example: '2026-01-01T12:00:00.000Z' })
  updated_at: Date;
}

