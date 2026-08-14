-- Module-owned authority boundary. The retained Prisma migrations run with
-- ?schema=knowledge; this bootstrap is intentionally safe to re-run.
CREATE SCHEMA IF NOT EXISTS knowledge;
REVOKE ALL ON SCHEMA knowledge FROM PUBLIC;
GRANT USAGE, CREATE ON SCHEMA knowledge TO knowledge;
