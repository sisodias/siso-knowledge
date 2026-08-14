import { StoreExtensionManager } from '@blocksuite/sisonotes/ext-loader';
import { getInternalStoreExtensions } from '@blocksuite/sisonotes/extensions/store';

const manager = new StoreExtensionManager(getInternalStoreExtensions());

export function getStoreManager() {
  return manager;
}
