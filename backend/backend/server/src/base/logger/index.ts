import { Global, Module } from '@nestjs/common';

import { ConfigModule } from '../config';
import { SisoNotesLogger } from './service';

@Global()
@Module({
  imports: [ConfigModule],
  providers: [SisoNotesLogger],
  exports: [SisoNotesLogger],
})
export class LoggerModule {}

export { SisoNotesLogger } from './service';
