# PostgreSQL Best Practices

A practical reference for schema design, performance, security, and operations when running PostgreSQL in production.

---

## 1. Schema & Data Modeling

- Choose the right data types — `TEXT` over `VARCHAR(n)` unless you truly need a length cap (Postgres doesn't penalize `TEXT`); use `NUMERIC` for money, never `FLOAT`.
- Prefer `TIMESTAMPTZ` over `TIMESTAMP` — always store time zone–aware timestamps and let the client convert to local time.
- Use `UUID` or `BIGINT` (not plain `INT`/`SERIAL`) for primary keys on tables expected to grow large, to avoid ID exhaustion.
- Normalize to 3NF by default; denormalize deliberately and only where a measured read-performance need justifies it.
- Use `ENUM` types or a lookup/reference table for fixed value sets — enums are cheap and enforce validity at the DB level.
- Add `NOT NULL` constraints wherever a column shouldn't logically be empty — don't leave nullability to the application layer.
- Use `CHECK` constraints for simple invariants (e.g., `CHECK (price >= 0)`) instead of enforcing them only in code.

```sql
CREATE TABLE orders (
    id           BIGSERIAL PRIMARY KEY,
    customer_id  BIGINT NOT NULL REFERENCES customers(id),
    status       order_status NOT NULL DEFAULT 'pending',
    total_amount NUMERIC(12,2) NOT NULL CHECK (total_amount >= 0),
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

---

## 2. Indexing

- Index columns used in `WHERE`, `JOIN`, `ORDER BY`, and `GROUP BY` clauses — but don't over-index; every index adds write overhead and storage.
- Use **composite indexes** matching your actual query patterns (leftmost-prefix rule applies).
- Use a **partial index** when queries filter on a common subset (e.g., `WHERE deleted_at IS NULL`).
- Use `EXPLAIN (ANALYZE, BUFFERS)` to verify an index is actually being used — don't assume.
- Add indexes on foreign key columns explicitly; Postgres does **not** create them automatically (unlike some other databases).
- Consider `GIN` indexes for full-text search (`tsvector`) and JSONB columns; `BRIN` indexes for very large, naturally ordered tables (e.g., time-series data).

```sql
-- Composite index matching a common query
CREATE INDEX idx_orders_customer_status ON orders (customer_id, status);

-- Partial index for a common filtered query
CREATE INDEX idx_orders_active ON orders (customer_id) WHERE status != 'cancelled';

-- Check query plan
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE customer_id = 42;
```

---

## 3. Query Performance

- Avoid `SELECT *` — fetch only the columns you need, especially on wide tables.
- Avoid N+1 query patterns from the application layer; batch with `IN (...)` or use joins/prefetching (e.g., SQLAlchemy `selectinload`, Django `select_related`/`prefetch_related`).
- Use `LIMIT`/`OFFSET` carefully — `OFFSET` on large tables is slow; prefer **keyset (cursor) pagination** for large datasets.
- Watch for implicit type casts that silently defeat indexes (e.g., comparing `TEXT` to `INT`).
- Use `pg_stat_statements` to find your slowest and most frequent queries in production.

```sql
-- Keyset pagination instead of OFFSET
SELECT * FROM orders
WHERE id > :last_seen_id
ORDER BY id
LIMIT 50;
```

```sql
-- Find slow/expensive queries (requires pg_stat_statements extension)
SELECT query, calls, total_exec_time, mean_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

---

## 4. Transactions & Concurrency

- Keep transactions **short** — long-running transactions hold locks and block `VACUUM` from reclaiming dead rows.
- Choose the right isolation level: `READ COMMITTED` (default) is fine for most workloads; use `REPEATABLE READ` or `SERIALIZABLE` only when you specifically need stronger guarantees, and handle serialization failures with retries.
- Use `SELECT ... FOR UPDATE` for explicit row locking when you need to prevent concurrent modification (e.g., decrementing inventory).
- Use `INSERT ... ON CONFLICT DO UPDATE` (upsert) instead of a manual check-then-insert, which is race-prone.

```sql
-- Safe upsert
INSERT INTO inventory (product_id, quantity)
VALUES (1, 10)
ON CONFLICT (product_id)
DO UPDATE SET quantity = inventory.quantity + EXCLUDED.quantity;
```

```sql
-- Explicit row lock to prevent oversell
BEGIN;
SELECT quantity FROM inventory WHERE product_id = 1 FOR UPDATE;
UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 1;
COMMIT;
```

---

## 5. Migrations

- Use a migration tool tied to your framework/ORM: **Alembic** (SQLAlchemy), Django migrations, or a standalone tool like `sqlx`/`golang-migrate`/`Flyway`.
- Make migrations **backward-compatible** during rollout (expand/contract pattern) so old and new app versions can run simultaneously during deploy:
  1. Add new column (nullable or with default) — deploy.
  2. Backfill data — deploy.
  3. Update app to use new column — deploy.
  4. Drop old column — deploy.
- Avoid long-locking operations on large tables in a single migration (e.g., adding a `NOT NULL` column with a default on a huge table locks it). Use `ADD COLUMN ... DEFAULT` on Postgres 11+ (metadata-only, fast) then backfill separately if further changes are needed.
- Always test migrations against a production-sized (or realistically sized) dataset before running in production.
- Wrap DDL changes in transactions where possible so failures roll back cleanly (Postgres supports transactional DDL, unlike MySQL).

---

## 6. Security

- Apply **least privilege**: create role-specific DB users (app read/write, reporting read-only, migration/admin) — never connect the application with a superuser account.
- Use `REVOKE`/`GRANT` explicitly rather than relying on default public schema permissions.
- Enforce SSL/TLS on connections (`sslmode=require` or stricter, e.g., `verify-full`).
- Use parameterized queries / your ORM's query builder — never string-interpolate user input into SQL.
- Enable **Row-Level Security (RLS)** for multi-tenant applications so tenants can't see each other's rows even via a bug in the application layer.
- Rotate DB credentials regularly and store them in a secrets manager, not in config files.
- Restrict network access to the DB — private subnet/VPC only, security group allow-listing, no public internet exposure.

```sql
-- Least-privilege app role
CREATE ROLE app_user WITH LOGIN PASSWORD :'secure_password';
GRANT CONNECT ON DATABASE mydb TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
REVOKE ALL ON pg_catalog.pg_authid FROM app_user;
```

```sql
-- Row-level security example (multi-tenant)
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON orders
    USING (tenant_id = current_setting('app.current_tenant')::uuid);
```

---

## 7. Backup & Recovery

- Enable **continuous archiving (WAL)** + periodic base backups for point-in-time recovery (PITR), not just nightly dumps.
- Use `pg_basebackup`, or a managed solution (AWS RDS/Aurora automated backups, `pgBackRest`, `wal-g`).
- Test restores regularly — an untested backup is not a backup.
- Encrypt backups at rest and control access via IAM/least-privilege.
- Define and document your **RPO/RTO** targets, and verify your backup cadence actually meets them.

---

## 8. Connection Management

- Use a **connection pooler** — **PgBouncer** (transaction or session pooling) — since Postgres connections are relatively expensive (each is a full OS process).
- Size your application's connection pool deliberately; too many idle connections waste server memory and can starve the DB under load.
- Set sensible `statement_timeout` and `idle_in_transaction_session_timeout` to prevent runaway queries or forgotten open transactions from holding locks indefinitely.

```sql
-- Guard against runaway/forgotten transactions
ALTER ROLE app_user SET statement_timeout = '30s';
ALTER ROLE app_user SET idle_in_transaction_session_timeout = '60s';
```

---

## 9. Maintenance: VACUUM & Autovacuum

- Postgres uses MVCC — updated/deleted rows leave "dead tuples" that must be reclaimed by `VACUUM`. Never disable autovacuum globally.
- Tune autovacuum settings (`autovacuum_vacuum_scale_factor`, `autovacuum_vacuum_cost_limit`) more aggressively for high-churn tables rather than relying on defaults.
- Run `VACUUM (ANALYZE)` after large bulk deletes/updates so the planner's statistics stay accurate.
- Watch for **table bloat** and **transaction ID (XID) wraparound** risk on very high-write tables; monitor `age(datfrozenxid)`.
- Use `pg_stat_user_tables` to check `n_dead_tup` and last autovacuum run per table.

```sql
SELECT relname, n_dead_tup, last_autovacuum, last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 10;
```

---

## 10. Monitoring & Observability

- Enable `pg_stat_statements` in production to track query-level performance over time.
- Monitor: connection count vs. `max_connections`, cache hit ratio, replication lag (if using replicas), lock waits, disk usage growth, and long-running queries.
- Use tools like **pgAdmin**, **pganalyze**, **Datadog**, or **CloudWatch/RDS Performance Insights** for ongoing visibility.
- Set alerts on: connection saturation, replication lag exceeding threshold, disk space thresholds, and unusually slow queries.

```sql
-- Cache hit ratio (should generally be > 99% for OLTP workloads)
SELECT
  sum(heap_blks_hit) / nullif(sum(heap_blks_hit) + sum(heap_blks_read), 0) AS cache_hit_ratio
FROM pg_statio_user_tables;
```

---

## 11. High Availability & Scaling

- Use **streaming replication** with a standby (or managed multi-AZ, e.g., RDS Multi-AZ) for failover.
- Offload read-heavy traffic to **read replicas**; be explicit in the app about read-after-write consistency needs (replicas lag).
- Consider **partitioning** (declarative table partitioning by range or list) for very large tables (e.g., time-series/event data) to keep queries and maintenance fast.
- Scale vertically first (more CPU/RAM) before reaching for sharding — Postgres handles surprisingly large single-node workloads well.
- For extreme scale, evaluate **Citus** (distributed Postgres) rather than building custom sharding logic.

```sql
-- Declarative range partitioning by date
CREATE TABLE events (
    id BIGSERIAL,
    created_at TIMESTAMPTZ NOT NULL,
    payload JSONB
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2026_09 PARTITION OF events
    FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');
```

---

## 12. Application Integration (ORM Notes)

- **SQLAlchemy**: use connection pooling (`pool_size`, `max_overflow`), enable `pool_pre_ping` to avoid stale-connection errors, and prefer explicit `selectinload`/`joinedload` to control eager loading.
- **Django**: set `CONN_MAX_AGE` for persistent connections, use `select_related`/`prefetch_related` to avoid N+1 queries, and review generated SQL with `django-debug-toolbar` in dev.
- Always run schema migrations through your ORM's migration tool — never hand-edit production schema out-of-band from the migration history.

---

## Quick Reference Checklist

- [ ] Correct data types (`TIMESTAMPTZ`, `NUMERIC`, `TEXT`, `UUID`/`BIGINT` PKs)
- [ ] `NOT NULL` and `CHECK` constraints enforced at the DB level
- [ ] Indexes match real query patterns; verified with `EXPLAIN ANALYZE`
- [ ] Foreign keys explicitly indexed
- [ ] Short transactions; correct isolation level; upserts instead of check-then-insert
- [ ] Backward-compatible, tested migrations (expand/contract pattern)
- [ ] Least-privilege DB roles; SSL enforced; RLS for multi-tenant data
- [ ] PITR-capable backups, tested restores, encrypted at rest
- [ ] Connection pooling (PgBouncer) with sane timeouts configured
- [ ] Autovacuum tuned; bloat and XID wraparound monitored
- [ ] `pg_stat_statements` + monitoring/alerting in place
- [ ] Replication/HA strategy and partitioning plan for large tables

---

*Revisit indexing and query performance as data volume grows — what's fast at 10K rows can degrade sharply at 10M without proactive tuning.*
