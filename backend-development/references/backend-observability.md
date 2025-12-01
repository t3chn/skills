# Backend Observability (2025)

Modern observability practices with OpenTelemetry, metrics, logs, and traces.

## Three Pillars of Observability

```
┌─────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY                            │
├───────────────────┬───────────────────┬────────────────────┤
│      METRICS      │       LOGS        │      TRACES        │
│                   │                   │                    │
│   What happened   │  Why it happened  │  How it happened   │
│   (quantitative)  │  (qualitative)    │  (causal)          │
│                   │                   │                    │
│   Prometheus      │  Loki/ELK         │  Jaeger/Tempo      │
│   Grafana         │  Kibana           │  Zipkin            │
└───────────────────┴───────────────────┴────────────────────┘
```

## OpenTelemetry (Standard)

OpenTelemetry is the vendor-neutral standard for observability. Use it for all new projects.

### Python Setup

```bash
uv add opentelemetry-api opentelemetry-sdk \
    opentelemetry-instrumentation-fastapi \
    opentelemetry-instrumentation-httpx \
    opentelemetry-instrumentation-sqlalchemy \
    opentelemetry-instrumentation-redis \
    opentelemetry-exporter-otlp
```

```python
# otel_setup.py
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

def setup_telemetry(service_name: str) -> None:
    """Initialize OpenTelemetry with OTLP exporter."""
    resource = Resource(attributes={SERVICE_NAME: service_name})

    # Traces
    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter())
    )
    trace.set_tracer_provider(trace_provider)

    # Metrics
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(),
        export_interval_millis=60000,
    )
    metrics.set_meter_provider(
        MeterProvider(resource=resource, metric_readers=[metric_reader])
    )

# FastAPI integration
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()
setup_telemetry("my-api")
FastAPIInstrumentor.instrument_app(app)
```

### Node.js Setup

```bash
npm install @opentelemetry/sdk-node \
    @opentelemetry/auto-instrumentations-node \
    @opentelemetry/exporter-trace-otlp-grpc \
    @opentelemetry/exporter-metrics-otlp-grpc
```

```typescript
// tracing.ts
import { NodeSDK } from "@opentelemetry/sdk-node";
import { getNodeAutoInstrumentations } from "@opentelemetry/auto-instrumentations-node";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-grpc";
import { OTLPMetricExporter } from "@opentelemetry/exporter-metrics-otlp-grpc";
import { PeriodicExportingMetricReader } from "@opentelemetry/sdk-metrics";

const sdk = new NodeSDK({
  serviceName: "my-api",
  traceExporter: new OTLPTraceExporter({
    url: "http://localhost:4317",
  }),
  metricReader: new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter({
      url: "http://localhost:4317",
    }),
    exportIntervalMillis: 60000,
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();

process.on("SIGTERM", () => {
  sdk.shutdown().finally(() => process.exit(0));
});
```

## Metrics

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import FastAPI, Response

app = FastAPI()

# Define metrics
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

http_request_duration = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
)

active_connections = Gauge(
    "active_connections",
    "Number of active connections",
)

# Middleware to track metrics
@app.middleware("http")
async def metrics_middleware(request, call_next):
    import time
    start = time.time()

    active_connections.inc()
    try:
        response = await call_next(request)
        duration = time.time() - start

        http_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code,
        ).inc()

        http_request_duration.labels(
            method=request.method,
            endpoint=request.url.path,
        ).observe(duration)

        return response
    finally:
        active_connections.dec()

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain",
    )
```

### Custom Business Metrics

```python
# Business metrics
orders_total = Counter(
    "orders_total",
    "Total orders processed",
    ["status", "payment_method"],
)

order_value = Histogram(
    "order_value_dollars",
    "Order value distribution",
    buckets=[10, 25, 50, 100, 250, 500, 1000],
)

# Usage in business logic
def process_order(order: Order):
    # ... process order ...
    orders_total.labels(
        status="completed",
        payment_method=order.payment_method,
    ).inc()
    order_value.observe(order.total_amount)
```

## Structured Logging

### Python with structlog

```python
import structlog
from structlog.processors import JSONRenderer, TimeStamper, add_log_level

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        add_log_level,
        TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Usage
logger.info(
    "order_processed",
    order_id="12345",
    user_id="user_abc",
    amount=99.99,
    duration_ms=42,
)

# Output (JSON):
# {"event": "order_processed", "order_id": "12345", "user_id": "user_abc",
#  "amount": 99.99, "duration_ms": 42, "level": "info", "timestamp": "2025-01-09T12:00:00Z"}
```

### Request Context

```python
from contextvars import ContextVar
from uuid import uuid4
from fastapi import Request

request_id_var: ContextVar[str] = ContextVar("request_id", default="")

@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    request_id_var.set(request_id)

    # Bind to structlog context
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        path=request.url.path,
        method=request.method,
    )

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

### Node.js with Pino

```typescript
import pino from "pino";

const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  formatters: {
    level: (label) => ({ level: label }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
});

// Child logger with context
const requestLogger = logger.child({
  requestId: "abc-123",
  userId: "user_456",
});

requestLogger.info({ orderId: "order_789", amount: 99.99 }, "Order processed");

// Output:
// {"level":"info","time":"2025-01-09T12:00:00.000Z","requestId":"abc-123",
//  "userId":"user_456","orderId":"order_789","amount":99.99,"msg":"Order processed"}
```

