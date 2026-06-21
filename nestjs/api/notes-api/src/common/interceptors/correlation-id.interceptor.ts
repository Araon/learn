import { Request, Response } from 'express';
import {
  CallHandler,
  ExecutionContext,
  Injectable,
  NestInterceptor,
} from '@nestjs/common';
import { Observable, tap } from 'rxjs';
import { v4 as uuid } from 'uuid';

interface RequestWithCorrelation extends Request {
  correlationId?: string;
}

@Injectable()
export class CorrelationIdInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest<RequestWithCorrelation>();
    const response = context.switchToHttp().getResponse<Response>();

    const correlationId =
      (request.headers['x-correlation-id'] as string | undefined) || uuid();

    request.correlationId = correlationId;
    response.setHeader('x-correlation-id', correlationId);

    const now = Date.now();
    return next.handle().pipe(
      tap(() => {
        const duration = Date.now() - now;
        console.log(
          `[${correlationId}] ${request.method} ${request.url} - ${response.statusCode} (${duration}ms)`,
        );
      }),
    );
  }
}
