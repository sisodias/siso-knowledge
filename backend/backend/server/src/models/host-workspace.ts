import * as Y from "yjs";

export function createHostWorkspaceUpdate(workspaceId: string) {
  const doc = new Y.Doc({ guid: workspaceId });
  const meta = doc.getMap("meta");
  meta.set("pages", new Y.Array());
  meta.set("name", "SISO Docs");
  return Y.encodeStateAsUpdate(doc);
}
