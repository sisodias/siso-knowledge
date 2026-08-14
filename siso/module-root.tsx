import type { ComponentType, PropsWithChildren, ReactNode } from 'react';
import { createContext, useContext } from 'react';

import type { SisoKnowledgeIdentity } from './identity';
import { knowledgeDatabaseConfig, type KnowledgeDatabaseAdapter } from './database-adapter';

export interface SisoKnowledgeHostContext {
  identity: SisoKnowledgeIdentity;
  database: KnowledgeDatabaseAdapter;
  tokens: Record<string, string>;
}

const HostContext = createContext<SisoKnowledgeHostContext | null>(null);

export function useSisoKnowledgeHost() {
  const context = useContext(HostContext);
  if (!context) throw new Error('SisoKnowledgeModuleRoot must be mounted by the SISO host');
  return context;
}

export interface SisoKnowledgeModuleRootProps {
  host: SisoKnowledgeHostContext;
  /** The complete AFFiNE-derived App, including its providers and internal router. */
  donorApp: ComponentType;
  children?: ReactNode;
}

export function SisoKnowledgeModuleRoot({ host, donorApp: DonorApp, children }: PropsWithChildren<SisoKnowledgeModuleRootProps>) {
  return (
    <HostContext.Provider value={host}>
      {children}
      <DonorApp />
    </HostContext.Provider>
  );
}

export { knowledgeDatabaseConfig };
