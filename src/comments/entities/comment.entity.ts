import { Entity, Column, ManyToOne, JoinColumn } from 'typeorm';
import { BaseEntity } from '../../common/entities/base.entity';
import { User } from '../../users/entities/user.entity';
import { Task } from '../../tasks/entities/task.entity';

@Entity('comments')
export class Comment extends BaseEntity {
  @Column({ type: 'varchar', length: 1000 })
  text: string;

  @Column({ name: 'task_id' })
  task_id: string;

  @Column({ name: 'user_id' })
  user_id: string;

  // Many comments belong to one task
  @ManyToOne(() => Task, (task) => task.comments, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'task_id' })
  task: Task;

  // Many comments belong to one user
  @ManyToOne(() => User, (user) => user.comments, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'user_id' })
  user: User;
}
