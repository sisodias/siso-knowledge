import { WinstonLogger } from 'nest-winston';

import { SisoNotesLogger as RawSisoNotesLogger } from '../../../base/logger';

export class SisoNotesLogger extends WinstonLogger {
  override error(
    message: any,
    stackOrError?: Error | string | unknown,
    context?: string
  ) {
    super.error(
      message,
      RawSisoNotesLogger.formatStack(stackOrError) as string,
      context
    );
  }
}
