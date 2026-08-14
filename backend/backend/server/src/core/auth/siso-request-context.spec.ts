import ava from "ava";

import {
  signSisoRequestContext,
  SisoRequestContextError,
  validateSisoRequestContext,
} from "./siso-request-context";

const claims = {
  clientId: "bykonz-yard",
  userId: "user-1",
  workspaceId: "workspace-1",
  capabilities: ["view", "edit", "share"],
  iat: 100,
  exp: 200,
} as const;

ava("accepts a valid signed SISO context", (t) => {
  const token = signSisoRequestContext(claims, "local-test-secret");
  t.deepEqual(validateSisoRequestContext(token, "local-test-secret", "bykonz-yard", "workspace-1", 150, "edit"), claims);
});

ava("fails closed for signature, expiry, client and workspace mismatches", (t) => {
  const token = signSisoRequestContext(claims, "local-test-secret");
  for (const [candidate, expected] of [
    [`${token.slice(0, -1)}x`, "invalid_signature"],
    [token, "expired"],
  ] as const) {
    t.throws(() => validateSisoRequestContext(candidate, "local-test-secret", "bykonz-yard", "workspace-1", expected === "expired" ? 201 : 150), { instanceOf: SisoRequestContextError, code: expected });
  }
  t.throws(() => validateSisoRequestContext(token, "local-test-secret", "other-client", "workspace-1", 150), { code: "client_mismatch" });
  t.throws(() => validateSisoRequestContext(token, "local-test-secret", "bykonz-yard", "other-workspace", 150), { code: "workspace_mismatch" });
  t.throws(() => validateSisoRequestContext(token, "local-test-secret", "bykonz-yard", "workspace-1", 150, "admin"), { code: "capability_denied" });
});
