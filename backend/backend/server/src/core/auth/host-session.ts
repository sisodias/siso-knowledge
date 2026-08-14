import { createHash } from "node:crypto";

import type { Request } from "express";
import { z } from "zod";

const HostSessionSchema = z.object({
  user: z.object({
    id: z.string().min(1).max(128),
    email: z.string().email().max(320),
    name: z.string().min(1).max(200),
    workspaceId: z.string().min(1).max(128),
  }),
  expiresAt: z.string().datetime(),
});

export type HostSession = z.infer<typeof HostSessionSchema>;

const HOST_COOKIE_NAMES = ["__Host-siso_session", "siso_host_session"];

export function getHostSessionToken(req: Pick<Request, "headers">) {
  const cookieHeader = req.headers.cookie;
  if (!cookieHeader) return null;
  const cookies = new Map(
    cookieHeader.split(";").map((part) => {
      const [name, ...value] = part.trim().split("=");
      return [name, value.join("=")] as const;
    }),
  );
  for (const name of HOST_COOKIE_NAMES) {
    const token = cookies.get(name);
    if (token) return { name, token };
  }
  return null;
}

export function hostSessionId(token: string) {
  const digest = createHash("sha256").update(token).digest("hex");
  return `siso_${digest.slice(0, 48)}`;
}

export async function fetchHostSession(
  endpoint: string,
  cookie: { name: string; token: string },
  fetcher: typeof fetch = fetch,
): Promise<HostSession | null> {
  const response = await fetcher(endpoint, {
    headers: {
      accept: "application/json",
      cookie: `${cookie.name}=${cookie.token}`,
    },
    signal: AbortSignal.timeout(3000),
  });
  if (response.status === 401) return null;
  if (!response.ok)
    throw new Error(`SISO host session check failed: ${response.status}`);
  return HostSessionSchema.parse(await response.json());
}
