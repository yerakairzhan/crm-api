import { ApiProperty } from '@nestjs/swagger';

export class TaskResponseDto {
  @ApiProperty({
    example: '487f3b13-2f77-470f-9fcb-bf8b4398f2a9',
    format: 'uuid',
  })
  id: string;

  @ApiProperty({
    example: '7f8f5e31-e7d9-4d5d-b367-c8a2cb3a9df7',
    format: 'uuid',
  })
  user_id: string;

  @ApiProperty({ example: 'Prepare CRM onboarding plan' })
  description: string;

  @ApiProperty({ example: 'Priority: high. Draft by Friday.' })
  comment: string;

  @ApiProperty({ example: '2026-01-01T12:00:00.000Z' })
  created_at: Date;

  @ApiProperty({ example: '2026-01-01T12:00:00.000Z' })
  updated_at: Date;
}

