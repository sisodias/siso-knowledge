import { createHmac, timingSafeEqual } from "node:crypto";

import type { NextFunction, Request, Response } from "express";
import { z } from "zod";

export const SisoKnowledgeCapability = z.enum(["view", "edit", "share", "admin"]);
export type SisoKnowledgeCapability = z.infer<typeof SisoKnowledgeCapability>;

const Claims = z.object({
  clientId: z.string().min(1).max(128),
  userId: z.string().min(1).max(128),
  workspaceId: z.string().min(1).max(128),
  capabilities: z.array(SisoKnowledgeCapability).min(1),
  exp: z.number().int().positive(),
  iat: z.number().int().positive(),
});

export type SisoRequestContext = z.infer<typeof Claims>;

export class SisoRequestContextError extends Error {
  constructor(readonly code: "malformed" | "invalid_signature" | "expired" | "client_mismatch" | "workspace_mismatch" | "capability_denied") {
    super(`Invalid SISO Knowledge request context: ${code}`);
    this.name = "SisoRequestContextError";
  }
}

const encode = (value: string) => Buffer.from(value).toString("base64url");

export function signSisoRequestContext(claims: SisoRequestContext, secret: string) {
  const payload = encode(JSON.stringify(Claims.parse(claims)));
  const signature = createHmac("sha256", secret).update(payload).digest("base64url");
  return `${payload}.${signature}`;
}

export function validateSisoRequestContext(
  token: string,
  secret: string,
  expectedClientId: string,
  expectedWorkspaceId: string,
  now = Math.floor(Date.now() / 1000),
  requiredCapability?: SisoKnowledgeCapability,
) {
  const [payload, signature] = token.split(".");
  if (!payload || !signature) throw new SisoRequestContextError("malformed");
  const expected = createHmac("sha256", secret).update(payload).digest("base64url");
  const actualBytes = Buffer.from(signature);
  const expectedBytes = Buffer.from(expected);
  if (actualBytes.length !== expectedBytes.length || !timingSafeEqual(actualBytes, expectedBytes)) {
    throw new SisoRequestContextError("invalid_signature");
  }
  let claims: SisoRequestContext;
  try {
    claims = Claims.parse(JSON.parse(Buffer.from(payload, "base64url").toString("utf8")));
  } catch {
    throw new SisoRequestContextError("malformed");
  }
  if (claims.exp <= now || claims.iat > now + 30) throw new SisoRequestContextError("expired");
  if (claims.clientId !== expectedClientId) throw new SisoRequestContextError("client_mismatch");
  if (claims.workspaceId !== expectedWorkspaceId) throw new SisoRequestContextError("workspace_mismatch");
  if (requiredCapability && !claims.capabilities.includes(requiredCapability)) {
    throw new SisoRequestContextError("capability_denied");
  }
  return claims;
}

declare global {
  namespace Express {
    interface Request { sisoKnowledgeContext?: SisoRequestContext; }
  }
}

export function sisoRequestContextMiddleware(options: {
  secret: string;
  clientId: string;
  workspaceId: string;
  capability?: SisoKnowledgeCapability;
}) {
  return (req: Request, res: Response, next: NextFunction) => {
    const token = req.header("x-siso-request-context");
    if (!token) return res.status(401).json({ error: "siso_context_required" });
    try {
      req.sisoKnowledgeContext = validateSisoRequestContext(
        token,
        options.secret,
        options.clientId,
        options.workspaceId,
        undefined,
        options.capability,
      );
      return next();
    } catch (error) {
      const code = error instanceof SisoRequestContextError ? error.code : "malformed";
      return res.status(code === "capability_denied" ? 403 : 401).json({ error: `siso_context_${code}` });
    }
  };
}
