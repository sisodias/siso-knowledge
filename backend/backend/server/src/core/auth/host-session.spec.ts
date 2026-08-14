import ava from "ava";

import {
  fetchHostSession,
  getHostSessionToken,
  hostSessionId,
} from "./host-session";

ava("reads only the canonical SISO host session cookies", (t) => {
  t.deepEqual(
    getHostSessionToken({
      headers: { cookie: "other=x; siso_host_session=opaque-token" },
    }),
    { name: "siso_host_session", token: "opaque-token" },
  );
  t.is(
    getHostSessionToken({ headers: { cookie: "affine_session=other" } }),
    null,
  );
});

ava("derives a stable non-reversible docs session id", (t) => {
  const first = hostSessionId("opaque-token");
  t.is(first, hostSessionId("opaque-token"));
  t.not(first, hostSessionId("other-token"));
  t.false(first.includes("opaque-token"));
});

ava(
  "forwards only the SISO cookie and validates the host payload",
  async (t) => {
    const session = await fetchHostSession(
      "http://127.0.0.1:4320/api/auth/session",
      { name: "siso_host_session", token: "opaque-token" },
      async (_input, init) => {
        t.deepEqual(init?.headers, {
          accept: "application/json",
          cookie: "siso_host_session=opaque-token",
        });
        return new Response(
          JSON.stringify({
            user: {
              id: "siso-user",
              email: "user@siso.local",
              name: "SISO User",
              workspaceId: "siso-workspace",
            },
            expiresAt: new Date(Date.now() + 60_000).toISOString(),
          }),
          { status: 200, headers: { "content-type": "application/json" } },
        );
      },
    );
    t.is(session?.user.id, "siso-user");
  },
);

ava("treats a revoked host session as anonymous", async (t) => {
  const session = await fetchHostSession(
    "http://127.0.0.1:4320/api/auth/session",
    { name: "siso_host_session", token: "revoked" },
    async () => new Response(null, { status: 401 }),
  );
  t.is(session, null);
});
