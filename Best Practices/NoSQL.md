# NoSQL Best Practices

A practical reference for data modeling, performance, and operations across document, key-value, and wide-column NoSQL databases — with specific notes for **MongoDB**, **Redis**, and **DynamoDB**.

---

## 1. Data Modeling: Design for Queries, Not Entities

The single biggest mindset shift from relational DBs: **model around your access patterns, not your entities.**

- List out every query your application needs to run *before* designing the schema.
- Denormalize deliberately — duplicate data where it saves a read-time join/lookup, and accept the write-time cost of keeping copies in sync.
- Decide **embed vs. reference** per relationship:
  - **Embed** when data is read together, doesn't grow unbounded, and doesn't need independent querying (e.g., an order's shipping address).
  - **Reference** when data is large, grows unbounded, is shared across many parents, or needs independent access (e.g., a product referenced by thousands of orders).

```javascript
// MongoDB — embed when read together, bounded size
{
  _id: ObjectId("..."),
  customer: { name: "Jane Doe", email: "jane@example.com" },
  items: [
    { product_id: "p1", name: "Widget", qty: 2, price: 9.99 }
  ],
  shipping_address: { street: "123 Main St", city: "Palakkad" }
}

// Reference when the related data is large/shared/independently queried
{
  _id: ObjectId("..."),
  customer_id: ObjectId("..."),   // reference, not embed — customer has many orders
  product_ids: [ObjectId("..."), ObjectId("...")]
}
```

- Avoid unbounded arrays inside a single document (e.g., appending every comment ever made to a post) — they eventually hit document size limits (16MB in MongoDB) and degrade write performance. Use a separate collection/table with a reference instead once growth is unbounded.

---

## 2. Schema Design Patterns (Document Stores)

- **Bucket pattern** — group time-series or event data into buckets (e.g., one document per sensor per hour) instead of one document per data point, to reduce document count and index overhead.
- **Polymorphic pattern** — store different "shapes" of a similar entity in the same collection when queried together, differentiated by a `type` field.
- **Attribute pattern** — turn a large number of similar optional fields into a key/value array so you can index just the array rather than every possible field.
- **Subset pattern** — embed only the most-recently/most-relevant subset of a large related collection (e.g., last 10 reviews) and reference the rest, when most reads only need the subset.

```javascript
// Attribute pattern — instead of dozens of optional top-level fields
{
  name: "Product A",
  specs: [
    { k: "color", v: "red" },
    { k: "weight_kg", v: 1.2 }
  ]
}
// Then index specs.k / specs.v instead of each possible field individually
```

---

## 3. Indexing

- Index every field used in `find`/`WHERE`-equivalent filters, sort, and range queries — NoSQL engines will do full collection/table scans without one, and that cost grows with data size.
- Use **compound indexes** matching your actual query shape; field order matters (equality fields first, then sort fields, then range fields — MongoDB's ESR rule).
- Avoid indexing high-cardinality fields you rarely filter on — every index adds write overhead and storage.
- Use `explain()` (MongoDB) or equivalent to confirm an index is actually used, not just present.
- Set a **TTL index** for data with a natural expiry (sessions, verification codes, logs) instead of manually deleting it.

```javascript
// MongoDB compound index — Equality, Sort, Range (ESR) rule
db.orders.createIndex({ customer_id: 1, created_at: -1, status: 1 });

// TTL index — auto-expire after 1 hour
db.sessions.createIndex({ created_at: 1 }, { expireAfterSeconds: 3600 });

// Verify index usage
db.orders.find({ customer_id: "c1" }).explain("executionStats");
```

---

## 4. Key Design (Key-Value & Wide-Column Stores)

For Redis, DynamoDB, Cassandra-style stores, the **key** (or partition key) design *is* the schema.

- Design keys around access patterns: `entity_type:id:sub_resource` (e.g., `user:123:sessions`).
- Avoid **hot partitions** — don't let one key/partition receive disproportionate traffic (e.g., a single "global counter" key hammered by every request). Shard or add a random suffix and aggregate client-side if needed.
- For DynamoDB specifically: choose a partition key with high cardinality and even access distribution; use **composite sort keys** to model one-to-many and hierarchical relationships in a single table where appropriate (single-table design).
- Set explicit TTLs on ephemeral keys (sessions, cache entries, rate-limit counters) rather than relying on manual cleanup.

```python
# Redis key naming convention
"user:1001:profile"
"session:abc123"
"ratelimit:api:1001:2026-09-07T10"

# Redis TTL on ephemeral data
redis_client.setex("session:abc123", 3600, session_data)
```

```python
# DynamoDB single-table design example (Python + boto3)
table.put_item(Item={
    "PK": "USER#1001",
    "SK": "ORDER#2026-09-07#o123",
    "total": 49.99,
    "status": "shipped"
})
# Query all orders for a user with one partition-key query
table.query(KeyConditionExpression=Key("PK").eq("USER#1001") & Key("SK").begins_with("ORDER#"))
```

---

## 5. Consistency & Transactions

- Understand your database's consistency model — most NoSQL stores default to **eventual consistency** on reads from replicas; use strongly-consistent reads only where correctness demands it (they cost more and are slower).
- Don't assume ACID transactions across documents/items unless your database explicitly supports them for that operation (MongoDB supports multi-document ACID transactions since 4.0; DynamoDB supports transactional writes/reads across up to 100 items/4MB).
- Design for **idempotency** on writes — network retries are common in distributed systems, so use idempotency keys or conditional writes to avoid double-processing.
- Use optimistic concurrency control (a `version` field + conditional update) instead of locking, for update-heavy documents.

```javascript
// Optimistic concurrency in MongoDB
db.accounts.updateOne(
  { _id: acctId, version: currentVersion },
  { $inc: { balance: -100, version: 1 } }
);
// If matchedCount is 0, someone else updated it first — retry
```

```python
# DynamoDB conditional write to prevent double-processing
table.put_item(
    Item={"PK": "ORDER#123", "status": "processed"},
    ConditionExpression="attribute_not_exists(PK)"  # idempotent create
)
```

---

## 6. Query & Read Performance

- Avoid unbounded `SCAN`/full-collection-scan operations in production paths — always filter via an indexed key/query.
- Paginate everything — use cursor-based pagination (`_id`-based or native pagination tokens), not offset-based, since offset scans get slower as data grows.
- Project only the fields you need (`find(filter, {projection})` in MongoDB) instead of pulling entire documents when you only need a few fields.
- Cache aggressively for read-heavy, rarely-changing data (Redis in front of Mongo/Dynamo is a very common pattern) — but define a clear invalidation strategy up front.
- Batch reads/writes where the API supports it (`BatchGetItem`/`BatchWriteItem` in DynamoDB, bulk operations in MongoDB) instead of looping single-item calls.

```python
# DynamoDB batch get instead of N single GetItems
response = dynamodb.batch_get_item(RequestItems={
    "Orders": {"Keys": [{"PK": f"ORDER#{i}"} for i in order_ids]}
})
```

---

## 7. Security

- Enable **authentication** on every NoSQL instance — default installs of MongoDB/Redis historically shipped with no auth enabled; never expose them to the public internet.
- Use **role-based access control** with least privilege (MongoDB roles, Redis ACLs, IAM policies for DynamoDB) — don't connect the application with an admin/root credential.
- Enforce **TLS** for client-server and inter-node traffic.
- Restrict network exposure — private VPC/subnet, security groups, no public bind address (`0.0.0.0`) without a firewall in front.
- Validate and sanitize all inputs used to build queries — NoSQL injection is real (e.g., MongoDB operator injection via unsanitized JSON like `{"$gt": ""}` from user input).
- Encrypt sensitive fields at rest (native encryption-at-rest, or application-level field encryption for especially sensitive data like PII).

```python
# ❌ BAD — MongoDB NoSQL injection risk
# If `username` comes straight from request JSON, an attacker can send
# {"$ne": null} instead of a string and bypass the filter logic.
db.users.find_one({"username": request_json["username"]})

# ✅ GOOD — validate/coerce type before using in a query
username = str(request_json.get("username", ""))
if not isinstance(request_json.get("username"), str):
    raise ValueError("Invalid username")
db.users.find_one({"username": username})
```

```python
# Pydantic validation prevents operator injection by construction
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str
# FastAPI + Pydantic rejects non-string payloads before they reach the query
```

---

## 8. Backup & Recovery

- Enable continuous/point-in-time backups where supported (MongoDB Atlas continuous backups, DynamoDB PITR, Redis persistence via RDB snapshots + AOF).
- For Redis specifically, decide deliberately between **RDB** (periodic snapshots, faster restart, some data-loss window) and **AOF** (every-write log, safer, larger files) — or both, depending on your durability needs. Redis is often used as a cache where data loss is acceptable; don't assume durability without configuring it.
- Test restores regularly, not just backup creation.
- Encrypt backups at rest and restrict access via least-privilege IAM.

---

## 9. Monitoring & Operations

- Monitor: query latency (p50/p95/p99), replica lag, connection/throughput saturation, cache hit ratio (Redis), throttled requests (DynamoDB — watch `ConsumedReadCapacityUnits`/`ConsumedWriteCapacityUnits` against provisioned limits).
- Use native tooling: MongoDB Atlas Performance Advisor / `mongostat`/`mongotop`, Redis `INFO`/`SLOWLOG`, DynamoDB CloudWatch metrics.
- Alert on: replica lag exceeding threshold, memory pressure (especially for Redis, which is in-memory and can evict/OOM), throttling events, and slow-query log entries.
- Track collection/table growth and document/item size distribution over time — silent growth is how you hit document-size or partition-hot-key limits in production.

```javascript
// MongoDB slow query profiling
db.setProfilingLevel(1, { slowms: 100 });
db.system.profile.find().sort({ ts: -1 }).limit(10);
```

```
# Redis slow log
SLOWLOG GET 10
```

---

## 10. Scaling & High Availability

- Use **replica sets** (MongoDB) / **cluster mode** (Redis) / native multi-AZ (DynamoDB) for failover — never run a single node in production.
- Shard/partition proactively once a single node's working set or write throughput approaches its limits — retrofitting a sharding strategy onto an already-large collection is expensive.
- Choose your **shard key** / **partition key** for even distribution — a poorly chosen shard key (e.g., a monotonically increasing timestamp as the sole key) creates hot shards.
- For DynamoDB, use **on-demand capacity** for unpredictable traffic or carefully provision + monitor auto-scaling policies for predictable traffic to avoid throttling.
- For Redis, use **Redis Cluster** for horizontal scaling once a single instance's memory or throughput is a constraint; plan key distribution (hash tags) if you need multi-key operations to land on the same node.

---

## 11. Application Integration Notes

- **MongoDB (PyMongo/Motor)**: use connection pooling (default pool is usually fine, tune `maxPoolSize` under load), enable retryable writes, and use `bulk_write()` for batch operations instead of looping single inserts/updates.
- **Redis (redis-py)**: use a connection pool (`redis.ConnectionPool`), pipeline commands (`pipeline()`) when issuing multiple commands back-to-back to cut round-trips, and use `SCAN` instead of `KEYS *` in production (KEYS blocks the server on large datasets).
- **DynamoDB (boto3)**: use the higher-level `Table` resource for readability, batch operations where possible, and implement exponential backoff/retry for throttled (`ProvisionedThroughputExceededException`) requests — boto3's default retry config handles this but tune it for your workload.

```python
# Redis — pipeline instead of N round-trips
pipe = redis_client.pipeline()
pipe.incr("counter:visits")
pipe.expire("counter:visits", 86400)
pipe.execute()
```

```python
# Redis — never use KEYS * in production
# ❌ BAD: blocks the server
for key in redis_client.keys("session:*"):
    ...

# ✅ GOOD: non-blocking cursor-based iteration
for key in redis_client.scan_iter("session:*"):
    ...
```

---

## Quick Reference Checklist

- [ ] Schema modeled around actual query/access patterns, not entities
- [ ] Embed vs. reference decided deliberately per relationship; no unbounded arrays/documents
- [ ] Indexes match real query shape; compound index field order correct; verified with `explain()`
- [ ] Hot-partition/hot-key risk reviewed for key-value/wide-column stores
- [ ] Consistency model understood; idempotent writes; optimistic concurrency where needed
- [ ] Cursor-based pagination; projections used; batch operations instead of loops
- [ ] Auth + RBAC enabled; TLS enforced; no public bind address
- [ ] Inputs validated to prevent NoSQL/operator injection
- [ ] Backups enabled (PITR where supported) and restore-tested
- [ ] Monitoring/alerting on latency, replica lag, memory pressure, throttling
- [ ] Replication/HA configured; shard/partition key chosen for even distribution
- [ ] TTLs set on ephemeral data (sessions, cache, rate-limit counters)

---

*NoSQL trades relational flexibility for query-pattern-first design — the schema decisions you make early are harder to unwind than in a relational DB, so nail down access patterns before writing the first document.*
