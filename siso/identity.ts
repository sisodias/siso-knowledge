export interface SisoKnowledgeIdentity {
  userId: string;
  email: string;
  displayName?: string;
  clientId: string;
  workspaceId: string;
  expiresAt: string;
  capabilities: Array<'view' | 'edit' | 'share' | 'admin'>;
}

/** The host session is the only client-facing identity source. */
export interface SisoKnowledgeIdentityAdapter {
  getCurrentIdentity(): SisoKnowledgeIdentity | null;
}
