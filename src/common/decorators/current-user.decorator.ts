import { createParamDecorator, ExecutionContext } from '@nestjs/common';

// Extract user object from request (populated by JWT strategy)
export const CurrentUser = createParamDecorator(
  (data: unknown, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    return request.user;
  },
);
