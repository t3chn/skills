# Debugging Strategies & Mindset

## The Scientific Method for Debugging

1. **Observe** - Gather symptoms and data
2. **Hypothesize** - Form theories about the cause
3. **Test** - Verify or disprove theories
4. **Iterate** - Refine understanding
5. **Fix** - Apply solution
6. **Verify** - Confirm fix works

## Golden Rules

1. **Reproduce first** - Debugging without reproduction is guessing
2. **Simplify the problem** - Isolate variables
3. **Read the logs** - Error messages contain clues
4. **Check assumptions** - "It should work" isn't debugging
5. **Use scientific method** - Avoid random changes
6. **Document findings** - Future you will thank you

## Structured Logging Best Practices

### Log Levels

| Level | Purpose | Example |
|-------|---------|---------|
| **TRACE** | Very detailed, dev only | Request/response bodies |
| **DEBUG** | Detailed info for debugging | SQL queries, cache hits |
| **INFO** | General informational | User login, API calls |
| **WARN** | Potential issues | Deprecated API usage |
| **ERROR** | Error conditions | Failed API calls, exceptions |
| **FATAL** | Critical failures | Database connection lost |

### What to Log

**DO LOG:**
- Request/response metadata (not bodies in prod)
- Error messages with context
- Performance metrics (duration, size)
- Security events (login, permission changes)
- Business events (orders, payments)

**DON'T LOG:**
- Passwords or secrets
- Credit card numbers
- Personal identifiable information (PII)
- Session tokens
- Full request bodies in production

### Structured Logging Examples

**Python (structlog):**
```python
import structlog

logger = structlog.get_logger()

# Structured context
logger.info(
    "order_processed",
    order_id="123",
    user_id="user_abc",
    amount=99.99,
    duration_ms=42,
)
```

**Node.js (Pino):**
```typescript
import pino from "pino";

const logger = pino({ level: "info" });

logger.info(
  { orderId: "123", userId: "user_abc", amount: 99.99 },
  "Order processed"
);
```

**Go (Zap):**
```go
import "go.uber.org/zap"

logger, _ := zap.NewProduction()

logger.Info("order processed",
    zap.String("order_id", "123"),
    zap.String("user_id", "user_abc"),
    zap.Float64("amount", 99.99),
)
```

## Debugging Checklist

**Before Diving Into Code:**
- [ ] Read error message completely
- [ ] Check logs for context
- [ ] Reproduce the issue reliably
- [ ] Isolate the problem (binary search)
- [ ] Verify assumptions

**Investigation:**
- [ ] Enable debug logging
- [ ] Add strategic log points
- [ ] Use debugger breakpoints
- [ ] Profile performance if slow
- [ ] Check database queries
- [ ] Monitor system resources

**Production Issues:**
- [ ] Check APM dashboards
- [ ] Review distributed traces
- [ ] Analyze error rates
- [ ] Compare with previous baseline
- [ ] Check for recent deployments
- [ ] Review infrastructure changes

**After Fix:**
- [ ] Verify fix in development
- [ ] Add regression test
- [ ] Document the issue
- [ ] Deploy with monitoring
- [ ] Confirm fix in production
