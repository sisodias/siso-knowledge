import { getBuildConfig } from '@siso-tools/utils/build-config';
import { Package } from '@siso-tools/utils/workspace';

import { createApp } from './create-app';

globalThis.BUILD_CONFIG = getBuildConfig(new Package('@siso/web'), {
  mode: 'development',
  channel: 'canary',
});
// @ts-expect-error testing
globalThis.app = await createApp();
