# Database Debugging

## PostgreSQL

### EXPLAIN ANALYZE

```sql
-- Show query execution plan and actual timings
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id, u.name
ORDER BY order_count DESC
LIMIT 10;

-- Look for:
-- - Seq Scan on large tables (missing indexes)
-- - High execution time
-- - Large row estimates
```

### Slow Query Logging

```sql
-- Enable slow query logging
ALTER DATABASE mydb SET log_min_duration_statement = 1000; -- Log queries >1s

-- Check slow queries
SELECT query, calls, total_exec_time, mean_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### Active Query Monitoring

```sql
-- See currently running queries
SELECT pid, now() - query_start as duration, query, state
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY duration DESC;

-- Kill a long-running query
SELECT pg_terminate_backend(pid);
```

### Lock Monitoring

```sql
-- Check for blocking locks
SELECT
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

## MongoDB

### Explain Query Performance

```javascript
db.users.find({ email: "test@example.com" }).explain("executionStats");

// Look for:
// - totalDocsExamined vs nReturned (should be close)
// - COLLSCAN (collection scan - needs index)
// - executionTimeMillis (should be low)
```

### Profile Slow Queries

```javascript
// Enable profiling for queries >100ms
db.setProfilingLevel(1, { slowms: 100 });

// View slow queries
db.system.profile.find().limit(5).sort({ ts: -1 }).pretty();

// Disable profiling
db.setProfilingLevel(0);
```

### Index Analysis

```javascript
// Show all indexes
db.collection.getIndexes();

// Show index usage stats
db.collection.aggregate([{ $indexStats: {} }]);

// Find missing indexes
db.collection.find({ field: "value" }).explain("executionStats");
// If "stage": "COLLSCAN", need index
```

## Redis

### Monitor Commands

```bash
# See all commands in real-time
redis-cli MONITOR

# Check slow log
redis-cli SLOWLOG GET 10

# Set slow log threshold (microseconds)
redis-cli CONFIG SET slowlog-log-slower-than 10000
```

### Memory Analysis

```bash
# Memory usage by key pattern
redis-cli --bigkeys

# Memory usage details
redis-cli INFO memory

# Analyze specific key
redis-cli MEMORY USAGE mykey

# Find large keys
redis-cli DEBUG OBJECT mykey
```

### Connection Debugging

```bash
# Check connected clients
redis-cli CLIENT LIST

# Check connection stats
redis-cli INFO clients

# Kill specific client
redis-cli CLIENT KILL ID <client-id>
```

## Common Database Issues

### N+1 Query Problem

```python
# BAD: N+1 queries
posts = await Post.findAll()
for post in posts:
    post.author = await User.findById(post.authorId)  # N queries!

# GOOD: Single query with JOIN
posts = await Post.findAll({
    include: [{ model: User, as: "author" }]
})
```

### Missing Indexes

```sql
-- Before: Slow full table scan
SELECT * FROM orders
WHERE user_id = 123
ORDER BY created_at DESC
LIMIT 10;

-- EXPLAIN shows: Seq Scan on orders

-- Fix: Add index
CREATE INDEX idx_orders_user_id_created_at
ON orders(user_id, created_at DESC);

-- After: Index Scan - 100x faster
```

### Connection Pool Exhaustion

```typescript
// BAD: Connection leak
async function getUser(id) {
  const client = await pool.connect();
  const result = await client.query("SELECT * FROM users WHERE id = $1", [id]);
  return result.rows[0];
  // Connection never released!
}

// GOOD: Always release
async function getUser(id) {
  const client = await pool.connect();
  try {
    const result = await client.query("SELECT * FROM users WHERE id = $1", [id]);
    return result.rows[0];
  } finally {
    client.release(); // Always release
  }
}

// BETTER: Use pool directly
async function getUser(id) {
  const result = await pool.query("SELECT * FROM users WHERE id = $1", [id]);
  return result.rows[0];
  // Automatically releases
}
```
