import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
  Query,
  UseGuards,
} from '@nestjs/common';
import {
  ApiTags,
  ApiBearerAuth,
  ApiOperation,
  ApiCreatedResponse,
  ApiOkResponse,
  ApiNoContentResponse,
  ApiUnauthorizedResponse,
  ApiForbiddenResponse,
  ApiNotFoundResponse,
  ApiBadRequestResponse,
  ApiQuery,
} from '@nestjs/swagger';
import { CommentsService } from './comments.service';
import { CreateCommentDto } from './dto/create-comment.dto';
import { UpdateCommentDto } from './dto/update-comment.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { CurrentUser } from '../common/decorators/current-user.decorator';
import { CommentResponseDto } from './dto/comment-response.dto';

@Controller('comments')
@UseGuards(JwtAuthGuard, RolesGuard)
@ApiTags('Comments')
@ApiBearerAuth('access-token')
export class CommentsController {
  constructor(private readonly commentsService: CommentsService) {}

  // Only users with role 'author' can create comments
  @Post()
  @Roles('author')
  @ApiOperation({ summary: 'Create comment (role: author only)' })
  @ApiCreatedResponse({
    description: 'Comment created successfully',
    type: CommentResponseDto,
  })
  @ApiBadRequestResponse({ description: 'Validation failed' })
  @ApiUnauthorizedResponse({ description: 'Missing or invalid access token' })
  @ApiForbiddenResponse({ description: 'Insufficient role' })
  create(@Body() createCommentDto: CreateCommentDto, @CurrentUser() user: any) {
    return this.commentsService.create(createCommentDto, user.userId);
  }

  @Get()
  @ApiOperation({ summary: 'Get comments (optionally filtered by task_id)' })
  @ApiQuery({
    name: 'task_id',
    required: false,
    description: 'Filter comments by task UUID',
    example: '487f3b13-2f77-470f-9fcb-bf8b4398f2a9',
  })
  @ApiOkResponse({
    description: 'List of comments',
    type: CommentResponseDto,
    isArray: true,
  })
  @ApiUnauthorizedResponse({ description: 'Missing or invalid access token' })
  findAll(@Query('task_id') taskId?: string) {
    return this.commentsService.findAll(taskId);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get comment by id' })
  @ApiOkResponse({ description: 'Comment details', type: CommentResponseDto })
  @ApiUnauthorizedResponse({ description: 'Missing or invalid access token' })
  @ApiNotFoundResponse({ description: 'Comment not found' })
  findOne(@Param('id') id: string) {
    return this.commentsService.findOne(id);
  }

  @Patch(':id')
  @ApiOperation({ summary: 'Update comment (owner only)' })
  @ApiOkResponse({
    description: 'Comment updated successfully',
    type: CommentResponseDto,
  })
  @ApiBadRequestResponse({ description: 'Validation failed' })
  @ApiUnauthorizedResponse({ description: 'Missing or invalid access token' })
  @ApiForbiddenResponse({ description: 'Not the comment owner' })
  @ApiNotFoundResponse({ description: 'Comment not found' })
  update(
    @Param('id') id: string,
    @Body() updateCommentDto: UpdateCommentDto,
    @CurrentUser() user: any,
  ) {
    return this.commentsService.update(id, updateCommentDto, user.userId);
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Delete comment (owner only)' })
  @ApiNoContentResponse({ description: 'Comment deleted successfully' })
  @ApiUnauthorizedResponse({ description: 'Missing or invalid access token' })
  @ApiForbiddenResponse({ description: 'Not the comment owner' })
  @ApiNotFoundResponse({ description: 'Comment not found' })
  remove(@Param('id') id: string, @CurrentUser() user: any) {
    return this.commentsService.remove(id, user.userId);
  }
}
