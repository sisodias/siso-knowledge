export const sisoKnowledgeBrand = {
  product: 'Actionist',
  block: 'Knowledge',
  donor: 'AFFiNE',
} as const;

/** Hosted-mode authority; this does not change the donor's standalone UI. */
export const sisoKnowledgeChromePolicy = {
  globalNavigation: 'host',
  workspaceSwitcher: 'host',
  accountSettingsBilling: 'host',
  documentTitle: 'host',
  contextualNavigation: 'knowledge',
  editorAndCanvas: 'knowledge',
  donorPromotion: 'suppressed-when-hosted',
  legacyPostMessageBridge: 'compatibility-only',
} as const;
