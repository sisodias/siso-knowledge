# Generated Knowledge index

`_index/` is a rebuildable projection over canonical pages.

- Never hand-edit generated manifests, maps, search databases, backlinks, redirects, or status.
- Change source pages or generator code, then intentionally run `python3 queries/rebuild_index.py`.
- Runtime events and agent status are local data-plane state and are ignored by Git.
- A generated file is never an alternate writer or evidence that its source is current.
