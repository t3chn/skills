# Backend AI/LLM Integration (2025)

Patterns and best practices for integrating Large Language Models into backend services.

## LLM Provider SDKs

### Anthropic Claude

```python
# Python (with httpx for async)
from anthropic import AsyncAnthropic

client = AsyncAnthropic()  # Uses ANTHROPIC_API_KEY env var

async def generate_response(prompt: str) -> str:
    message = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
```

```typescript
// TypeScript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

async function generateResponse(prompt: string): Promise<string> {
  const message = await client.messages.create({
    model: "claude-sonnet-4-20250514",
    max_tokens: 1024,
    messages: [{ role: "user", content: prompt }],
  });
  return message.content[0].type === "text" ? message.content[0].text : "";
}
```

### OpenAI

```python
from openai import AsyncOpenAI

client = AsyncOpenAI()  # Uses OPENAI_API_KEY env var

async def generate_response(prompt: str) -> str:
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
    )
    return response.choices[0].message.content or ""
```

## Streaming Responses

### Server-Sent Events (SSE)

```python
# FastAPI SSE streaming
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from anthropic import AsyncAnthropic

app = FastAPI()
client = AsyncAnthropic()

@app.post("/chat/stream")
async def chat_stream(prompt: str):
    async def generate():
        async with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            async for text in stream.text_stream:
                yield f"data: {text}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
```

```typescript
// NestJS SSE streaming
import { Controller, Post, Body, Sse } from "@nestjs/common";
import { Observable } from "rxjs";
import Anthropic from "@anthropic-ai/sdk";

@Controller("chat")
export class ChatController {
  private client = new Anthropic();

  @Post("stream")
  @Sse()
  async streamChat(@Body("prompt") prompt: string): Promise<Observable<MessageEvent>> {
    return new Observable((subscriber) => {
      (async () => {
        const stream = await this.client.messages.stream({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1024,
          messages: [{ role: "user", content: prompt }],
        });

        for await (const event of stream) {
          if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
            subscriber.next({ data: event.delta.text } as MessageEvent);
          }
        }
        subscriber.complete();
      })();
    });
  }
}
```

## Prompt Management

### Structured Prompts with Templates

```python
from string import Template
from pydantic import BaseModel

class PromptTemplate(BaseModel):
    """Structured prompt template."""

    system: str
    user_template: Template

    def render(self, **kwargs) -> list[dict]:
        return [
            {"role": "system", "content": self.system},
            {"role": "user", "content": self.user_template.safe_substitute(**kwargs)},
        ]

# Define templates
SUMMARIZATION_PROMPT = PromptTemplate(
    system="You are a helpful assistant that summarizes text concisely.",
    user_template=Template("Summarize the following text in $max_sentences sentences:\n\n$text"),
)

# Usage
messages = SUMMARIZATION_PROMPT.render(
    text="Long article content...",
    max_sentences="3",
)
```

### Prompt Versioning

```python
from enum import Enum
from typing import Callable

class PromptVersion(Enum):
    V1 = "v1"
    V2 = "v2"

PROMPTS: dict[str, dict[PromptVersion, str]] = {
    "summarize": {
        PromptVersion.V1: "Summarize: {text}",
        PromptVersion.V2: "Provide a concise summary (max 3 sentences) of:\n\n{text}",
    },
}

def get_prompt(name: str, version: PromptVersion = PromptVersion.V2) -> str:
    return PROMPTS[name][version]
```

## Caching Strategies

### Response Caching with Redis

```python
import hashlib
import json
from redis.asyncio import Redis

redis = Redis.from_url("redis://localhost:6379")

async def cached_llm_call(
    prompt: str,
    model: str,
    ttl: int = 3600,  # 1 hour default
) -> str:
    # Create cache key from prompt hash
    cache_key = f"llm:{model}:{hashlib.sha256(prompt.encode()).hexdigest()}"

    # Check cache
    cached = await redis.get(cache_key)
    if cached:
        return cached.decode()

    # Call LLM
    response = await generate_response(prompt, model)

    # Cache response
    await redis.setex(cache_key, ttl, response)

    return response
```

### Semantic Caching (Advanced)

```python
# Cache similar prompts using embeddings
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_similar_cached(prompt: str, threshold: float = 0.95) -> str | None:
    prompt_embedding = model.encode(prompt)

    # Search vector DB for similar prompts
    # (using pgvector, Pinecone, Qdrant, etc.)
    similar = vector_db.search(
        embedding=prompt_embedding,
        threshold=threshold,
        limit=1,
    )

    if similar:
        return similar[0].cached_response
    return None
```

## Rate Limiting

### Token Bucket for API Calls

```python
import asyncio
from dataclasses import dataclass
from time import time

@dataclass
class TokenBucket:
    """Token bucket rate limiter for LLM API calls."""

    tokens_per_minute: int
    max_tokens: int

    def __post_init__(self):
        self.tokens = self.max_tokens
        self.last_update = time()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens: int = 1) -> bool:
        async with self._lock:
            now = time()
            elapsed = now - self.last_update
            self.tokens = min(
                self.max_tokens,
                self.tokens + elapsed * (self.tokens_per_minute / 60),
            )
            self.last_update = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    async def wait_and_acquire(self, tokens: int = 1) -> None:
        while not await self.acquire(tokens):
            await asyncio.sleep(0.1)

# Usage
rate_limiter = TokenBucket(tokens_per_minute=60, max_tokens=60)

async def rate_limited_llm_call(prompt: str) -> str:
    await rate_limiter.wait_and_acquire()
    return await generate_response(prompt)
```