## Distributed Tracing

### Manual Span Creation

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

async def process_payment(order_id: str, amount: float) -> bool:
    with tracer.start_as_current_span("process_payment") as span:
        span.set_attribute("order.id", order_id)
        span.set_attribute("payment.amount", amount)

        try:
            # Call payment provider
            with tracer.start_as_current_span("call_stripe"):
                result = await stripe_client.charge(amount)

            span.set_attribute("payment.success", True)
            span.set_attribute("payment.transaction_id", result.id)
            return True

        except PaymentError as e:
            span.set_attribute("payment.success", False)
            span.set_attribute("payment.error", str(e))
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            raise
```

### Trace Context Propagation

```python
from opentelemetry.propagate import inject, extract
from opentelemetry import trace
import httpx

async def call_downstream_service(url: str, data: dict) -> dict:
    """Call downstream service with trace context."""
    headers = {}
    inject(headers)  # Inject trace context into headers

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
        return response.json()

# Receiving service extracts context
@app.middleware("http")
async def extract_trace_context(request: Request, call_next):
    ctx = extract(request.headers)
    token = trace.context.attach(ctx)
    try:
        return await call_next(request)
    finally:
        trace.context.detach(token)
```

## Observability Stack (Docker Compose)

```yaml
# docker-compose.observability.yml
services:
  # Collector
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.114.0
    command: ["--config=/etc/otel-collector-config.yaml"]
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    ports:
      - "4317:4317"   # OTLP gRPC
      - "4318:4318"   # OTLP HTTP

  # Traces
  jaeger:
    image: jaegertracing/all-in-one:1.62
    ports:
      - "16686:16686"  # UI
      - "14268:14268"  # HTTP collector

  # Metrics
  prometheus:
    image: prom/prometheus:v2.55.0
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  # Visualization
  grafana:
    image: grafana/grafana:11.3.0
    ports:
      - "3000:3000"
    environment:
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Admin
    volumes:
      - grafana_data:/var/lib/grafana

  # Logs
  loki:
    image: grafana/loki:3.2.0
    ports:
      - "3100:3100"
    command: -config.file=/etc/loki/local-config.yaml

volumes:
  grafana_data:
```

### OpenTelemetry Collector Config

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 10s
    send_batch_size: 1000

exporters:
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true

  prometheus:
    endpoint: "0.0.0.0:8889"

  loki:
    endpoint: http://loki:3100/loki/api/v1/push

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [jaeger]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [loki]
```

## SLOs and Alerting

### Define SLOs

```yaml
# SLO definitions
slos:
  - name: api-availability
    description: API availability
    target: 99.9%
    indicator:
      type: availability
      good: http_requests_total{status!~"5.."}
      total: http_requests_total

  - name: api-latency
    description: API response time
    target: 95%
    indicator:
      type: latency
      threshold: 500ms
      metric: http_request_duration_seconds
```

### Prometheus Alerting Rules

```yaml
# alerts.yml
groups:
  - name: api-alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) /
          sum(rate(http_requests_total[5m])) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
          description: Error rate is {{ $value | humanizePercentage }}

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
          description: P95 latency is {{ $value }}s

      - alert: PodCrashLooping
        expr: |
          rate(kube_pod_container_status_restarts_total[15m]) > 0
        for: 5m
        labels:
          severity: warning
```

## Health Checks

```python
from fastapi import FastAPI, status
from pydantic import BaseModel

class HealthStatus(BaseModel):
    status: str
    checks: dict[str, bool]

@app.get("/health/live", status_code=status.HTTP_200_OK)
async def liveness():
    """Kubernetes liveness probe - is the app running?"""
    return {"status": "alive"}

@app.get("/health/ready", response_model=HealthStatus)
async def readiness():
    """Kubernetes readiness probe - is the app ready to serve traffic?"""
    checks = {
        "database": await check_database(),
        "redis": await check_redis(),
        "external_api": await check_external_api(),
    }

    all_healthy = all(checks.values())
    return HealthStatus(
        status="ready" if all_healthy else "not_ready",
        checks=checks,
    )

async def check_database() -> bool:
    try:
        await db.execute("SELECT 1")
        return True
    except Exception:
        return False
```

## Dashboards as Code

```json
// Grafana dashboard JSON (simplified)
{
  "title": "API Overview",
  "panels": [
    {
      "title": "Request Rate",
      "type": "graph",
      "targets": [
        {
          "expr": "sum(rate(http_requests_total[5m])) by (endpoint)",
          "legendFormat": "{{endpoint}}"
        }
      ]
    },
    {
      "title": "Error Rate",
      "type": "stat",
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))"
        }
      ],
      "thresholds": {
        "steps": [
          {"color": "green", "value": null},
          {"color": "yellow", "value": 0.01},
          {"color": "red", "value": 0.05}
        ]
      }
    },
    {
      "title": "P95 Latency",
      "type": "graph",
      "targets": [
        {
          "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
        }
      ]
    }
  ]
}
```

## Resources

- **OpenTelemetry:** https://opentelemetry.io/docs/
- **Prometheus:** https://prometheus.io/docs/
- **Grafana:** https://grafana.com/docs/
- **Jaeger:** https://www.jaegertracing.io/docs/
- **SRE Book:** https://sre.google/sre-book/
