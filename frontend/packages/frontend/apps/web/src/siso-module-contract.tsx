import type { ComponentType, PropsWithChildren, ReactNode } from 'react';
import { createContext, useContext } from 'react';

export type SisoKnowledgeCapability = 'view' | 'edit' | 'share' | 'admin';
export interface SisoKnowledgeIdentity {
  userId: string;
  email: string;
  displayName?: string;
  clientId: string;
  workspaceId: string;
  expiresAt: string;
  capabilities: SisoKnowledgeCapability[];
}
export interface SisoKnowledgeHostContext {
  identity: SisoKnowledgeIdentity;
  database: { config: { schema: 'knowledge'; redisNamespace: 'knowledge'; yjsNamespace: 'knowledge'; blobNamespace: 'knowledge' } };
  tokens: Record<string, string>;
}
export interface SisoKnowledgeModuleRootProps {
  host: SisoKnowledgeHostContext;
  expectedClientId?: string;
  donorApp: ComponentType;
  children?: ReactNode;
}
const HostContext = createContext<SisoKnowledgeHostContext | null>(null);
export function useSisoKnowledgeHost() {
  const context = useContext(HostContext);
  if (!context) throw new Error('SisoKnowledgeModuleRoot must be mounted by the SISO host');
  return context;
}
export function assertSisoKnowledgeIdentity(identity: SisoKnowledgeIdentity, expectedClientId: string) {
  if (identity.clientId !== expectedClientId) throw new Error('SISO Knowledge client mismatch');
  if (Date.parse(identity.expiresAt) <= Date.now()) throw new Error('SISO Knowledge identity expired');
  if (!identity.userId || !identity.workspaceId || identity.capabilities.length === 0) throw new Error('SISO Knowledge identity is incomplete');
}
export function SisoKnowledgeModuleRoot({ host, donorApp: DonorApp, children, expectedClientId = 'bykonz-yard' }: PropsWithChildren<SisoKnowledgeModuleRootProps>) {
  assertSisoKnowledgeIdentity(host.identity, expectedClientId);
  return <HostContext.Provider value={host}>{children}<DonorApp /></HostContext.Provider>;
}
