import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
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
} from '@nestjs/swagger';
import { TasksService } from './tasks.service';
import { CreateTaskDto } from './dto/create-task.dto';
import { UpdateTaskDto } from './dto/update-task.dto';
import { JwtAuthGuard } from '../common/guards/jwt-auth.guard';
import { CurrentUser } from '../common/decorators/current-user.decorator';
import { RolesGuard } from '../common/guards/roles.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { TaskResponseDto } from './dto/task-response.dto';

@Controller('tasks')
@UseGuards(JwtAuthGuard, RolesGuard)
@ApiTags('Tasks')
@ApiBearerAuth('access-token')
export class TasksController {
  constructor(private readonly tasksService: TasksService) {}

  @Post()
  @Roles('user')
  @ApiOperation({ summary: 'Create task (role: user only)' })
  @ApiCreatedResponse({
    description: 'Task created successfully',
    type: TaskResponseDto,
  })
  @ApiBadRequestResponse({ description: 'Validation failed' })
  @ApiUnauthorizedResponse({ description: 'Missing or invalid access token' })
  @ApiForbiddenResponse({ description: 'Insufficient role' })
  create(@Body() createTaskDto: CreateTaskDto, @CurrentUser() user: any) {
    return this.tasksService.create(createTaskDto, user.userId);
  }

  @Get()
  @ApiOperation({ summary: 'Get all tasks (newest first)' })
  @ApiOkResponse({ description: 'List of tasks', type: TaskResponseDto, isArray: true })
  @ApiUnauthorizedResponse({ description: 'Missing or invalid access token' })
  findAll() {
    return this.tasksService.findAll();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get task by id' })
  @ApiOkResponse({ description: 'Task details', type: TaskResponseDto })
  @ApiUnauthorizedResponse({ description: 'Missing or invalid access token' })
  @ApiNotFoundResponse({ description: 'Task not found' })
  findOne(@Param('id') id: string) {
    return this.tasksService.findOne(id);
  }

  @Patch(':id')
  @ApiOperation({ summary: 'Update task (owner only)' })
  @ApiOkResponse({ description: 'Task updated successfully', type: TaskResponseDto })
  @ApiBadRequestResponse({ description: 'Validation failed' })
  @ApiUnauthorizedResponse({ description: 'Missing or invalid access token' })
  @ApiForbiddenResponse({ description: 'Not the task owner' })
  @ApiNotFoundResponse({ description: 'Task not found' })
  update(
    @Param('id') id: string,
    @Body() updateTaskDto: UpdateTaskDto,
    @CurrentUser() user: any,
  ) {
    return this.tasksService.update(id, updateTaskDto, user.userId);
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Delete task (owner only)' })
  @ApiNoContentResponse({ description: 'Task deleted successfully' })
  @ApiUnauthorizedResponse({ description: 'Missing or invalid access token' })
  @ApiForbiddenResponse({ description: 'Not the task owner' })
  @ApiNotFoundResponse({ description: 'Task not found' })
  remove(@Param('id') id: string, @CurrentUser() user: any) {
    return this.tasksService.remove(id, user.userId);
  }
}
