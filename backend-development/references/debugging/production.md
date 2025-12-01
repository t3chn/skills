# Production Debugging

## Application Performance Monitoring (APM)

### New Relic

```typescript
// newrelic.js
export const config = {
  app_name: ["My Backend API"],
  license_key: process.env.NEW_RELIC_LICENSE_KEY,
  logging: { level: "info" },
  distributed_tracing: { enabled: true },
};

// Import at app entry
import "newrelic";
```

### DataDog

```typescript
import tracer from "dd-trace";

tracer.init({
  service: "backend-api",
  env: process.env.NODE_ENV,
  version: "1.0.0",
  logInjection: true,
});
```

### Sentry (Error Tracking)

```typescript
import * as Sentry from "@sentry/node";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,
});

// Capture errors
try {
  await riskyOperation();
} catch (error) {
  Sentry.captureException(error, {
    user: { id: userId },
    tags: { operation: "payment" },
  });
}
```

## Distributed Tracing

### OpenTelemetry

```typescript
import { NodeSDK } from "@opentelemetry/sdk-node";
import { getNodeAutoInstrumentations } from "@opentelemetry/auto-instrumentations-node";
import { JaegerExporter } from "@opentelemetry/exporter-jaeger";

const sdk = new NodeSDK({
  traceExporter: new JaegerExporter({
    endpoint: "http://localhost:14268/api/traces",
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
// Traces HTTP, database, Redis automatically
```

## Log Aggregation

### ELK Stack

```yaml
# docker-compose.yml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
    ports:
      - 9200:9200

  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    ports:
      - 5601:5601
```

### Loki + Grafana

```yaml
# promtail config for log shipping
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: backend-api
          __path__: /var/log/app/*.log
```

## Common Production Issues

### High CPU Usage

**Steps:**
1. Profile CPU (flamegraph)
2. Identify hot functions
3. Check for:
   - Infinite loops
   - Heavy regex operations
   - Inefficient algorithms (O(n²))
   - Blocking operations in event loop (Node.js)

```typescript
// BAD: Blocking event loop
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2); // Exponential time
}

// GOOD: Memoized
const memo = new Map();
function fibonacciMemo(n) {
  if (n <= 1) return n;
  if (memo.has(n)) return memo.get(n);
  const result = fibonacciMemo(n - 1) + fibonacciMemo(n - 2);
  memo.set(n, result);
  return result;
}
```

### Memory Leaks

**Symptoms:**
- Memory usage grows over time
- Eventually crashes (OOM)
- Performance degradation

**Common Causes:**
```typescript
// BAD: Event listeners not removed
class DataService {
  constructor(eventBus) {
    eventBus.on("data", (data) => this.processData(data));
    // Listener never removed, holds reference
  }
}

// GOOD: Remove listeners
class DataService {
  constructor(eventBus) {
    this.eventBus = eventBus;
    this.handler = (data) => this.processData(data);
    eventBus.on("data", this.handler);
  }

  destroy() {
    this.eventBus.off("data", this.handler);
  }
}
```

```typescript
// BAD: Global cache without limits
const cache = new Map();
function getCachedData(key) {
  if (!cache.has(key)) {
    cache.set(key, expensiveOperation(key)); // Grows forever
  }
  return cache.get(key);
}

// GOOD: LRU cache with size limit
import LRU from "lru-cache";
const cache = new LRU({ max: 1000, ttl: 1000 * 60 * 60 });
```

### Race Conditions

```typescript
// BAD: Race condition
let counter = 0;

async function incrementCounter() {
  const current = counter; // Thread 1 reads 0
  await doSomethingAsync(); // Thread 2 reads 0
  counter = current + 1; // Thread 1 writes 1, Thread 2 writes 1
  // Expected: 2, Actual: 1
}

// GOOD: Atomic operations (Redis)
async function incrementCounter() {
  return await redis.incr("counter");
}

// GOOD: Database transactions with locking
async function incrementCounter(userId) {
  await db.transaction(async (trx) => {
    const user = await trx("users")
      .where({ id: userId })
      .forUpdate() // Row-level lock
      .first();

    await trx("users")
      .where({ id: userId })
      .update({ counter: user.counter + 1 });
  });
}
```

## Resources

- **Node.js Debugging:** https://nodejs.org/en/docs/guides/debugging-getting-started/
- **Chrome DevTools:** https://developer.chrome.com/docs/devtools/
- **Clinic.js:** https://clinicjs.org/
- **Sentry:** https://docs.sentry.io/
- **Google SRE Book:** https://sre.google/sre-book/
