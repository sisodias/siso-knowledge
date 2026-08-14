import { App } from './app';
import { SisoKnowledgeModuleRoot, type SisoKnowledgeModuleRootProps } from './siso-module-contract';

/** Host-native entrypoint; the complete donor App remains compiled in-process. */
export function SisoKnowledgeModule(props: Omit<SisoKnowledgeModuleRootProps, 'donorApp'>) {
  return <SisoKnowledgeModuleRoot {...props} donorApp={App} />;
}

export { SisoKnowledgeModuleRoot } from './siso-module-contract';
