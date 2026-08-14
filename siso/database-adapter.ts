export interface KnowledgeDatabaseConfig {
  schema: 'knowledge';
  redisNamespace: 'knowledge';
  yjsNamespace: 'knowledge';
  blobNamespace: 'knowledge';
}

/** Phase 1 seam: the host supplies configuration; no data migration occurs here. */
export interface KnowledgeDatabaseAdapter {
  readonly config: KnowledgeDatabaseConfig;
}

export const knowledgeDatabaseConfig: KnowledgeDatabaseConfig = {
  schema: 'knowledge',
  redisNamespace: 'knowledge',
  yjsNamespace: 'knowledge',
  blobNamespace: 'knowledge',
};