### Per-User Rate Limiting

```python
from fastapi import HTTPException, Request, Depends
from redis.asyncio import Redis

async def check_user_rate_limit(
    request: Request,
    redis: Redis = Depends(get_redis),
) -> None:
    user_id = request.state.user_id
    key = f"ratelimit:llm:{user_id}"

    current = await redis.incr(key)
    if current == 1:
        await redis.expire(key, 60)  # 1 minute window

    if current > 10:  # 10 requests per minute
        raise HTTPException(429, "Rate limit exceeded")
```

## Cost Optimization

### Token Counting

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens for OpenAI models."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    model: str,
) -> float:
    """Estimate API call cost."""
    # Prices per 1M tokens (example, check current pricing)
    PRICES = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
    }

    prices = PRICES.get(model, {"input": 0, "output": 0})
    return (input_tokens * prices["input"] + output_tokens * prices["output"]) / 1_000_000
```

### Prompt Optimization

```python
# Use shorter system prompts
SYSTEM_PROMPT_VERBOSE = """
You are a helpful AI assistant designed to help users with their questions.
You should always be polite, informative, and helpful. When answering questions,
provide clear and concise responses. If you don't know something, say so.
"""  # 52 tokens

SYSTEM_PROMPT_CONCISE = "Helpful AI assistant. Be concise and accurate."  # 9 tokens

# Use structured output to reduce tokens
async def get_structured_response(prompt: str) -> dict:
    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
        # Request JSON response
        response_format={"type": "json_object"},
    )
    return json.loads(response.content[0].text)
```

## Error Handling & Retries

```python
import asyncio
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from anthropic import (
    APIConnectionError,
    RateLimitError,
    APIStatusError,
)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type((APIConnectionError, RateLimitError)),
)
async def resilient_llm_call(prompt: str) -> str:
    try:
        return await generate_response(prompt)
    except APIStatusError as e:
        if e.status_code == 529:  # Overloaded
            await asyncio.sleep(30)
            raise
        raise
```

## Observability

### Logging LLM Calls

```python
import structlog
from time import time
from functools import wraps

logger = structlog.get_logger()

def log_llm_call(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time()
        try:
            result = await func(*args, **kwargs)
            duration = time() - start
            logger.info(
                "llm_call_success",
                model=kwargs.get("model"),
                duration_ms=duration * 1000,
                input_tokens=count_tokens(str(args)),
            )
            return result
        except Exception as e:
            logger.error(
                "llm_call_error",
                model=kwargs.get("model"),
                error=str(e),
                duration_ms=(time() - start) * 1000,
            )
            raise
    return wrapper
```

### Metrics with Prometheus

```python
from prometheus_client import Counter, Histogram

llm_requests_total = Counter(
    "llm_requests_total",
    "Total LLM API requests",
    ["model", "status"],
)

llm_request_duration = Histogram(
    "llm_request_duration_seconds",
    "LLM request duration",
    ["model"],
    buckets=[0.5, 1, 2, 5, 10, 30, 60],
)

llm_tokens_total = Counter(
    "llm_tokens_total",
    "Total tokens used",
    ["model", "type"],  # type: input/output
)
```

## Security Considerations

### Input Validation

```python
from pydantic import BaseModel, field_validator
import re

class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 1024

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, v: str) -> str:
        # Remove potential injection attempts
        if len(v) > 10000:
            raise ValueError("Prompt too long")

        # Check for prompt injection patterns
        dangerous_patterns = [
            r"ignore previous instructions",
            r"disregard all prior",
            r"system:\s*",
        ]
        for pattern in dangerous_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError("Invalid prompt content")

        return v
```

### Output Sanitization

```python
def sanitize_llm_output(output: str) -> str:
    """Sanitize LLM output before sending to client."""
    # Remove potential XSS if output will be rendered as HTML
    import html
    return html.escape(output)

def validate_json_output(output: str, schema: type[BaseModel]) -> BaseModel:
    """Validate LLM JSON output against schema."""
    try:
        data = json.loads(output)
        return schema.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Invalid LLM output: {e}")
```

## Architecture Patterns

### Queue-Based Processing

```python
# For long-running LLM tasks
from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379")

@app.task(bind=True, max_retries=3)
def process_document(self, document_id: str):
    """Process document with LLM in background."""
    try:
        document = get_document(document_id)
        summary = generate_summary(document.content)
        save_summary(document_id, summary)
    except Exception as exc:
        self.retry(exc=exc, countdown=60)
```

### Gateway Pattern

```python
# Unified gateway for multiple LLM providers
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        pass

class AnthropicProvider(LLMProvider):
    async def generate(self, prompt: str, **kwargs) -> str:
        # Anthropic implementation
        pass

class OpenAIProvider(LLMProvider):
    async def generate(self, prompt: str, **kwargs) -> str:
        # OpenAI implementation
        pass

class LLMGateway:
    def __init__(self, primary: LLMProvider, fallback: LLMProvider | None = None):
        self.primary = primary
        self.fallback = fallback

    async def generate(self, prompt: str, **kwargs) -> str:
        try:
            return await self.primary.generate(prompt, **kwargs)
        except Exception:
            if self.fallback:
                return await self.fallback.generate(prompt, **kwargs)
            raise
```

## Resources

- **Anthropic SDK:** https://github.com/anthropics/anthropic-sdk-python
- **OpenAI SDK:** https://github.com/openai/openai-python
- **LangChain:** https://python.langchain.com/
- **Prompt Engineering Guide:** https://www.promptingguide.ai/
