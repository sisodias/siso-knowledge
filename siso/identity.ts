export interface SisoKnowledgeIdentity {
  userId: string;
  email: string;
  displayName?: string;
  clientId: string;
  workspaceId: string;
}

/** The host session is the only client-facing identity source. */
export interface SisoKnowledgeIdentityAdapter {
  getCurrentIdentity(): SisoKnowledgeIdentity | null;
}
