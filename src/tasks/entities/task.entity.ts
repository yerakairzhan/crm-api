import { Entity, Column, ManyToOne, OneToMany, JoinColumn } from 'typeorm';
import { BaseEntity } from '../../common/entities/base.entity';
import { User } from '../../users/entities/user.entity';
import { Comment } from '../../comments/entities/comment.entity';

@Entity('tasks')
export class Task extends BaseEntity {
  @Column({ type: 'varchar', length: 1000 })
  description: string;

  @Column({ name: 'user_id' })
  user_id: string;

  // Many tasks belong to one user
  @ManyToOne(() => User, (user) => user.tasks, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'user_id' })
  user: User;

  // One task has many comments
  @OneToMany(() => Comment, (comment) => comment.task)
  comments: Comment[];
}
