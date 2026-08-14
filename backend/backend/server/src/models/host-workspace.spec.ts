import test from "ava";
import * as Y from "yjs";

import { createHostWorkspaceUpdate } from "./host-workspace";

test("creates an initialized empty SISO workspace root document", (t) => {
  const doc = new Y.Doc({ guid: "siso-workspace" });
  Y.applyUpdate(doc, createHostWorkspaceUpdate("siso-workspace"));

  const meta = doc.getMap("meta");
  t.is(meta.get("name"), "SISO Docs");
  t.true(meta.get("pages") instanceof Y.Array);
  t.is((meta.get("pages") as Y.Array<unknown>).length, 0);
});
