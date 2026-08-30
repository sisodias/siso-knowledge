import type { ComponentType, PropsWithChildren, ReactNode } from 'react';
import { createContext, useContext } from 'react';

import type { SisoKnowledgeIdentity } from './identity';
import { knowledgeDatabaseConfig, type KnowledgeDatabaseAdapter } from './database-adapter';
import { sisoKnowledgeBrand, sisoKnowledgeChromePolicy } from './assimilation/brand-chrome-policy';
import { createSisoKnowledgeThemeStyle, type SisoKnowledgeThemeMode } from './theme-adapter';

export function assertSisoKnowledgeIdentity(identity: SisoKnowledgeIdentity, expectedClientId: string) {
  if (identity.clientId !== expectedClientId) throw new Error('SISO Knowledge client mismatch');
  if (Date.parse(identity.expiresAt) <= Date.now()) throw new Error('SISO Knowledge identity expired');
  if (!identity.userId || !identity.workspaceId || identity.capabilities.length === 0) {
    throw new Error('SISO Knowledge identity is incomplete');
  }
  return identity;
}

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
  expectedClientId?: string;
  themeMode?: SisoKnowledgeThemeMode;
  /** The complete AFFiNE-derived App, including its providers and internal router. */
  donorApp: ComponentType;
  children?: ReactNode;
}

export function SisoKnowledgeModuleRoot({ host, donorApp: DonorApp, children, expectedClientId = 'bykonz-yard', themeMode }: PropsWithChildren<SisoKnowledgeModuleRootProps>) {
  assertSisoKnowledgeIdentity(host.identity, expectedClientId);
  return (
    <HostContext.Provider value={host}>
      <div
        data-siso-knowledge-brand={`${sisoKnowledgeBrand.product} ${sisoKnowledgeBrand.block}`}
        data-siso-knowledge-chrome={sisoKnowledgeChromePolicy.globalNavigation}
        data-siso-knowledge-contextual-navigation={sisoKnowledgeChromePolicy.contextualNavigation}
        data-siso-knowledge-theme={themeMode ?? 'host'}
        style={createSisoKnowledgeThemeStyle(themeMode)}
      >
        {children}
        <DonorApp />
      </div>
    </HostContext.Provider>
  );
}

export { knowledgeDatabaseConfig };
