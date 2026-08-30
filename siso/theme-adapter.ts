import type { CSSProperties } from 'react';

export type SisoKnowledgeThemeMode = 'light' | 'dark';

/**
 * Donor variables used by visible AFFiNE chrome and common controls.
 * Values are Base semantic references, never copied palette values.
 */
export const sisoKnowledgeTokenLinks = {
  '--affine-background-color': '--actionist-surface-canvas',
  '--affine-background-primary': '--actionist-surface-canvas',
  '--affine-background-primary-color': '--actionist-surface-canvas',
  '--affine-background-secondary': '--actionist-surface-panel',
  '--affine-background-secondary-color': '--actionist-surface-panel',
  '--affine-background-tertiary': '--actionist-surface-raised',
  '--affine-background-tertiary-color': '--actionist-surface-raised',
  '--affine-background-overlay-panel-color': '--actionist-surface-raised',
  '--affine-background-modal-color': '--actionist-surface-overlay',
  '--affine-text-primary': '--actionist-text-primary',
  '--affine-text-primary-color': '--actionist-text-primary',
  '--affine-text-secondary': '--actionist-text-muted',
  '--affine-text-secondary-color': '--actionist-text-muted',
  '--affine-text-tertiary': '--actionist-text-faint',
  '--affine-text-disable-color': '--actionist-text-faint',
  '--affine-text-emphasis-color': '--actionist-text-strong',
  '--affine-icon-color': '--actionist-text-primary',
  '--affine-icon-secondary': '--actionist-text-muted',
  '--affine-border-color': '--actionist-border-default',
  '--affine-divider-color': '--actionist-border-subtle',
  '--affine-primary-color': '--actionist-action-primary',
  '--affine-brand-color': '--actionist-action-primary',
  '--affine-link-color': '--actionist-action-primary',
  '--affine-hover-color': '--actionist-surface-hover',
  '--affine-hover-color-filled': '--actionist-surface-raised',
  '--affine-error-color': '--actionist-status-danger',
  '--affine-warning-color': '--actionist-status-warning',
  '--affine-success-color': '--actionist-status-positive',
  '--affine-processing-color': '--actionist-status-info',
  '--affine-font-family': '--actionist-type-font-sans',
  '--affine-font-sans-family': '--actionist-type-font-sans',
  '--affine-font-mono-family': '--actionist-type-font-mono',
  '--affine-font-code-family': '--actionist-type-font-mono',
  '--affine-font-base': '--actionist-type-size-md',
  '--affine-font-sm': '--actionist-type-size-sm',
  '--affine-font-xs': '--actionist-type-size-xs',
  '--affine-popover-radius': '--actionist-radius-control-lg',
  '--affine-popover-shadow': '--actionist-shadow-control',
  '--affine-menu-shadow': '--actionist-shadow-control',
  '--affine-overlay-shadow': '--actionist-shadow-modal',
  '--affine-overlay-panel-shadow': '--actionist-shadow-modal',
  '--affine-toolbar-shadow': '--actionist-shadow-control',
  '--affine-v2-background-primary': '--actionist-surface-canvas',
  '--affine-v2-background-secondary': '--actionist-surface-panel',
  '--affine-v2-layer-background-primary': '--actionist-surface-panel',
  '--affine-v2-layer-background-hoverOverlay': '--actionist-surface-hover',
  '--affine-v2-layer-background-overlayPanel': '--actionist-surface-raised',
  '--affine-v2-layer-background-error': '--actionist-status-danger',
  '--affine-v2-layer-insideBorder-border': '--actionist-border-default',
  '--affine-v2-layer-insideBorder-primaryBorder': '--actionist-border-focus',
  '--affine-v2-layer-insideBorder-blackBorder': '--actionist-border-strong',
  '--affine-v2-text-primary': '--actionist-text-primary',
  '--affine-v2-text-secondary': '--actionist-text-muted',
  '--affine-v2-text-placeholder': '--actionist-text-faint',
  '--affine-v2-pure-white-text': '--actionist-action-on-primary',
  '--affine-v2-icon-primary': '--actionist-text-primary',
  '--affine-v2-icon-activated': '--actionist-action-primary',
  '--affine-v2-icon-disable': '--actionist-text-faint',
  '--affine-v2-button-primary': '--actionist-action-primary',
  '--affine-v2-button-error': '--actionist-status-danger',
  '--affine-v2-button-disable': '--actionist-text-faint',
  '--affine-v2-input-background': '--actionist-surface-panel',
  '--affine-v2-tooltips-background': '--actionist-text-strong',
  '--affine-v2-tooltips-foreground': '--actionist-text-inverse',
} as const satisfies Record<`--affine-${string}`, `--actionist-${string}`>;

export type SisoKnowledgeThemeStyle = CSSProperties &
  Record<`--${string}`, string>;

export function createSisoKnowledgeThemeStyle(
  mode?: SisoKnowledgeThemeMode
): SisoKnowledgeThemeStyle {
  const style: SisoKnowledgeThemeStyle = {
    width: '100%',
    height: '100%',
    minWidth: 0,
    minHeight: 0,
    boxSizing: 'border-box',
    padding: 'var(--actionist-space-0)',
    borderRadius: 'var(--actionist-radius-panel)',
    backgroundColor: 'var(--actionist-surface-canvas)',
    color: 'var(--actionist-text-primary)',
    fontFamily: 'var(--actionist-type-font-sans)',
    transition:
      'background-color var(--actionist-motion-normal) var(--actionist-motion-easing), color var(--actionist-motion-normal) var(--actionist-motion-easing)',
  };

  if (mode) style.colorScheme = mode;

  for (const [donorToken, baseToken] of Object.entries(
    sisoKnowledgeTokenLinks
  )) {
    style[donorToken as `--${string}`] = `var(${baseToken})`;
  }

  return style;
}
