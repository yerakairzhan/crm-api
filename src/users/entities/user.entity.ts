import { Entity, Column, OneToMany } from 'typeorm';
import { BaseEntity } from '../../common/entities/base.entity';
import { Task } from '../../tasks/entities/task.entity';
import { Comment } from '../../comments/entities/comment.entity';

export enum UserRole {
  AUTHOR = 'author',
  USER = 'user',
}

@Entity('users')
export class User extends BaseEntity {
  @Column({ unique: true })
  email: string;

  @Column()
  password: string;

  @Column({
    type: 'enum',
    enum: UserRole,
    default: UserRole.USER,
  })
  role: UserRole;

  @Column({ name: 'task_id', type: 'uuid', nullable: true })
  task_id?: string;

  @Column({ name: 'refresh_token_hash', type: 'varchar', nullable: true })
  refresh_token_hash?: string | null;

  // One user can have many tasks
  @OneToMany(() => Task, (task) => task.user)
  tasks: Task[];

  // One user can have many comments
  @OneToMany(() => Comment, (comment) => comment.user)
  comments: Comment[];
}
