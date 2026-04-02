## 📂 Python Learning Files
[Basics](BASICS.md) | [Advanced](ADVANCED.md) | [**SQL**](SQL.md) | [Senior Dev Guide](README.md)

---

# 🐘 SQL & PostgreSQL – Complete Learning & Interview Preparation Guide

> **Level:** Beginner → Expert  
> **Covers:** SQL Fundamentals, PostgreSQL Internals, Query Optimization, Best Practices  
> **Goal:** Master SQL and PostgreSQL for production systems and senior-level interviews

---

## Table of Contents

### Part I – SQL Basics
1. [Module 1: Relational Model & SQL Fundamentals](#module-1)
2. [Module 2: DDL – Creating & Managing Tables](#module-2)
3. [Module 3: DML – CRUD Operations](#module-3)
4. [Module 4: Filtering, Sorting & Aggregation](#module-4)
5. [Module 5: Joins](#module-5)
6. [Module 6: Subqueries & CTEs](#module-6)

### Part II – SQL Advanced
7. [Module 7: Window Functions](#module-7)
8. [Module 8: Indexes & Performance](#module-8)
9. [Module 9: Transactions & Concurrency](#module-9)
10. [Module 10: PostgreSQL-Specific Features](#module-10)
11. [Module 11: Query Optimization & EXPLAIN](#module-11)
12. [Module 12: Schema Design & Best Practices](#module-12)

### Part III – Interview & Challenges
13. [Interview Questions](#interview-questions)
14. [Coding Challenges](#coding-challenges)
15. [Final Summary](#final-summary)

---

# PART I – SQL BASICS

---

## Module 1: Relational Model & SQL Fundamentals {#module-1}

### 📖 Explanation
A **relational database** stores data in tables (relations) with rows (tuples) and columns (attributes). Relationships between tables are expressed through keys. SQL (Structured Query Language) is the standard language for querying and manipulating relational data.

### 🔑 Key Concepts
| Concept | Description |
|---|---|
| **Table** | Named collection of rows with fixed columns |
| **Primary Key (PK)** | Uniquely identifies each row; never NULL |
| **Foreign Key (FK)** | References a PK in another table; enforces referential integrity |
| **Unique Key** | Enforces uniqueness but allows NULL |
| **NOT NULL** | Column must have a value |
| **Check Constraint** | Enforces a domain rule on column values |
| **Normalization** | Organizing data to reduce redundancy (1NF → 3NF → BCNF) |
| **ACID** | Atomicity, Consistency, Isolation, Durability |

### 🏛️ Normalization Quick Reference
```
1NF → No repeating groups; atomic values
2NF → No partial dependencies (all cols depend on full PK)
3NF → No transitive dependencies (non-key cols depend only on PK)
BCNF → Every determinant is a candidate key
```

### 💻 Example
```sql
-- Entity Relationship: Users place Orders containing Products

-- Primary key, constraints, and foreign keys
CREATE TABLE users (
    id         SERIAL PRIMARY KEY,
    email      VARCHAR(255) UNIQUE NOT NULL,
    username   VARCHAR(50)  NOT NULL,
    created_at TIMESTAMPTZ  DEFAULT NOW()
);

CREATE TABLE products (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    price       NUMERIC(10,2) NOT NULL CHECK (price >= 0),
    stock_qty   INTEGER NOT NULL DEFAULT 0 CHECK (stock_qty >= 0)
);

CREATE TABLE orders (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status      VARCHAR(20) NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending','processing','shipped','delivered','cancelled')),
    total       NUMERIC(12,2) NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE order_items (
    id          SERIAL PRIMARY KEY,
    order_id    INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id  INTEGER NOT NULL REFERENCES products(id),
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    unit_price  NUMERIC(10,2) NOT NULL,
    UNIQUE (order_id, product_id)   -- composite unique constraint
);
```

### 🏭 Real-world Use Cases
- E-commerce platforms (users, orders, products, inventory)
- Financial systems (accounts, transactions, ledgers)
- CMS platforms (articles, authors, categories, tags)
- SaaS multi-tenant applications

### ⚠️ Common Mistakes
- Using `VARCHAR` for everything (use proper types: `NUMERIC`, `BOOLEAN`, `DATE`)
- Storing multiple values in one column (violates 1NF)
- Missing foreign key constraints (data integrity issues)
- Using natural keys (email, SSN) as primary keys — they can change

### ✅ Best Practices
- Always define a surrogate `SERIAL`/`UUID` primary key
- Apply `NOT NULL` by default; allow NULL only when absence is meaningful
- Use `TIMESTAMPTZ` (timezone-aware) over `TIMESTAMP` for all timestamps
- Define `ON DELETE` behavior explicitly (CASCADE, SET NULL, RESTRICT)
- Name constraints explicitly for clear error messages

### 📝 Mini Summary
> The relational model is the foundation of all SQL. Strong schema design with proper constraints prevents entire classes of bugs before they happen.

---

## Module 2: DDL – Creating & Managing Tables {#module-2}

### 📖 Explanation
**DDL (Data Definition Language)** commands define the structure of the database: creating, altering, and dropping tables, indexes, sequences, and schemas.

### 🔑 Key Concepts
- `CREATE TABLE` / `CREATE INDEX` / `CREATE SCHEMA`
- `ALTER TABLE` — add/drop/modify columns and constraints
- `DROP TABLE` — remove table (data destroyed)
- `TRUNCATE` — fast empty a table
- Data types: numeric, character, date/time, boolean, JSON, arrays, UUID
- Sequences and `SERIAL` / `BIGSERIAL` / `GENERATED ALWAYS AS IDENTITY`
- Schemas — namespacing for tables

### 💻 Example
```sql
-- ─── Schemas for namespacing ───
CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS audit;

-- ─── PostgreSQL data types showcase ───
CREATE TABLE app.employees (
    -- Identity
    id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uuid          UUID DEFAULT gen_random_uuid() UNIQUE,

    -- Text
    first_name    VARCHAR(100) NOT NULL,
    last_name     VARCHAR(100) NOT NULL,
    bio           TEXT,

    -- Numeric
    salary        NUMERIC(12,2) NOT NULL CHECK (salary > 0),
    rating        SMALLINT CHECK (rating BETWEEN 1 AND 5),

    -- Boolean
    is_active     BOOLEAN NOT NULL DEFAULT TRUE,

    -- Date/Time (always use TIMESTAMPTZ!)
    birth_date    DATE,
    hired_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fired_at      TIMESTAMPTZ,

    -- PostgreSQL-specific types
    tags          TEXT[],                  -- array
    metadata      JSONB,                   -- binary JSON
    work_schedule INT4RANGE,               -- range type
    location      POINT,                   -- geometric

    -- Computed column (PostgreSQL 12+)
    full_name     TEXT GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED
);

-- ─── ALTER TABLE ───
ALTER TABLE app.employees
    ADD COLUMN department_id INTEGER REFERENCES app.departments(id),
    ADD COLUMN email VARCHAR(255) UNIQUE,
    ALTER COLUMN bio SET NOT NULL,
    ALTER COLUMN salary SET DEFAULT 50000,
    DROP COLUMN work_schedule;

-- Rename
ALTER TABLE app.employees RENAME COLUMN rating TO performance_rating;
ALTER TABLE app.employees RENAME TO staff;

-- ─── Constraints after creation ───
ALTER TABLE app.employees
    ADD CONSTRAINT chk_fired_after_hired
    CHECK (fired_at IS NULL OR fired_at > hired_at);

ALTER TABLE app.employees
    ADD CONSTRAINT uq_email UNIQUE (email);

-- ─── TRUNCATE vs DELETE ───
TRUNCATE TABLE app.audit_logs;                      -- fast, no WHERE
TRUNCATE TABLE app.orders RESTART IDENTITY CASCADE; -- reset sequences too

-- ─── DROP with safety ───
DROP TABLE IF EXISTS app.temp_imports CASCADE;
DROP SCHEMA IF EXISTS staging CASCADE;
```

### 🏭 Real-world Use Cases
- Schema migrations in CI/CD pipelines
- Adding audit columns to existing tables
- Multi-tenant schemas (one schema per tenant)
- JSONB columns for flexible/semi-structured data

### ⚠️ Common Mistakes
```sql
-- Using INT instead of BIGINT for IDs at scale
id SERIAL PRIMARY KEY    -- ❌ Max 2.1B rows before overflow
id BIGSERIAL PRIMARY KEY -- ✅ Max 9.2 quintillion rows

-- Storing timestamps without timezone
created_at TIMESTAMP    -- ❌ Ambiguous timezone
created_at TIMESTAMPTZ  -- ✅ Always UTC internally

-- Using FLOAT for money (floating point precision errors!)
price FLOAT             -- ❌ 9.99 may become 9.9900000001
price NUMERIC(10,2)     -- ✅ Exact decimal arithmetic

-- Forgetting CASCADE on DROP
DROP TABLE users;       -- ❌ ERROR if orders references users
DROP TABLE users CASCADE; -- ✅ Also drops dependent objects
```

### ✅ Best Practices
- Use `BIGINT GENERATED ALWAYS AS IDENTITY` (SQL standard) over `BIGSERIAL`
- Use `NUMERIC` for all monetary values — never `FLOAT`/`REAL`
- Always use `IF NOT EXISTS` / `IF EXISTS` in migration scripts
- Use schemas to organize tables by domain (`app`, `audit`, `reporting`)
- Store UUIDs with `gen_random_uuid()` for distributed systems

### 📝 Mini Summary
> DDL defines your data contract. Get it right up front — schema migrations on large tables in production are expensive and risky.

---

## Module 3: DML – CRUD Operations {#module-3}

### 📖 Explanation
**DML (Data Manipulation Language)** commands read and modify data: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, and PostgreSQL's powerful `UPSERT` (INSERT ON CONFLICT).

### 🔑 Key Concepts
- `INSERT INTO ... VALUES` / `INSERT INTO ... SELECT`
- `UPDATE ... SET ... WHERE`
- `DELETE FROM ... WHERE`
- `RETURNING` clause — get affected rows back
- `INSERT ON CONFLICT` (UPSERT)
- `UPDATE FROM` — join in updates
- Bulk operations with `COPY`

### 💻 Example
```sql
-- ─── INSERT ───
INSERT INTO users (email, username)
VALUES ('alice@example.com', 'alice'),
       ('bob@example.com',   'bob'),
       ('carol@example.com', 'carol');

-- INSERT with RETURNING (get generated IDs back)
INSERT INTO products (name, price, stock_qty)
VALUES ('Laptop Pro', 1299.99, 50)
RETURNING id, name, created_at;

-- INSERT from SELECT
INSERT INTO archive.old_orders (id, user_id, total, created_at)
SELECT id, user_id, total, created_at
FROM orders
WHERE created_at < NOW() - INTERVAL '2 years';

-- ─── UPSERT (INSERT ON CONFLICT) ───
-- Insert or update if email already exists
INSERT INTO users (email, username, updated_at)
VALUES ('alice@example.com', 'alice_new', NOW())
ON CONFLICT (email)
DO UPDATE SET
    username   = EXCLUDED.username,
    updated_at = EXCLUDED.updated_at;

-- Insert or do nothing
INSERT INTO user_tags (user_id, tag)
VALUES (1, 'premium')
ON CONFLICT (user_id, tag) DO NOTHING;

-- ─── UPDATE ───
UPDATE products
SET
    price     = price * 1.10,      -- 10% price increase
    updated_at = NOW()
WHERE category_id = 3
  AND is_active = TRUE
RETURNING id, name, price;

-- UPDATE with JOIN (UPDATE ... FROM)
UPDATE order_items oi
SET unit_price = p.price
FROM products p
WHERE oi.product_id = p.id
  AND oi.order_id IN (
      SELECT id FROM orders WHERE status = 'pending'
  );

-- ─── DELETE ───
DELETE FROM sessions
WHERE expires_at < NOW()
RETURNING id, user_id;  -- see what was deleted

-- DELETE with JOIN (using USING clause in PostgreSQL)
DELETE FROM order_items oi
USING orders o
WHERE oi.order_id = o.id
  AND o.status = 'cancelled'
  AND o.created_at < NOW() - INTERVAL '30 days';

-- ─── COPY (bulk import/export — fastest method) ───
-- Import from CSV
COPY products (name, price, stock_qty)
FROM '/data/products.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');

-- Export to CSV
COPY (SELECT * FROM products WHERE is_active = TRUE)
TO '/data/active_products.csv'
WITH (FORMAT CSV, HEADER TRUE);
```

### 🏭 Real-world Use Cases
- `UPSERT` — syncing data from external APIs (idempotent operations)
- `RETURNING` — getting generated IDs without a second query
- `COPY` — bulk data loading (100x faster than individual INSERTs)
- `UPDATE FROM` — denormalizing summary data into reporting tables

### ⚠️ Common Mistakes
```sql
-- DELETE/UPDATE without WHERE — destroys all data!
DELETE FROM users;             -- ❌ Deletes EVERYONE
DELETE FROM users WHERE id = 1; -- ✅ Specific target

-- UPDATE sets NULL unintentionally
UPDATE users SET email = NULL WHERE id = 1;  -- if email NOT NULL: error
-- Always check NOT NULL constraints before updating

-- UPSERT using wrong conflict target
INSERT INTO users (email, username)
VALUES ('a@b.com', 'alice')
ON CONFLICT DO NOTHING;  -- ❌ What conflict? Be specific:
ON CONFLICT (email) DO NOTHING; -- ✅

-- Slow bulk inserts (one at a time)
-- for row in data: INSERT INTO ... VALUES (row)  ← ❌ thousands of round trips
-- Use multi-row INSERT or COPY instead ✅
```

### ✅ Best Practices
- Always use `WHERE` in `UPDATE`/`DELETE` — double-check before running
- Use `RETURNING` to avoid follow-up `SELECT` queries
- Use `COPY` or multi-row `INSERT` for bulk data loading
- Use `ON CONFLICT DO UPDATE` for idempotent data sync operations
- Wrap destructive operations in a transaction with `BEGIN` / `ROLLBACK` for testing

### 📝 Mini Summary
> DML is your daily driver. Master UPSERT for idempotency, RETURNING for efficiency, and COPY for bulk operations — these three patterns appear in nearly every production application.

---

## Module 4: Filtering, Sorting & Aggregation {#module-4}

### 📖 Explanation
The `SELECT` statement is the heart of SQL. Filtering (`WHERE`), grouping (`GROUP BY`), aggregating (`COUNT`, `SUM`, `AVG`), filtering groups (`HAVING`), and sorting (`ORDER BY`) transform raw data into meaningful information.

### 🔑 Key Concepts
- `WHERE` — filter rows (before aggregation)
- `HAVING` — filter groups (after aggregation)
- Aggregate functions: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `STRING_AGG`, `ARRAY_AGG`
- `GROUP BY` — group rows for aggregation
- `ORDER BY` / `LIMIT` / `OFFSET`
- `DISTINCT` / `DISTINCT ON` (PostgreSQL)
- `FILTER` clause on aggregates
- `NULLIF`, `COALESCE`, `CASE WHEN`
- `LIKE` / `ILIKE` / `SIMILAR TO` / regex

### 💻 Example
```sql
-- ─── Basic filtering ───
SELECT id, email, username
FROM   users
WHERE  is_active = TRUE
  AND  created_at >= '2024-01-01'
  AND  email ILIKE '%@gmail.com'   -- case-insensitive LIKE
ORDER BY created_at DESC
LIMIT  20 OFFSET 40;               -- page 3 (20 per page)

-- ─── NULL handling ───
SELECT
    name,
    COALESCE(phone, 'N/A')          AS phone,        -- fallback for NULL
    NULLIF(discount_pct, 0)         AS discount,     -- treat 0 as NULL
    CASE
        WHEN salary >= 100000 THEN 'Senior'
        WHEN salary >= 60000  THEN 'Mid-level'
        ELSE                       'Junior'
    END                             AS level
FROM employees
WHERE fired_at IS NULL;             -- active employees only

-- ─── Aggregation ───
SELECT
    DATE_TRUNC('month', created_at) AS month,
    COUNT(*)                        AS total_orders,
    COUNT(DISTINCT user_id)         AS unique_customers,
    SUM(total)                      AS revenue,
    AVG(total)                      AS avg_order_value,
    MIN(total)                      AS min_order,
    MAX(total)                      AS max_order,
    PERCENTILE_CONT(0.5)
        WITHIN GROUP (ORDER BY total) AS median_order
FROM   orders
WHERE  status = 'delivered'
GROUP  BY DATE_TRUNC('month', created_at)
HAVING COUNT(*) >= 10               -- only months with 10+ orders
ORDER  BY month DESC;

-- ─── FILTER on aggregates (PostgreSQL) ───
SELECT
    COUNT(*)                              AS total_users,
    COUNT(*) FILTER (WHERE is_active)     AS active_users,
    COUNT(*) FILTER (WHERE NOT is_active) AS inactive_users,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE is_active) / COUNT(*), 2
    )                                     AS active_pct
FROM users;

-- ─── STRING_AGG / ARRAY_AGG ───
SELECT
    u.username,
    STRING_AGG(p.name, ', ' ORDER BY p.name)  AS products_bought,
    ARRAY_AGG(DISTINCT o.status)               AS order_statuses
FROM users u
JOIN orders o    ON o.user_id  = u.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p  ON p.id = oi.product_id
GROUP BY u.id, u.username;

-- ─── DISTINCT ON (PostgreSQL — latest order per user) ───
SELECT DISTINCT ON (user_id)
    user_id, id AS order_id, total, created_at
FROM   orders
ORDER  BY user_id, created_at DESC;
-- Returns most recent order per user
```

### 🏭 Real-world Use Cases
- Monthly revenue dashboards with `DATE_TRUNC` + `SUM`
- User cohort analysis with `COUNT(DISTINCT)`
- Building comma-separated tag lists with `STRING_AGG`
- Pagination with `LIMIT`/`OFFSET` or keyset pagination
- `DISTINCT ON` for latest record per group (avoid subquery)

### ⚠️ Common Mistakes
```sql
-- WHERE vs HAVING confusion
SELECT user_id, COUNT(*) AS cnt
FROM orders
WHERE COUNT(*) > 5        -- ❌ ERROR: can't use aggregate in WHERE
GROUP BY user_id
HAVING COUNT(*) > 5;      -- ✅ Filter after aggregation

-- COUNT(*) vs COUNT(column)
COUNT(*)        -- counts all rows including NULLs
COUNT(column)   -- counts only non-NULL values in that column

-- OFFSET pagination degrades at large pages
SELECT * FROM orders ORDER BY id LIMIT 20 OFFSET 100000;  -- ❌ Slow!
-- ✅ Use keyset pagination:
SELECT * FROM orders WHERE id > 100000 ORDER BY id LIMIT 20;

-- Selecting non-aggregated columns not in GROUP BY
SELECT user_id, email, COUNT(*)  -- ❌ email not in GROUP BY or aggregate
FROM orders
GROUP BY user_id;
```

### ✅ Best Practices
- Use `FILTER` clause instead of `CASE WHEN` inside aggregates
- Use `DATE_TRUNC` for time-series grouping, not `TO_CHAR`
- Avoid `OFFSET` for deep pagination — use keyset/cursor pagination
- Use `COALESCE` to handle NULLs explicitly in calculations
- Index columns used in `WHERE`, `GROUP BY`, and `ORDER BY`

### 📝 Mini Summary
> Aggregation and filtering are where SQL earns its power. Master `GROUP BY` + `HAVING`, the `FILTER` clause, and keyset pagination to write reports that are both correct and performant.

---

## Module 5: Joins {#module-5}

### 📖 Explanation
Joins combine rows from two or more tables based on related columns. Understanding join types and how the query planner executes them is critical for both correctness and performance.

### 🔑 Key Concepts
| Join Type | Returns |
|---|---|
| `INNER JOIN` | Only matching rows in both tables |
| `LEFT JOIN` | All left rows + matching right (NULL if no match) |
| `RIGHT JOIN` | All right rows + matching left (NULL if no match) |
| `FULL OUTER JOIN` | All rows from both, NULL where no match |
| `CROSS JOIN` | Cartesian product (every combination) |
| `SELF JOIN` | Table joined to itself |
| `LATERAL JOIN` | Correlated subquery in FROM clause |

### 💻 Example
```sql
-- ─── INNER JOIN ───
SELECT
    o.id        AS order_id,
    u.email,
    o.total,
    o.status
FROM orders o
INNER JOIN users u ON u.id = o.user_id
WHERE o.status = 'delivered';

-- ─── LEFT JOIN (users with their order count — include users with 0 orders) ───
SELECT
    u.id,
    u.email,
    COUNT(o.id)  AS order_count,
    COALESCE(SUM(o.total), 0) AS lifetime_value
FROM users u
LEFT JOIN orders o ON o.user_id = u.id AND o.status != 'cancelled'
GROUP BY u.id, u.email
ORDER BY lifetime_value DESC;

-- ─── Multi-table JOIN ───
SELECT
    u.username,
    o.id        AS order_id,
    p.name      AS product,
    oi.quantity,
    oi.unit_price,
    oi.quantity * oi.unit_price AS line_total
FROM users u
JOIN orders      o  ON o.user_id   = u.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products    p  ON p.id        = oi.product_id
WHERE o.created_at >= NOW() - INTERVAL '7 days';

-- ─── FULL OUTER JOIN (find gaps) ───
SELECT
    COALESCE(a.date, b.date) AS date,
    a.actual_sales,
    b.forecasted_sales
FROM actual_sales a
FULL OUTER JOIN forecasted_sales b ON a.date = b.date
WHERE a.date IS NULL OR b.date IS NULL;  -- find missing dates

-- ─── SELF JOIN (org chart: employee and their manager) ───
SELECT
    e.id,
    e.full_name             AS employee,
    m.full_name             AS manager,
    e.salary,
    e.salary - m.salary     AS salary_vs_manager
FROM employees e
LEFT JOIN employees m ON m.id = e.manager_id;

-- ─── LATERAL JOIN (last 3 orders per user) ───
SELECT
    u.id,
    u.email,
    recent.id    AS order_id,
    recent.total,
    recent.created_at
FROM users u
CROSS JOIN LATERAL (
    SELECT id, total, created_at
    FROM   orders
    WHERE  user_id = u.id
    ORDER  BY created_at DESC
    LIMIT  3
) AS recent;

-- ─── Anti-join pattern (users who never ordered) ───
-- Method 1: LEFT JOIN + IS NULL (fast)
SELECT u.id, u.email
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE o.id IS NULL;

-- Method 2: NOT EXISTS (often same plan, sometimes clearer intent)
SELECT u.id, u.email
FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);
```

### 🏭 Real-world Use Cases
- `LEFT JOIN` — customer reports including zero-purchase users
- `LATERAL` — top-N per group (latest events, recent transactions)
- `SELF JOIN` — hierarchical data (org charts, categories, threaded comments)
- Anti-join — finding gaps, unmatched records, churned users

### ⚠️ Common Mistakes
```sql
-- Missing JOIN condition — accidental CROSS JOIN
SELECT * FROM orders, users;  -- ❌ Cartesian product! Millions of rows
SELECT * FROM orders JOIN users ON orders.user_id = users.id; -- ✅

-- Filtering in WHERE vs ON with LEFT JOIN — different results!
-- ❌ This turns LEFT JOIN into INNER JOIN:
SELECT u.*, o.*
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE o.status = 'delivered';  -- ← filters out users with no orders!

-- ✅ Filter in ON clause to keep all users:
SELECT u.*, o.*
FROM users u
LEFT JOIN orders o ON o.user_id = u.id AND o.status = 'delivered';

-- Joining on non-indexed columns — massive performance hit
JOIN orders o ON o.user_id = u.id  -- ← user_id must be indexed!
```

### ✅ Best Practices
- Always index foreign key columns (PostgreSQL does NOT do this automatically)
- Prefer `LEFT JOIN + IS NULL` or `NOT EXISTS` over `NOT IN` for anti-joins (NOT IN fails with NULLs)
- Use `LATERAL` for top-N-per-group instead of correlated subqueries
- Qualify all column names with table alias in multi-table queries
- Understand the difference between filtering in `WHERE` vs `ON` for outer joins

### 📝 Mini Summary
> Joins are the heart of relational SQL. Master the LEFT JOIN filter trap, use LATERAL for top-N problems, and always index your foreign keys.

---

## Module 6: Subqueries & CTEs {#module-6}

### 📖 Explanation
**Subqueries** are queries nested inside other queries. **CTEs (Common Table Expressions)** with `WITH` make complex queries readable and composable. **Recursive CTEs** handle hierarchical/graph data.

### 🔑 Key Concepts
- Scalar subquery — returns one value
- Row subquery — returns one row
- Table subquery — returns a result set (in FROM)
- Correlated subquery — references outer query
- `IN` / `NOT IN` / `EXISTS` / `NOT EXISTS`
- CTE (`WITH`) — named temporary result set
- Recursive CTE (`WITH RECURSIVE`)
- Materialized CTEs (`MATERIALIZED` / `NOT MATERIALIZED`)

### 💻 Example
```sql
-- ─── Scalar Subquery ───
SELECT
    id,
    email,
    (SELECT COUNT(*) FROM orders WHERE user_id = u.id) AS order_count
FROM users u;
-- Note: correlated — runs once per user. Use LEFT JOIN + COUNT for large tables.

-- ─── Table Subquery in FROM ───
SELECT dept, avg_salary
FROM (
    SELECT
        department    AS dept,
        AVG(salary)   AS avg_salary,
        COUNT(*)      AS headcount
    FROM employees
    GROUP BY department
) dept_stats
WHERE avg_salary > 80000;

-- ─── EXISTS (check existence without returning data) ───
SELECT id, email
FROM users u
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.user_id = u.id
      AND o.total   > 1000
      AND o.created_at >= NOW() - INTERVAL '90 days'
);

-- ─── CTE (WITH) — readable multi-step query ───
WITH
monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', created_at) AS month,
        SUM(total)                       AS revenue
    FROM orders
    WHERE status = 'delivered'
    GROUP BY 1
),
revenue_with_growth AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month) AS prev_revenue
    FROM monthly_revenue
)
SELECT
    month,
    revenue,
    prev_revenue,
    ROUND(100.0 * (revenue - prev_revenue) / NULLIF(prev_revenue, 0), 2) AS growth_pct
FROM revenue_with_growth
ORDER BY month;

-- ─── Recursive CTE (org chart / category tree) ───
WITH RECURSIVE org_chart AS (
    -- Base case: top-level employees (no manager)
    SELECT
        id, full_name, manager_id,
        0           AS depth,
        full_name   AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case: employees reporting to already-found employees
    SELECT
        e.id,
        e.full_name,
        e.manager_id,
        oc.depth + 1,
        oc.path || ' → ' || e.full_name
    FROM employees e
    INNER JOIN org_chart oc ON oc.id = e.manager_id
    WHERE oc.depth < 10   -- prevent infinite loops
)
SELECT
    REPEAT('  ', depth) || full_name AS tree,
    depth,
    path
FROM org_chart
ORDER BY path;

-- ─── Recursive CTE (category breadcrumbs) ───
WITH RECURSIVE category_path AS (
    SELECT id, name, parent_id, name AS breadcrumb
    FROM categories
    WHERE id = 42   -- target category

    UNION ALL

    SELECT c.id, c.name, c.parent_id,
           c.name || ' > ' || cp.breadcrumb
    FROM categories c
    JOIN category_path cp ON cp.parent_id = c.id
)
SELECT breadcrumb FROM category_path WHERE parent_id IS NULL;
-- "Electronics > Computers > Laptops"

-- ─── CTE with data modification (writeable CTE) ───
WITH moved_orders AS (
    DELETE FROM orders
    WHERE status = 'cancelled'
      AND created_at < NOW() - INTERVAL '1 year'
    RETURNING *
)
INSERT INTO archive.orders
SELECT * FROM moved_orders;
```

### 🏭 Real-world Use Cases
- Recursive CTEs — category trees, comment threads, org hierarchies, graph traversal
- Writeable CTEs — atomic move operations (delete + insert)
- CTEs for readability — multi-step analytics pipelines
- `EXISTS` — efficient user segmentation queries

### ⚠️ Common Mistakes
```sql
-- NOT IN with NULLs is a classic bug!
SELECT * FROM a WHERE id NOT IN (SELECT user_id FROM b);
-- ❌ If ANY user_id in b is NULL, returns 0 rows!
-- ✅ Use NOT EXISTS:
SELECT * FROM a WHERE NOT EXISTS (SELECT 1 FROM b WHERE b.user_id = a.id);

-- Assuming CTEs are always materialized (they're not in PostgreSQL 12+)
-- PostgreSQL 12+ may inline CTEs — use MATERIALIZED keyword if needed
WITH expensive AS MATERIALIZED (
    SELECT ... FROM large_table  -- force materialization
)
SELECT * FROM expensive WHERE ...;

-- Infinite recursion in recursive CTE
-- Always add a depth limit or cycle detection!
WHERE depth < 50   -- ✅ safety limit
```

### ✅ Best Practices
- Use CTEs for readability, not necessarily performance (check `EXPLAIN`)
- Use `NOT EXISTS` instead of `NOT IN` when NULLs might be present
- Always add a depth limit to recursive CTEs
- Use writeable CTEs for atomic multi-step operations
- Use `LATERAL` when a subquery needs to reference the outer row

### 📝 Mini Summary
> CTEs make complex queries readable and maintainable. Recursive CTEs unlock hierarchical data patterns. Never use `NOT IN` with nullable subqueries — always use `NOT EXISTS`.

---

# PART II – SQL ADVANCED

---

## Module 7: Window Functions {#module-7}

### 📖 Explanation
**Window functions** perform calculations across a set of rows related to the current row — without collapsing rows like `GROUP BY`. They are the most powerful SQL feature for analytics and reporting, enabling rankings, running totals, moving averages, and lag/lead comparisons.

### 🔑 Key Concepts
- `OVER (PARTITION BY ... ORDER BY ...)` — window definition
- **Ranking:** `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `NTILE(n)`
- **Navigation:** `LAG()`, `LEAD()`, `FIRST_VALUE()`, `LAST_VALUE()`, `NTH_VALUE()`
- **Aggregate:** `SUM()`, `AVG()`, `COUNT()`, `MIN()`, `MAX()` as window functions
- **Frame:** `ROWS BETWEEN`, `RANGE BETWEEN`
- Named windows with `WINDOW` clause

### 💻 Example
```sql
-- ─── Ranking functions ───
SELECT
    id,
    full_name,
    department,
    salary,
    ROW_NUMBER()  OVER (PARTITION BY department ORDER BY salary DESC) AS row_num,
    RANK()        OVER (PARTITION BY department ORDER BY salary DESC) AS rank,
    DENSE_RANK()  OVER (PARTITION BY department ORDER BY salary DESC) AS dense_rank,
    NTILE(4)      OVER (PARTITION BY department ORDER BY salary DESC) AS quartile
FROM employees;
-- ROW_NUMBER: 1,2,3,4 (no ties)
-- RANK:       1,2,2,4 (gaps after ties)
-- DENSE_RANK: 1,2,2,3 (no gaps)

-- ─── Top N per group (using window function) ───
SELECT * FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
    FROM employees
) ranked
WHERE rn <= 3;  -- top 3 earners per department

-- ─── Running totals & moving averages ───
SELECT
    o.created_at::DATE                        AS date,
    SUM(o.total)                              AS daily_revenue,
    SUM(SUM(o.total)) OVER (ORDER BY o.created_at::DATE
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                                              AS cumulative_revenue,
    AVG(SUM(o.total)) OVER (ORDER BY o.created_at::DATE
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
                                              AS rolling_7day_avg
FROM orders o
WHERE o.status = 'delivered'
GROUP BY o.created_at::DATE
ORDER BY date;

-- ─── LAG / LEAD (compare to previous/next row) ───
SELECT
    month,
    revenue,
    LAG(revenue, 1)  OVER (ORDER BY month)  AS prev_month,
    LEAD(revenue, 1) OVER (ORDER BY month)  AS next_month,
    revenue - LAG(revenue) OVER (ORDER BY month)  AS mom_change,
    ROUND(
        100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
        / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 2
    )                                         AS mom_growth_pct
FROM monthly_revenue
ORDER BY month;

-- ─── FIRST_VALUE / LAST_VALUE ───
SELECT
    id,
    full_name,
    department,
    salary,
    FIRST_VALUE(salary) OVER dept_window  AS dept_max_salary,
    LAST_VALUE(salary)  OVER dept_window  AS dept_min_salary,
    salary / FIRST_VALUE(salary) OVER dept_window * 100 AS pct_of_max
FROM employees
WINDOW dept_window AS (
    PARTITION BY department
    ORDER BY salary DESC
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
);

-- ─── Percentile / distribution ───
SELECT
    department,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY salary) AS p25,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY salary) AS median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY salary) AS p75,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY salary) AS p90
FROM employees
GROUP BY department;

-- ─── Gap detection with LAG ───
SELECT
    user_id,
    login_date,
    LAG(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS prev_login,
    login_date - LAG(login_date) OVER (PARTITION BY user_id ORDER BY login_date)
        AS days_gap
FROM user_logins
ORDER BY user_id, login_date;
```

### 🏭 Real-world Use Cases
- **ROW_NUMBER + filter** — top-N per group, deduplication
- **Running SUM** — cumulative revenue, balance ledgers
- **LAG/LEAD** — month-over-month growth, churn detection
- **NTILE** — customer segmentation into quartiles/deciles
- **DENSE_RANK** — leaderboards, product rankings

### ⚠️ Common Mistakes
```sql
-- LAST_VALUE default frame misses most rows
SELECT LAST_VALUE(salary) OVER (ORDER BY salary DESC)
-- ❌ Default frame is RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
-- Only sees up to current row! Add explicit frame:
SELECT LAST_VALUE(salary) OVER (
    ORDER BY salary DESC
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING  -- ✅
)

-- Can't use window functions in WHERE clause
SELECT * FROM (
    SELECT *, RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk
    FROM employees
) r
WHERE rnk = 1;  -- ✅ Must wrap in subquery or CTE

-- RANK vs DENSE_RANK confusion in leaderboards
-- RANK: 1,1,3 (skips 2) — DENSE_RANK: 1,1,2 (no skip)
-- Choose based on business requirement
```

### ✅ Best Practices
- Define reusable windows with the `WINDOW` clause
- Always specify explicit `ROWS BETWEEN` frame for `FIRST_VALUE`/`LAST_VALUE`
- Use `ROW_NUMBER()` for deduplication, `RANK()`/`DENSE_RANK()` for leaderboards
- Window functions execute after `WHERE`, `GROUP BY`, and `HAVING` — plan accordingly
- For very large datasets, consider pre-aggregating before windowing

### 📝 Mini Summary
> Window functions are the analyst's superpower — ranking, running totals, period-over-period comparisons, all without losing row-level detail. Master them and most reporting queries become straightforward.

---

## Module 8: Indexes & Performance {#module-8}

### 📖 Explanation
Indexes are database structures that allow fast data lookup without full table scans. Choosing the right index type and knowing when (and when not) to index is the single biggest lever for query performance.

### 🔑 Key Concepts
- **B-Tree** — default; equality (`=`) and range (`<`, `>`, `BETWEEN`)
- **Hash** — equality only; faster than B-Tree for pure equality (PostgreSQL 10+)
- **GIN** — arrays, JSONB, full-text search (inverted index)
- **GiST** — geometric, range types, full-text (generalized search tree)
- **BRIN** — naturally ordered data (timestamps, sequential IDs) — tiny index
- **Partial index** — index only rows matching a WHERE clause
- **Composite index** — multiple columns; order matters
- **Expression index** — index on a function result
- **Covering index** — `INCLUDE` columns to enable index-only scans
- `EXPLAIN (ANALYZE, BUFFERS)` — read query execution plan

### 💻 Example
```sql
-- ─── B-Tree (default) ───
CREATE INDEX idx_orders_user_id   ON orders (user_id);
CREATE INDEX idx_orders_status    ON orders (status);
CREATE INDEX idx_orders_created   ON orders (created_at DESC);

-- Composite index (column order matters — most selective/common first)
CREATE INDEX idx_orders_user_status
    ON orders (user_id, status, created_at DESC);
-- Supports: WHERE user_id = ?
--           WHERE user_id = ? AND status = ?
--           WHERE user_id = ? AND status = ? ORDER BY created_at DESC
-- Does NOT help: WHERE status = ? (missing leading column)

-- ─── Covering index (index-only scan — avoids heap fetch) ───
CREATE INDEX idx_orders_covering
    ON orders (user_id, created_at DESC)
    INCLUDE (total, status);
-- Query can be satisfied entirely from index!
SELECT total, status
FROM   orders
WHERE  user_id = 1
ORDER  BY created_at DESC;

-- ─── Partial index (index subset of rows) ───
-- Only index active users (huge win if 90% are inactive)
CREATE INDEX idx_users_active_email
    ON users (email)
    WHERE is_active = TRUE;

-- Only index unprocessed jobs
CREATE INDEX idx_jobs_pending
    ON jobs (priority DESC, created_at)
    WHERE status = 'pending';

-- ─── Expression index ───
-- Query: WHERE LOWER(email) = 'alice@example.com'
CREATE INDEX idx_users_email_lower
    ON users (LOWER(email));

-- Query: WHERE DATE_TRUNC('day', created_at) = '2024-01-15'
CREATE INDEX idx_orders_date
    ON orders (DATE_TRUNC('day', created_at));

-- ─── GIN index for JSONB ───
CREATE INDEX idx_products_metadata
    ON products USING GIN (metadata);

-- Enables fast JSONB queries:
SELECT * FROM products WHERE metadata @> '{"brand": "Apple"}';
SELECT * FROM products WHERE metadata ? 'warranty';

-- ─── GIN for full-text search ───
ALTER TABLE articles ADD COLUMN search_vector TSVECTOR
    GENERATED ALWAYS AS (
        TO_TSVECTOR('english', COALESCE(title,'') || ' ' || COALESCE(body,''))
    ) STORED;

CREATE INDEX idx_articles_fts ON articles USING GIN (search_vector);

SELECT title, TS_RANK(search_vector, query) AS rank
FROM articles, TO_TSQUERY('english', 'postgresql & index') AS query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 10;

-- ─── BRIN for time-series ───
CREATE INDEX idx_events_created_brin
    ON events USING BRIN (created_at);
-- Tiny index — great for append-only tables ordered by time

-- ─── Concurrent index creation (no lock) ───
CREATE INDEX CONCURRENTLY idx_orders_email
    ON orders (user_id);
-- Allows writes during index build — use in production!

-- ─── EXPLAIN ANALYZE ───
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT o.id, o.total, u.email
FROM   orders o
JOIN   users  u ON u.id = o.user_id
WHERE  o.status = 'pending'
  AND  o.created_at >= NOW() - INTERVAL '7 days';

-- Read the plan:
-- Seq Scan    → full table scan (add index!)
-- Index Scan  → uses index, fetches heap rows
-- Index Only Scan → index has all needed columns (fastest)
-- Bitmap Heap Scan → multiple index conditions combined
-- Hash Join   → good for large unsorted sets
-- Nested Loop → good when inner set is small and indexed
-- Merge Join  → good for pre-sorted large sets

-- ─── Index maintenance ───
-- Find unused indexes
SELECT schemaname, tablename, indexname, idx_scan
FROM   pg_stat_user_indexes
WHERE  idx_scan = 0
  AND  indexname NOT LIKE 'pg_%'
ORDER BY schemaname, tablename;

-- Find bloated indexes
SELECT indexname, pg_size_pretty(pg_relation_size(indexname::regclass))
FROM   pg_indexes
WHERE  tablename = 'orders'
ORDER BY pg_relation_size(indexname::regclass) DESC;

-- Rebuild bloated index
REINDEX INDEX CONCURRENTLY idx_orders_user_id;
```

### 🏭 Real-world Use Cases
- B-Tree on FK columns for join performance
- Partial index on `WHERE status = 'pending'` for job queues
- GIN on JSONB for flexible product attribute filtering
- Covering index for hot read queries (dashboard APIs)
- BRIN on `created_at` in time-series / event tables

### ⚠️ Common Mistakes
```sql
-- Index on low-cardinality column (wastes space, rarely used)
CREATE INDEX ON orders (status);  -- only 5 distinct values — often slower than seq scan!
-- Use partial index or composite index instead

-- Missing index on foreign keys
-- PostgreSQL does NOT auto-create indexes on FK columns!
CREATE INDEX ON order_items (order_id);   -- ✅ always do this
CREATE INDEX ON order_items (product_id); -- ✅

-- Index not used due to implicit type cast
WHERE user_id = '123'  -- user_id is INTEGER, '123' is TEXT → cast → no index use!
WHERE user_id = 123    -- ✅ correct type

-- Indexing every column "just in case"
-- Each index slows INSERT/UPDATE/DELETE and costs disk space
-- Only index columns used in WHERE, JOIN ON, ORDER BY, GROUP BY

-- LIKE with leading wildcard ignores index
WHERE name LIKE '%apple%'  -- ❌ B-Tree can't help (use GIN + pg_trgm)
WHERE name LIKE 'apple%'   -- ✅ B-Tree can use prefix
```

### ✅ Best Practices
- Always index foreign key columns manually in PostgreSQL
- Use `CREATE INDEX CONCURRENTLY` in production to avoid locking
- Use partial indexes for sparse queries (status = 'pending', active = true)
- Use `INCLUDE` for covering indexes on hot read paths
- Regularly check `pg_stat_user_indexes` for unused indexes and remove them
- Use `EXPLAIN (ANALYZE, BUFFERS)` — not just `EXPLAIN` — to see actual performance

### 📝 Mini Summary
> Indexes are your #1 performance tool. Understand when each type applies, index your FKs manually, use partial and covering indexes for hot paths, and always validate with `EXPLAIN ANALYZE`.

---

## Module 9: Transactions & Concurrency {#module-9}

### 📖 Explanation
Transactions group operations into atomic units. PostgreSQL uses **MVCC (Multi-Version Concurrency Control)** to allow readers and writers to proceed without blocking each other, while maintaining data consistency.

### 🔑 Key Concepts
- **ACID** — Atomicity, Consistency, Isolation, Durability
- `BEGIN` / `COMMIT` / `ROLLBACK` / `SAVEPOINT`
- **Isolation levels:** READ COMMITTED (default), REPEATABLE READ, SERIALIZABLE
- **MVCC** — each transaction sees a snapshot of data
- **Locking:** row-level, table-level, advisory locks
- `SELECT ... FOR UPDATE` — pessimistic locking
- `SELECT ... FOR UPDATE SKIP LOCKED` — job queue pattern
- **Deadlock** — circular lock dependency
- `pg_locks` — inspect active locks

### 💻 Example
```sql
-- ─── Basic Transaction ───
BEGIN;

UPDATE accounts SET balance = balance - 500 WHERE id = 1;
UPDATE accounts SET balance = balance + 500 WHERE id = 2;

-- Validate
DO $$
BEGIN
    IF (SELECT balance FROM accounts WHERE id = 1) < 0 THEN
        RAISE EXCEPTION 'Insufficient funds';
    END IF;
END;
$$;

COMMIT;  -- or ROLLBACK on error

-- ─── SAVEPOINT (partial rollback) ───
BEGIN;

INSERT INTO orders (user_id, total) VALUES (1, 100) RETURNING id;
SAVEPOINT after_order;

INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES (currval('orders_id_seq'), 999, 1, 100);
-- If product 999 doesn't exist → FK violation

ROLLBACK TO SAVEPOINT after_order;  -- undo item, keep order
-- Continue with corrected data...
COMMIT;

-- ─── Isolation Levels ───
-- Default: READ COMMITTED (each statement sees latest committed data)
BEGIN;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- REPEATABLE READ (snapshot at start of transaction — no phantom reads for rows)
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT SUM(balance) FROM accounts WHERE user_id = 1;
-- ... other work ...
SELECT SUM(balance) FROM accounts WHERE user_id = 1;
-- Returns SAME result even if other transactions committed! ✅
COMMIT;

-- SERIALIZABLE (full serializability — prevents all anomalies, slowest)
BEGIN ISOLATION LEVEL SERIALIZABLE;
-- Use for financial transactions, inventory management

-- ─── SELECT FOR UPDATE (pessimistic lock) ───
BEGIN;

-- Lock the row for update, block other transactions
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;

COMMIT;

-- ─── SELECT FOR UPDATE SKIP LOCKED (job queue) ───
BEGIN;

SELECT id, payload
FROM   job_queue
WHERE  status = 'pending'
ORDER  BY priority DESC, created_at
LIMIT  1
FOR UPDATE SKIP LOCKED;  -- skip rows locked by other workers

UPDATE job_queue SET status = 'processing', started_at = NOW()
WHERE  id = <id_from_above>;

COMMIT;

-- ─── Advisory Locks (application-level mutex) ───
-- Acquire application-level lock (non-blocking check)
SELECT pg_try_advisory_lock(12345);  -- returns true if acquired
-- ... do exclusive work ...
SELECT pg_advisory_unlock(12345);

-- Session-level (released on disconnect)
SELECT pg_advisory_lock(hashtext('user_42_report'));

-- ─── Deadlock prevention ───
-- Always lock resources in consistent order!
-- Transaction 1: locks account 1 then 2
-- Transaction 2: locks account 2 then 1
-- → DEADLOCK!

-- ✅ Fix: always order by ID
BEGIN;
SELECT * FROM accounts WHERE id IN (1,2) ORDER BY id FOR UPDATE;
-- Lock both in same order ✅
COMMIT;

-- ─── Monitor locks ───
SELECT
    pid,
    locktype,
    relation::regclass,
    mode,
    granted,
    query
FROM pg_locks l
JOIN pg_stat_activity a USING (pid)
WHERE NOT granted;  -- blocked queries
```

### 🏭 Real-world Use Cases
- `BEGIN`/`COMMIT` — financial transfers, inventory updates
- `FOR UPDATE SKIP LOCKED` — distributed job queues (Sidekiq-style)
- `SAVEPOINT` — batch imports with partial retry
- `SERIALIZABLE` — inventory reservation systems
- Advisory locks — preventing duplicate cron job execution

### ⚠️ Common Mistakes
```sql
-- Long transactions hold locks — keep transactions short!
BEGIN;
-- ❌ Don't do HTTP requests, file I/O, or user input inside a transaction
UPDATE ...;
COMMIT;

-- SERIALIZABLE for all transactions — unnecessary overhead
-- Use READ COMMITTED for most reads; escalate only when needed

-- Deadlock from inconsistent lock order
-- Always acquire locks on multiple resources in a consistent order (sort by ID)

-- Not handling transaction errors in application code
-- If a query fails mid-transaction, always ROLLBACK before reusing the connection!
```

### ✅ Best Practices
- Keep transactions as short as possible
- Use `FOR UPDATE SKIP LOCKED` for distributed queue patterns
- Always handle transaction rollback in application error handlers
- Use `SERIALIZABLE` only when correctness requires it (with retry logic)
- Monitor `pg_locks` and `pg_stat_activity` for lock contention in production
- Use advisory locks to coordinate application-level distributed operations

### 📝 Mini Summary
> Transactions are your consistency guarantee. MVCC means readers never block writers in PostgreSQL. Master `FOR UPDATE SKIP LOCKED` for queues and keep transactions short to minimize contention.

---

## Module 10: PostgreSQL-Specific Features {#module-10}

### 📖 Explanation
PostgreSQL offers powerful features beyond standard SQL: JSONB for document storage, arrays, range types, table partitioning, full-text search, and advanced extensions. These features reduce the need for additional services.

### 🔑 Key Concepts
- **JSONB** — binary JSON with indexing (GIN)
- **Arrays** — native array columns and functions
- **Range types** — `DATERANGE`, `TSTZRANGE`, `INT4RANGE`
- **Table partitioning** — declarative partitioning by range, list, or hash
- **Full-text search** — `TSVECTOR`, `TSQUERY`, `pg_trgm`
- **Extensions** — `uuid-ossp`, `pg_trgm`, `PostGIS`, `pg_cron`, `timescaledb`
- **Generated columns** — computed at write time
- **Table inheritance**
- **`pg_cron`** — cron jobs inside PostgreSQL

### 💻 Example
```sql
-- ─── JSONB ───
CREATE TABLE events (
    id         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    type       VARCHAR(50) NOT NULL,
    payload    JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO events (type, payload) VALUES
('user.signup',   '{"user_id": 1, "email": "alice@example.com", "source": "organic"}'),
('order.placed',  '{"order_id": 42, "total": 99.99, "items": [{"sku":"A1","qty":2}]}'),
('page.view',     '{"path": "/products", "user_id": 1, "duration_ms": 350}');

-- JSONB operators
SELECT payload->>'email'          FROM events WHERE type = 'user.signup';   -- text
SELECT payload->'items'->0->>'sku' FROM events WHERE type = 'order.placed'; -- nested

-- Containment (@>)
SELECT * FROM events WHERE payload @> '{"user_id": 1}';

-- Key existence (?)
SELECT * FROM events WHERE payload ? 'email';

-- Update JSONB
UPDATE events
SET payload = payload || '{"processed": true}'::jsonb
WHERE id = 1;

-- Delete JSONB key
UPDATE events SET payload = payload - 'source' WHERE type = 'user.signup';

-- JSONB aggregation
SELECT
    type,
    JSONB_AGG(payload ORDER BY created_at) AS all_payloads,
    JSONB_OBJECT_AGG(id::text, payload->>'email') AS id_to_email
FROM events
GROUP BY type;

-- ─── Arrays ───
CREATE TABLE articles (
    id    SERIAL PRIMARY KEY,
    title TEXT,
    tags  TEXT[]
);

INSERT INTO articles (title, tags)
VALUES ('PostgreSQL Tips', ARRAY['postgres', 'database', 'performance']);

-- Array operators
SELECT * FROM articles WHERE tags @> ARRAY['postgres'];   -- contains
SELECT * FROM articles WHERE tags && ARRAY['postgres','mysql']; -- overlap
SELECT * FROM articles WHERE 'postgres' = ANY(tags);

-- Array functions
SELECT ARRAY_LENGTH(tags, 1), UNNEST(tags) FROM articles;
SELECT title, ARRAY_TO_STRING(tags, ', ') FROM articles;

-- ─── Range Types ───
CREATE TABLE room_bookings (
    id        SERIAL PRIMARY KEY,
    room_id   INTEGER NOT NULL,
    guest     TEXT,
    stay      DATERANGE NOT NULL,
    EXCLUDE USING GIST (room_id WITH =, stay WITH &&)  -- prevent overlaps!
);

INSERT INTO room_bookings (room_id, guest, stay)
VALUES (101, 'Alice', '[2024-01-10, 2024-01-15)');

-- Range operators
SELECT * FROM room_bookings WHERE stay @> '2024-01-12'::DATE;  -- contains date
SELECT * FROM room_bookings WHERE stay && '[2024-01-14, 2024-01-20)'::DATERANGE; -- overlap

-- ─── Table Partitioning ───
CREATE TABLE orders (
    id         BIGINT GENERATED ALWAYS AS IDENTITY,
    user_id    INTEGER NOT NULL,
    total      NUMERIC(12,2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2023 PARTITION OF orders
    FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

CREATE TABLE orders_2024 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE orders_2025 PARTITION OF orders
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

-- Default partition for out-of-range data
CREATE TABLE orders_default PARTITION OF orders DEFAULT;

-- Queries automatically route to correct partition (partition pruning)
SELECT * FROM orders WHERE created_at >= '2024-06-01';
-- Only scans orders_2024 partition!

-- Drop old data efficiently (instant vs DELETE)
DROP TABLE orders_2023;  -- drops entire partition

-- ─── pg_trgm (fuzzy search / LIKE optimization) ───
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX idx_products_name_trgm
    ON products USING GIN (name gin_trgm_ops);

-- Now LIKE with any pattern uses the index!
SELECT * FROM products WHERE name ILIKE '%macbook%';

-- Similarity score
SELECT name, SIMILARITY(name, 'macbookpro') AS score
FROM products
WHERE name % 'macbookpro'   -- % operator: similarity > threshold
ORDER BY score DESC;

-- ─── pg_cron ───
CREATE EXTENSION pg_cron;

-- Schedule daily cleanup at 2 AM UTC
SELECT CRON.SCHEDULE(
    'cleanup-old-sessions',
    '0 2 * * *',
    'DELETE FROM sessions WHERE expires_at < NOW()'
);

-- List scheduled jobs
SELECT * FROM CRON.JOB;
```

### 🏭 Real-world Use Cases
- **JSONB** — audit logs, event streams, flexible product attributes, user preferences
- **Arrays** — tags, permissions, multi-value attributes
- **Range types** — hotel bookings, subscription periods, price validity windows
- **Partitioning** — multi-year time-series data (logs, events, transactions)
- **pg_trgm** — product search, fuzzy matching, autocomplete

### ⚠️ Common Mistakes
```sql
-- JSON vs JSONB — always use JSONB!
-- JSON: stores raw text, no indexing, slower operators
-- JSONB: binary format, indexed, faster operators, preserves no key order/duplicates

-- Unbounded partitions cause issues
-- Always create a DEFAULT partition for out-of-range data
-- Otherwise INSERTs with unexpected dates will error!

-- Array column as substitute for proper normalization
tags TEXT[]   -- ❌ if you frequently search/join by individual tags
-- ✅ Use a separate tags table with FK for queryability

-- JSONB for frequently queried columns
metadata->>'user_id'   -- ❌ Slow without index; loses type safety
user_id INTEGER        -- ✅ Use proper columns for stable, known fields
```

### ✅ Best Practices
- Use `JSONB` for flexible, evolving attributes; use proper columns for stable ones
- Use range types + GIST exclusion constraints to prevent scheduling conflicts
- Partition large tables (>50M rows) by time range for query performance and data lifecycle
- Use `pg_trgm` for any user-facing search with LIKE/ILIKE
- Use `pg_cron` for scheduled maintenance tasks instead of external cron + psql scripts

### 📝 Mini Summary
> PostgreSQL is not just a SQL database — it's a platform. JSONB, arrays, range types, and partitioning reduce your need for external services and enable patterns that other databases require separate systems for.

---

## Module 11: Query Optimization & EXPLAIN {#module-11}

### 📖 Explanation
Query optimization is about understanding what PostgreSQL's planner does, identifying bottlenecks with `EXPLAIN ANALYZE`, and rewriting queries or adding indexes to achieve optimal plans. The query planner uses cost estimates and statistics to choose execution strategies.

### 🔑 Key Concepts
- `EXPLAIN` — show query plan (estimated costs)
- `EXPLAIN ANALYZE` — execute + show actual timing
- `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` — full detail
- **Scan types:** Seq Scan, Index Scan, Index Only Scan, Bitmap Heap Scan
- **Join types:** Nested Loop, Hash Join, Merge Join
- **Cost components:** startup cost, total cost
- `pg_stats` — column statistics used by planner
- `ANALYZE` / `VACUUM ANALYZE` — update planner statistics
- `work_mem` — memory for sorts and hash joins
- `enable_seqscan` / `enable_hashjoin` — planner flags (debugging only)

### 💻 Example
```sql
-- ─── Reading EXPLAIN output ───
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.email, COUNT(o.id) AS order_count
FROM   users u
LEFT   JOIN orders o ON o.user_id = u.id
WHERE  u.is_active = TRUE
GROUP  BY u.id, u.email
HAVING COUNT(o.id) > 5
ORDER  BY order_count DESC;

/*
Sample output:
Sort  (cost=1250.45..1253.45 rows=120 width=50) (actual time=45.2..45.3 rows=87)
  Sort Key: (count(o.id)) DESC
  Sort Method: quicksort  Memory: 32kB
  Buffers: shared hit=420 read=38
  ->  HashAggregate  (cost=1232.10..1244.10 rows=120 width=50)
        Group Key: u.id
        Filter: (count(o.id) > 5)
        ->  Hash Left Join  (cost=412.00..1132.10 rows=20000 width=16)
              Hash Cond: (o.user_id = u.id)
              ->  Seq Scan on orders o  (cost=0..820.00 rows=20000 width=8)
              ->  Hash  (cost=312.00..312.00 rows=8000 width=12)
                    Buckets: 8192  Batches: 1  Memory Usage: 512kB
                    ->  Seq Scan on users u  (cost=0..312.00 rows=8000 width=12)
                          Filter: (is_active = TRUE)
Planning Time: 0.8 ms
Execution Time: 45.9 ms
*/

-- Key things to look for:
-- 1. Seq Scan on large tables → consider adding index
-- 2. High "rows" estimate vs actual → run ANALYZE to update stats
-- 3. Nested Loop with large outer set → may need index on inner table
-- 4. "Batches > 1" in Hash Join → increase work_mem
-- 5. High "Buffers read" → data not in cache (cold cache or table too large)

-- ─── Planner statistics ───
-- Check column statistics
SELECT
    attname,
    n_distinct,
    correlation,
    most_common_vals,
    most_common_freqs
FROM pg_stats
WHERE tablename = 'orders'
  AND attname = 'status';

-- Force statistics update
ANALYZE orders;
VACUUM ANALYZE orders;  -- also reclaims dead tuples

-- ─── Common optimization patterns ───

-- Pattern 1: Avoid function on indexed column
-- ❌ Index not used:
SELECT * FROM orders WHERE DATE(created_at) = '2024-01-15';
-- ✅ Sargable (index used):
SELECT * FROM orders
WHERE created_at >= '2024-01-15' AND created_at < '2024-01-16';

-- Pattern 2: EXISTS vs COUNT for existence check
-- ❌ Counts all rows:
SELECT * FROM users WHERE (SELECT COUNT(*) FROM orders WHERE user_id = users.id) > 0;
-- ✅ Stops at first match:
SELECT * FROM users WHERE EXISTS (SELECT 1 FROM orders WHERE user_id = users.id);

-- Pattern 3: Avoid SELECT * in production
SELECT *         FROM orders;  -- ❌ Fetches all columns, can't use covering index
SELECT id, total FROM orders;  -- ✅ Minimal projection

-- Pattern 4: Keyset pagination over OFFSET
-- ❌ Slow for large pages:
SELECT * FROM orders ORDER BY id LIMIT 20 OFFSET 100000;
-- ✅ Fast keyset:
SELECT * FROM orders WHERE id > 100000 ORDER BY id LIMIT 20;

-- Pattern 5: Batch large deletes
-- ❌ Locks table, generates huge WAL:
DELETE FROM logs WHERE created_at < NOW() - INTERVAL '1 year';
-- ✅ Batch delete:
DO $$
DECLARE batch_size INT := 10000;
BEGIN
    LOOP
        DELETE FROM logs
        WHERE id IN (
            SELECT id FROM logs
            WHERE created_at < NOW() - INTERVAL '1 year'
            LIMIT batch_size
        );
        EXIT WHEN NOT FOUND;
        PERFORM pg_sleep(0.1);  -- breathing room for other queries
    END LOOP;
END $$;

-- Pattern 6: Use materialized CTE for repeated reference
WITH MATERIALIZED expensive_calc AS (
    SELECT user_id, SUM(total) AS ltv
    FROM orders
    WHERE status = 'delivered'
    GROUP BY user_id
)
SELECT u.email, ec.ltv
FROM users u
JOIN expensive_calc ec ON ec.user_id = u.id
WHERE ec.ltv > 1000;

-- ─── Configuration tuning ───
-- Per-session work_mem (for sort/hash operations)
SET work_mem = '256MB';

-- Show query plan as JSON for tooling (pgMustard, explain.dalibo.com)
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT ...;
```

### 🏭 Real-world Use Cases
- Profiling slow API endpoints by logging slow queries (`log_min_duration_statement`)
- Identifying missing indexes via `pg_stat_user_tables` (seq scan counts)
- Batching large deletes during off-peak hours
- Tuning `work_mem` for complex reporting queries

### ⚠️ Common Mistakes
```sql
-- Applying function on WHERE column (breaks index use)
WHERE UPPER(email) = 'ALICE@EXAMPLE.COM'   -- ❌
WHERE email = LOWER('ALICE@EXAMPLE.COM')   -- ✅ or use expression index

-- Trusting EXPLAIN without ANALYZE (estimated rows vs actual)
EXPLAIN SELECT ...  -- shows estimates only — can be very wrong!
EXPLAIN ANALYZE ... -- shows actual rows and timing ✅

-- Setting work_mem globally too high
SET work_mem = '1GB'  -- ❌ each sort/hash node PER QUERY gets this!
-- 100 concurrent queries × multiple nodes × 1GB = OOM
-- Set per-session for known heavy queries only

-- Ignoring vacuum — table bloat kills performance
-- Dead tuples accumulate and slow scans
-- Ensure autovacuum is running; manually VACUUM ANALYZE after bulk operations
```

### ✅ Best Practices
- Enable `log_min_duration_statement = 500` to log queries > 500ms
- Use `pg_stat_statements` extension to aggregate slow query statistics
- Always run `EXPLAIN (ANALYZE, BUFFERS)` — never trust estimated plans alone
- Run `ANALYZE` after bulk data loads to update planner statistics
- Use `pgBadger` or `pgMustard` to analyze query logs at scale
- Monitor `pg_stat_user_tables` for high `seq_scan` counts on large tables

### 📝 Mini Summary
> EXPLAIN ANALYZE is your performance X-ray. Learn to read scan types, join methods, and actual vs estimated rows. Most performance issues are solved by the right index and keeping statistics current.

---

## Module 12: Schema Design & Best Practices {#module-12}

### 📖 Explanation
Good schema design prevents performance problems, data integrity issues, and maintenance nightmares before they happen. This module covers naming conventions, audit patterns, soft deletes, multi-tenancy, and migration strategies.

### 🔑 Key Concepts
- Naming conventions (consistency prevents confusion)
- Audit columns (`created_at`, `updated_at`, `created_by`)
- Soft deletes (`deleted_at`) vs hard deletes
- Multi-tenancy patterns: shared table, schema per tenant, DB per tenant
- Enum vs lookup tables vs CHECK constraints
- Optimistic locking (`version` column)
- Migration best practices (zero-downtime)
- Connection pooling (PgBouncer)

### 💻 Example
```sql
-- ─── Naming conventions ───
-- Tables:        snake_case plural   → users, order_items, product_categories
-- Columns:       snake_case          → first_name, created_at, is_active
-- PKs:           id (always)
-- FKs:           {table_singular}_id → user_id, product_id
-- Indexes:       idx_{table}_{column(s)} → idx_orders_user_id
-- Constraints:   {type}_{table}_{column} → uq_users_email, chk_products_price
-- Sequences:     {table}_{column}_seq

-- ─── Standard audit columns ───
-- Add to every important table:
CREATE TABLE products (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    -- ... business columns ...

    -- Audit columns
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by  INTEGER REFERENCES users(id),
    updated_by  INTEGER REFERENCES users(id),
    version     INTEGER NOT NULL DEFAULT 1  -- optimistic locking
);

-- Auto-update updated_at with trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = NOW();
    NEW.version    = OLD.version + 1;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_products_updated_at
    BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ─── Soft deletes ───
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;

-- Partial index for active records only (fast lookups)
CREATE INDEX idx_users_active ON users (email) WHERE deleted_at IS NULL;

-- Views for convenience
CREATE VIEW active_users AS
SELECT * FROM users WHERE deleted_at IS NULL;

-- Restore: UPDATE users SET deleted_at = NULL WHERE id = ?;
-- Purge:   DELETE FROM users WHERE deleted_at < NOW() - INTERVAL '30 days';

-- ─── Optimistic locking ───
-- Application reads record with version
-- Application updates with version check
UPDATE products
SET
    price   = 149.99,
    version = version + 1
WHERE id      = 42
  AND version = 5;   -- ← if 0 rows updated, someone else updated first!
-- Application checks affected rows: if 0, retry or error

-- ─── Lookup table pattern (preferred over enums) ───
CREATE TABLE order_statuses (
    code        VARCHAR(20) PRIMARY KEY,
    label       VARCHAR(100) NOT NULL,
    description TEXT,
    is_terminal BOOLEAN NOT NULL DEFAULT FALSE,
    sort_order  SMALLINT NOT NULL DEFAULT 0
);

INSERT INTO order_statuses VALUES
('pending',    'Pending',    'Order received',          FALSE, 1),
('processing', 'Processing', 'Payment confirmed',       FALSE, 2),
('shipped',    'Shipped',    'Package dispatched',      FALSE, 3),
('delivered',  'Delivered',  'Customer received order', TRUE,  4),
('cancelled',  'Cancelled',  'Order cancelled',         TRUE,  5);

ALTER TABLE orders ADD CONSTRAINT fk_orders_status
    FOREIGN KEY (status) REFERENCES order_statuses(code);
-- Now adding a new status doesn't require schema migration!

-- ─── Multi-tenancy (Row-Level Security) ───
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY orders_tenant_isolation ON orders
    USING (tenant_id = current_setting('app.current_tenant_id')::INTEGER);

-- Application sets tenant at start of each request:
SET app.current_tenant_id = '42';
-- Now: SELECT * FROM orders; → automatically filtered to tenant 42

-- ─── Zero-downtime migration patterns ───

-- Adding a column (safe — instant):
ALTER TABLE users ADD COLUMN phone VARCHAR(20);  -- ✅ Instant

-- Adding NOT NULL column (requires default or backfill first):
-- Step 1: Add nullable
ALTER TABLE users ADD COLUMN tier VARCHAR(20);

-- Step 2: Backfill (batched)
UPDATE users SET tier = 'free' WHERE tier IS NULL;

-- Step 3: Add constraint (validate separately)
ALTER TABLE users ALTER COLUMN tier SET DEFAULT 'free';
ALTER TABLE users ADD CONSTRAINT chk_users_tier CHECK (tier IS NOT NULL) NOT VALID;
-- NOT VALID: existing rows not checked immediately (fast)
ALTER TABLE users VALIDATE CONSTRAINT chk_users_tier;
-- Validates without lock (uses ShareUpdateExclusiveLock only)

-- Renaming a column (requires app code support for both names):
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN user_name VARCHAR(50);
-- Step 2: Sync data (trigger or backfill)
-- Step 3: Deploy code supporting both
-- Step 4: Remove old column
ALTER TABLE users DROP COLUMN username;
```

### 🏭 Real-world Use Cases
- Audit columns — compliance, debugging, support tickets
- Soft deletes — GDPR right-to-erasure workflows, undo functionality
- Optimistic locking — concurrent form submissions, API race conditions
- RLS — SaaS multi-tenant data isolation at the database layer
- Zero-downtime migrations — blue-green deployments, rolling updates

### ⚠️ Common Mistakes
```sql
-- Using PostgreSQL ENUM type (hard to modify!)
CREATE TYPE status_enum AS ENUM ('pending', 'active');
-- ❌ Adding a value requires ALTER TYPE (can't be done in transaction!)
-- ✅ Use lookup table or CHECK constraint instead

-- Skipping updated_at / version columns
-- Makes debugging production issues extremely difficult

-- Long-running migrations that lock tables
ALTER TABLE orders ADD COLUMN notes TEXT NOT NULL DEFAULT '';
-- ❌ On large tables: rewrites entire table, long exclusive lock!
-- ✅ Add nullable first, backfill, then add constraint

-- Forgetting indexes on soft-delete queries
SELECT * FROM users WHERE deleted_at IS NULL AND email = ?;
-- Without partial index, scans ALL users including deleted ones!
```

### ✅ Best Practices
- Enforce consistent naming conventions from day one
- Every production table should have `created_at`, `updated_at`
- Use `NOT VALID` + `VALIDATE CONSTRAINT` for zero-downtime constraint addition
- Use Row Level Security for multi-tenant data isolation
- Use lookup tables instead of PostgreSQL `ENUM` for status/type columns
- Always test migrations on production-sized data before deploying

### 📝 Mini Summary
> Schema design is the foundation everything else rests on. Good naming, audit columns, soft deletes, and zero-downtime migration patterns are what separate hobby projects from production-grade systems.

---

# PART III – INTERVIEW & CHALLENGES

---

## Interview Questions {#interview-questions}

### 🟢 Basic Level

**Q1: What is the difference between `WHERE` and `HAVING`?**

**Answer:**
- `WHERE` filters **individual rows before** grouping and aggregation. It cannot reference aggregate functions.
- `HAVING` filters **groups after** `GROUP BY` aggregation. It can reference aggregate functions.
```sql
SELECT department, AVG(salary) AS avg_sal
FROM employees
WHERE is_active = TRUE          -- ← filters rows before grouping
GROUP BY department
HAVING AVG(salary) > 75000;    -- ← filters groups after aggregation
```

---

**Q2: What is the difference between `INNER JOIN`, `LEFT JOIN`, and `FULL OUTER JOIN`?**

**Answer:**
- `INNER JOIN` — returns only rows where there is a match in **both** tables.
- `LEFT JOIN` — returns **all rows from the left table**; right side is NULL if no match.
- `FULL OUTER JOIN` — returns **all rows from both tables**; NULL where no match on either side.

Real-world: Use `LEFT JOIN` when you want all customers even if they have no orders. Use `INNER JOIN` when only matched data matters.

---

**Q3: What is a Primary Key vs a Foreign Key?**

**Answer:**
- **Primary Key** — uniquely identifies each row in a table; must be unique and NOT NULL; only one per table.
- **Foreign Key** — a column in one table that references the Primary Key of another table; enforces **referential integrity** (you can't have an order for a user that doesn't exist).

```sql
CREATE TABLE orders (
    id      SERIAL PRIMARY KEY,          -- PK
    user_id INTEGER REFERENCES users(id) -- FK
);
```

---

**Q4: What is the difference between `DELETE`, `TRUNCATE`, and `DROP`?**

**Answer:**
| | `DELETE` | `TRUNCATE` | `DROP` |
|---|---|---|---|
| Scope | Rows | All rows | Entire table |
| `WHERE` support | ✅ Yes | ❌ No | ❌ No |
| Rollback | ✅ Yes | ✅ Yes (in transaction) | ❌ Not easily |
| Speed | Slower (logs each row) | Fast | Instant |
| Triggers | ✅ Fires | ❌ Doesn't fire | ❌ |
| Resets sequence | ❌ No | ✅ With `RESTART IDENTITY` | N/A |

---

**Q5: What is normalization? Explain 1NF, 2NF, and 3NF.**

**Answer:**
Normalization reduces data redundancy and improves integrity.
- **1NF:** Each column has atomic values (no arrays/repeating groups); each row is unique.
- **2NF:** 1NF + every non-key column depends on the **whole** primary key (eliminates partial dependency — relevant for composite PKs).
- **3NF:** 2NF + no transitive dependencies (non-key column depends only on PK, not on another non-key column).

Example of 3NF violation: `orders` table containing `customer_city` — city depends on `customer_id`, not `order_id`. Fix: move city to `customers` table.

---

### 🟡 Intermediate Level

**Q6: What is a window function? How does it differ from `GROUP BY`?**

**Answer:**
Both perform calculations across groups of rows, but:
- `GROUP BY` **collapses rows** into one row per group — you lose individual row data.
- Window functions **retain all rows** while adding a calculated column computed across a window of related rows.

```sql
-- GROUP BY: one row per department
SELECT department, AVG(salary) FROM employees GROUP BY department;

-- Window function: all rows + department average alongside each
SELECT
    full_name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS dept_avg
FROM employees;
```

---

**Q7: Explain the difference between `RANK()`, `DENSE_RANK()`, and `ROW_NUMBER()`.**

**Answer:**
All three assign numbers to rows within a window, but handle ties differently:
- `ROW_NUMBER()` — always unique: 1, 2, 3, 4 (ties broken arbitrarily)
- `RANK()` — ties get same rank, then skips: 1, 2, 2, **4** (gap after tie)
- `DENSE_RANK()` — ties get same rank, no gap: 1, 2, 2, **3**

Choose: `ROW_NUMBER` for deduplication, `DENSE_RANK` for leaderboards without gaps, `RANK` for competition-style ranking.

---

**Q8: What is an index and what types does PostgreSQL support?**

**Answer:**
An index is a data structure that allows fast row lookup without full table scan. PostgreSQL supports:
- **B-Tree** (default) — equality, range queries, sorting
- **Hash** — equality only; faster than B-Tree for pure equality lookups
- **GIN** — JSONB containment, arrays, full-text search (inverted index)
- **GiST** — geometric types, ranges, full-text (generalized)
- **BRIN** — block-level min/max; tiny index for naturally ordered data (time-series)
- **SP-GiST** — non-balanced structures (quadtrees, prefix trees)

---

**Q9: What is a CTE and when would you use it over a subquery?**

**Answer:**
A CTE (`WITH` clause) is a named temporary result set visible within a query. Use CTEs when:
1. **Readability** — breaking complex queries into named logical steps
2. **Reuse** — referencing the same subquery multiple times
3. **Recursion** — hierarchical data (`WITH RECURSIVE`)
4. **Writeable CTEs** — combining DML operations atomically

Subqueries are fine for simple one-off cases. CTEs shine for multi-step analytics or recursive patterns. In PostgreSQL 12+, CTEs may be inlined (same plan as subquery) unless `MATERIALIZED` is specified.

---

**Q10: What is MVCC and how does it affect reads and writes in PostgreSQL?**

**Answer:**
**MVCC (Multi-Version Concurrency Control)** means PostgreSQL maintains multiple versions of rows. When a transaction modifies a row, the old version is kept for concurrent readers.

Key implications:
- **Readers never block writers** and **writers never block readers** — high concurrency
- Each transaction sees a consistent **snapshot** of data at its start (or statement start for READ COMMITTED)
- Dead row versions accumulate and must be cleaned by **VACUUM**
- Long-running transactions can cause **table bloat** by preventing VACUUM from reclaiming old versions

---

### 🔴 Advanced Level

**Q11: How does the PostgreSQL query planner choose between Nested Loop, Hash Join, and Merge Join?**

**Answer:**
The planner estimates cost based on table statistics and chooses the join strategy:

| | **Nested Loop** | **Hash Join** | **Merge Join** |
|---|---|---|---|
| Best for | Small inner set with index | Large unsorted sets | Large pre-sorted sets |
| Index required | Inner table | Neither | Neither (uses sort) |
| Memory usage | Low | High (`work_mem`) | Moderate |
| When to tune | Add index on inner join key | Increase `work_mem` | Ensure data is sorted |

The planner uses `pg_statistic` (via `ANALYZE`) for row count estimates. Wrong estimates lead to bad plan choices — run `ANALYZE` after bulk loads and check actual vs estimated rows in `EXPLAIN ANALYZE`.

---

**Q12: What is table bloat? What causes it and how do you fix it?**

**Answer:**
**Table bloat** occurs when dead tuple versions (from `UPDATE`/`DELETE`) accumulate faster than `VACUUM` can reclaim them.

**Causes:**
- High-frequency `UPDATE`/`DELETE` workloads
- Long-running transactions preventing `VACUUM` from reclaiming rows
- Autovacuum configured too conservatively

**Effects:** Increased table/index size, slower sequential scans, wasted disk space.

**Solutions:**
```sql
-- Check bloat
SELECT relname, n_dead_tup, n_live_tup,
       ROUND(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- Reclaim space (requires brief lock)
VACUUM (ANALYZE, VERBOSE) orders;

-- Full reclaim + rewrite (locks table — use pg_repack instead!)
VACUUM FULL orders;   -- ❌ Long exclusive lock in production

-- ✅ Production: use pg_repack extension
-- pg_repack orders;  -- rewrites without exclusive lock
```

---

**Q13: Design a schema for a multi-tenant SaaS application. What are the tradeoffs of each approach?**

**Answer:**
Three approaches:

**1. Shared Database, Shared Schema (Row-Level)**
```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders
    USING (tenant_id = current_setting('app.tenant_id')::INT);
```
- ✅ Cheapest, easiest to operate, cross-tenant analytics possible
- ❌ Risk of data leakage if RLS misconfigured; noisy neighbor problems

**2. Shared Database, Separate Schemas**
```sql
CREATE SCHEMA tenant_42;
CREATE TABLE tenant_42.orders (...);
```
- ✅ Strong isolation, easy per-tenant backup/restore
- ❌ Schema proliferation (thousands of schemas → DDL migrations complex); no cross-tenant queries

**3. Separate Databases**
- ✅ Complete isolation, independent scaling, compliance-friendly
- ❌ Expensive, complex connection management, no cross-tenant analytics

**Recommendation:** Start with RLS on shared schema. Move to separate schemas/DBs only when isolation requirements or scale demands it.

---

**Q14: What is the difference between optimistic and pessimistic locking? When do you use each?**

**Answer:**
**Pessimistic Locking** — locks the row at read time, preventing others from modifying it:
```sql
SELECT * FROM orders WHERE id = 1 FOR UPDATE;  -- blocks others
```
Use when: contention is high, conflicts are frequent, operations are short.

**Optimistic Locking** — no lock at read; checks at write time that data hasn't changed:
```sql
-- Read: remember version = 5
UPDATE orders SET status = 'shipped', version = version + 1
WHERE id = 1 AND version = 5;  -- fails if someone else updated
-- Check: if 0 rows → conflict → retry
```
Use when: contention is low, reads are frequent, conflicts are rare (most web apps).

**`FOR UPDATE SKIP LOCKED`** — the best of both for job queues:
```sql
SELECT * FROM jobs WHERE status = 'pending' LIMIT 1 FOR UPDATE SKIP LOCKED;
-- Workers grab different jobs without blocking each other
```

---

**Q15: Explain PostgreSQL's WAL (Write-Ahead Log). How does it enable durability, replication, and PITR?**

**Answer:**
**WAL (Write-Ahead Log)** is an append-only log of all database changes. Before any data page is written to disk, the change is first written to WAL. This ensures:

1. **Durability (D in ACID):** On crash, PostgreSQL replays WAL to recover uncommitted changes. Data is never lost once a transaction's WAL record is fsynced.

2. **Streaming Replication:** Standby servers receive and replay WAL records in real-time, maintaining a hot standby copy.

3. **Point-in-Time Recovery (PITR):** By archiving WAL files, you can replay them to any specific timestamp after restoring a base backup.

4. **Logical Replication:** Decodes WAL to produce logical change streams (INSERT/UPDATE/DELETE events) for replication to heterogeneous systems.

```
Write → WAL Buffer → fsync to WAL file → Data Page Cache → Data Files
                          ↓
                    Streaming to standby
                          ↓
                    WAL archiving for PITR
```

**Key settings:**
- `wal_level = replica` (for replication) or `logical` (for logical decoding)
- `archive_mode = on` + `archive_command` for PITR
- `synchronous_commit = on` for full durability (off for async performance)

---

## Coding Challenges {#coding-challenges}

### Challenge 1: Analytics Report – Customer Lifetime Value Segmentation

**📋 Problem:**
Write a single SQL query that produces a customer LTV (Lifetime Value) segmentation report with:
1. Total revenue per customer (delivered orders only)
2. Order count, average order value, first/last order dates
3. Days since last order (recency)
4. LTV segment: `'Champion'` (top 20%), `'Loyal'` (top 21-50%), `'At Risk'` (51-80%), `'Dormant'` (bottom 20%)
5. Month-over-month revenue change per customer (last 2 months)
6. Return only customers with at least 2 orders

**Schema:**
```sql
users(id, email, username, created_at)
orders(id, user_id, total, status, created_at)
```

**✅ Solution:**
```sql
WITH
-- Step 1: Per-customer order statistics
customer_stats AS (
    SELECT
        u.id                            AS user_id,
        u.email,
        u.username,
        COUNT(o.id)                     AS order_count,
        SUM(o.total)                    AS lifetime_value,
        AVG(o.total)                    AS avg_order_value,
        MIN(o.created_at)               AS first_order_at,
        MAX(o.created_at)               AS last_order_at,
        NOW() - MAX(o.created_at)       AS time_since_last_order
    FROM users u
    JOIN orders o ON o.user_id = u.id AND o.status = 'delivered'
    GROUP BY u.id, u.email, u.username
    HAVING COUNT(o.id) >= 2
),

-- Step 2: LTV percentile ranking
ltv_ranked AS (
    SELECT
        *,
        NTILE(5) OVER (ORDER BY lifetime_value DESC) AS ltv_quintile
    FROM customer_stats
),

-- Step 3: Monthly revenue per customer (last 2 months)
monthly_rev AS (
    SELECT
        user_id,
        DATE_TRUNC('month', created_at)    AS month,
        SUM(total)                          AS monthly_total
    FROM orders
    WHERE status = 'delivered'
      AND created_at >= DATE_TRUNC('month', NOW()) - INTERVAL '1 month'
    GROUP BY user_id, DATE_TRUNC('month', created_at)
),

-- Step 4: MoM comparison
mom_comparison AS (
    SELECT
        user_id,
        SUM(monthly_total) FILTER (
            WHERE month = DATE_TRUNC('month', NOW())
        )                                   AS current_month_rev,
        SUM(monthly_total) FILTER (
            WHERE month = DATE_TRUNC('month', NOW()) - INTERVAL '1 month'
        )                                   AS prev_month_rev
    FROM monthly_rev
    GROUP BY user_id
)

-- Final output
SELECT
    lr.user_id,
    lr.email,
    lr.username,
    lr.order_count,
    ROUND(lr.lifetime_value, 2)             AS lifetime_value,
    ROUND(lr.avg_order_value, 2)            AS avg_order_value,
    lr.first_order_at::DATE                 AS first_order_date,
    lr.last_order_at::DATE                  AS last_order_date,
    EXTRACT(DAY FROM lr.time_since_last_order)::INT  AS days_since_last_order,
    CASE lr.ltv_quintile
        WHEN 1 THEN 'Champion'
        WHEN 2 THEN 'Loyal'
        WHEN 3 THEN 'Loyal'
        WHEN 4 THEN 'At Risk'
        WHEN 5 THEN 'Dormant'
    END                                     AS segment,
    ROUND(COALESCE(mc.current_month_rev, 0), 2) AS current_month_rev,
    ROUND(COALESCE(mc.prev_month_rev, 0), 2)    AS prev_month_rev,
    ROUND(
        100.0 * (COALESCE(mc.current_month_rev, 0) - COALESCE(mc.prev_month_rev, 0))
        / NULLIF(mc.prev_month_rev, 0), 2
    )                                       AS mom_growth_pct
FROM ltv_ranked lr
LEFT JOIN mom_comparison mc ON mc.user_id = lr.user_id
ORDER BY lr.lifetime_value DESC;
```

**💡 Explanation:**
- CTE chain breaks the problem into clear steps (stats → ranking → monthly → MoM)
- `NTILE(5)` divides customers into quintiles for segment assignment
- `FILTER` clause efficiently computes pivoted monthly aggregates without CASE WHEN
- `LEFT JOIN` on mom_comparison keeps customers with no recent orders
- `NULLIF` prevents division-by-zero in growth calculation

---

### Challenge 2: Detect Fraudulent Transactions

**📋 Problem:**
Write a query to flag potentially fraudulent activity:
1. Users with **3+ orders in the same hour** (velocity check)
2. Users with an order **>5× their own historical average**
3. Orders from a **new account (<24 hours old)**
4. Return: `user_id`, `order_id`, `fraud_flags` (array of triggered rules), `risk_score` (1 point per flag)

**Schema:**
```sql
users(id, email, created_at)
orders(id, user_id, total, status, created_at)
```

**✅ Solution:**
```sql
WITH
-- Rule 1: High velocity — 3+ orders in same hour window
velocity_check AS (
    SELECT DISTINCT user_id, id AS order_id
    FROM (
        SELECT
            id,
            user_id,
            COUNT(*) OVER (
                PARTITION BY user_id
                ORDER BY created_at
                RANGE BETWEEN INTERVAL '1 hour' PRECEDING AND CURRENT ROW
            ) AS orders_in_window
        FROM orders
        WHERE status != 'cancelled'
    ) windowed
    WHERE orders_in_window >= 3
),

-- Rule 2: Order total > 5× user's historical average
avg_check AS (
    SELECT
        o.id    AS order_id,
        o.user_id
    FROM orders o
    JOIN (
        SELECT
            user_id,
            AVG(total) AS hist_avg
        FROM orders
        WHERE status = 'delivered'
        GROUP BY user_id
        HAVING COUNT(*) >= 3   -- need at least 3 orders for baseline
    ) baseline ON baseline.user_id = o.user_id
    WHERE o.total > baseline.hist_avg * 5
),

-- Rule 3: Order from account < 24 hours old
new_account_check AS (
    SELECT o.id AS order_id, o.user_id
    FROM orders o
    JOIN users u ON u.id = o.user_id
    WHERE o.created_at < u.created_at + INTERVAL '24 hours'
),

-- Combine all orders with their fraud flags
all_orders AS (
    SELECT DISTINCT id AS order_id, user_id FROM orders
    WHERE status != 'cancelled'
),

flagged AS (
    SELECT
        ao.order_id,
        ao.user_id,
        ARRAY_REMOVE(ARRAY[
            CASE WHEN vc.order_id IS NOT NULL THEN 'HIGH_VELOCITY'   END,
            CASE WHEN ac.order_id IS NOT NULL THEN 'ABNORMAL_AMOUNT'  END,
            CASE WHEN na.order_id IS NOT NULL THEN 'NEW_ACCOUNT'      END
        ], NULL) AS fraud_flags
    FROM all_orders ao
    LEFT JOIN velocity_check    vc ON vc.order_id = ao.order_id
    LEFT JOIN avg_check         ac ON ac.order_id = ao.order_id
    LEFT JOIN new_account_check na ON na.order_id = ao.order_id
)

SELECT
    f.user_id,
    u.email,
    f.order_id,
    o.total,
    o.created_at,
    f.fraud_flags,
    CARDINALITY(f.fraud_flags)      AS risk_score,
    CASE
        WHEN CARDINALITY(f.fraud_flags) >= 2 THEN 'HIGH'
        WHEN CARDINALITY(f.fraud_flags) = 1  THEN 'MEDIUM'
        ELSE                                      'CLEAN'
    END                             AS risk_level
FROM flagged f
JOIN orders o ON o.id = f.order_id
JOIN users  u ON u.id = f.user_id
WHERE CARDINALITY(f.fraud_flags) > 0    -- only flagged orders
ORDER BY risk_score DESC, o.created_at DESC;
```

**💡 Explanation:**
- `RANGE BETWEEN INTERVAL '1 hour' PRECEDING AND CURRENT ROW` — sliding time-based window (not row-based)
- Each rule is isolated in its own CTE for testability
- `ARRAY_REMOVE(..., NULL)` — cleanly builds dynamic fraud flag array from CASE results
- `CARDINALITY()` counts array elements for risk scoring
- `LEFT JOIN` all rules and filter at end — flexible for adding new rules without restructuring

---

## Final Summary {#final-summary}

```
╔════════════════════════════════════════════════════════════════════╗
║          SQL & POSTGRESQL — COMPLETE KNOWLEDGE MAP                 ║
╠════════════════════════════════════════════════════════════════════╣
║  BASICS                                                            ║
║  Module 1  → Relational Model, Keys, Constraints, ACID            ║
║  Module 2  → DDL: CREATE/ALTER/DROP, Data Types                   ║
║  Module 3  → DML: INSERT/UPDATE/DELETE/UPSERT/COPY                ║
║  Module 4  → SELECT, Aggregation, FILTER, Pagination              ║
║  Module 5  → Joins: INNER/LEFT/LATERAL/SELF/Anti-join             ║
║  Module 6  → Subqueries, CTEs, Recursive CTEs                     ║
╠════════════════════════════════════════════════════════════════════╣
║  ADVANCED                                                          ║
║  Module 7  → Window Functions: RANK, LAG, Running Totals          ║
║  Module 8  → Indexes: B-Tree/GIN/BRIN, Partial, Covering          ║
║  Module 9  → Transactions, MVCC, Locking, SKIP LOCKED             ║
║  Module 10 → PostgreSQL: JSONB, Arrays, Ranges, Partitioning      ║
║  Module 11 → EXPLAIN ANALYZE, Query Optimization Patterns         ║
║  Module 12 → Schema Design, Audit, Soft Delete, RLS, Migrations   ║
╠════════════════════════════════════════════════════════════════════╣
║  TOP 10 POSTGRESQL RULES                                           ║
║   1. Always use TIMESTAMPTZ (never TIMESTAMP)                      ║
║   2. Always use NUMERIC for money (never FLOAT)                    ║
║   3. Always index FK columns manually (no auto-index in PG!)       ║
║   4. Use CREATE INDEX CONCURRENTLY in production                   ║
║   5. Never use NOT IN with nullable subqueries — use NOT EXISTS    ║
║   6. LEFT JOIN filter in WHERE = INNER JOIN (filter in ON!)        ║
║   7. Run VACUUM ANALYZE after bulk operations                      ║
║   8. Use EXPLAIN (ANALYZE, BUFFERS) — never trust estimates alone  ║
║   9. Use FOR UPDATE SKIP LOCKED for distributed job queues         ║
║  10. Use lookup tables over PostgreSQL ENUM type                   ║
╠════════════════════════════════════════════════════════════════════╣
║  OPTIMIZATION CHECKLIST                                            ║
║  □ Are FK columns indexed?                                         ║
║  □ Are WHERE/JOIN columns indexed?                                 ║
║  □ Is EXPLAIN ANALYZE showing Index Scans (not Seq Scans)?         ║
║  □ Are statistics current? (ANALYZE run after bulk loads)          ║
║  □ Are large tables partitioned?                                   ║
║  □ Is autovacuum configured and running?                           ║
║  □ Is work_mem set appropriately for sort/hash operations?         ║
║  □ Are slow queries logged? (log_min_duration_statement)           ║
║  □ Is pg_stat_statements enabled for query analytics?              ║
║  □ Are unused indexes cleaned up?                                  ║
╠════════════════════════════════════════════════════════════════════╣
║  NEXT STEPS                                                        ║
║  → PL/pgSQL: Functions, Stored Procedures, Triggers               ║
║  → PostgreSQL Replication (Streaming, Logical)                     ║
║  → Connection Pooling (PgBouncer)                                  ║
║  → TimescaleDB for time-series workloads                           ║
║  → PostGIS for geospatial queries                                  ║
║  → pg_partman for automated partition management                   ║
╚════════════════════════════════════════════════════════════════════╝
```

> 💡 **The Expert Mindset:** SQL mastery isn't about memorizing syntax — it's about understanding *how the database thinks*. Know your query plan, know your data distribution, know your access patterns. Every performance problem is just a mismatch between what the planner assumes and what's actually happening — `EXPLAIN ANALYZE` is your bridge between the two.

---
*Guide covers PostgreSQL 14+. SQL standard compliance noted where behavior differs.*
